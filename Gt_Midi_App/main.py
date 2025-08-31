import sys
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import mido
import pretty_midi
import sounddevice as sd
import soundfile as sf
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QSpinBox, QLabel, QDoubleSpinBox, QComboBox, QMainWindow
)
from PySide6.QtCore import QThread, Signal, QFile
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_Gt_midi_main import Ui_MainWindow
from ui_Gt_midi_piano import Ui_Form 


# ==== 録音スレッド ====
class RecordThread(QThread):
    update_log = Signal(str)

    def __init__(self, samplerate=44100, channels=1, filename="input.wav", device=None, input_channel=0):
        super().__init__()
        self.samplerate = samplerate
        self.channels = channels
        self.filename = filename
        self.device = device
        self.input_channel = input_channel  # 録音するチャンネル番号
        self.recording = False
        self.audio_data = []
        self.record_thread = None
        self.wav_path = None


    def run(self):
        self.recording = True
        self.audio_data = []
        self.update_log.emit(f"録音開始... デバイスID: {self.device} チャンネル: {self.input_channel+1}")
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            # 指定したチャンネルのデータのみ取得
            channel_data = indata[:, self.input_channel].copy()
            self.audio_data.extend(channel_data)

        with sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,  # デバイスの総入力チャンネル数
            device=self.device,
            callback=callback
        ):
            while self.recording:
                sd.sleep(100)
        
        # モノラルで保存
        sf.write(self.filename, np.array(self.audio_data), self.samplerate)
        self.update_log.emit(f"録音終了: {self.filename}")


    def stop(self):
        self.recording = False


# ==== 音声 → MIDI変換関数 ====
def audio_to_midi(wav_path, output_midi, min_note_len=0.05, amp_thresh=0.02):
    y, sr = librosa.load(wav_path, sr=None, mono=True)

    # 音量で無音部分を除外
    rms = librosa.feature.rms(y=y)[0]
    frames = range(len(rms))
    t = librosa.frames_to_time(frames, sr=sr)

    f0, voiced_flag, _ = librosa.pyin(
        y, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('E6')
    )

    midi_notes = []
    prev_note = None
    note_start = None

    for i, (pitch, is_voiced) in enumerate(zip(f0, voiced_flag)):
        if is_voiced and pitch is not None and not np.isnan(pitch) and rms[i] > amp_thresh:
            try:
                note = round(librosa.hz_to_midi(pitch))
                if prev_note is None:
                    prev_note = note
                    note_start = t[i]
                elif note != prev_note:
                    dur = t[i] - note_start
                    if dur >= min_note_len:
                        midi_notes.append((prev_note, note_start, dur))
                    prev_note = note
                    note_start = t[i]
            except ValueError:
                continue
        else:
            if prev_note is not None:
                dur = t[i] - note_start
                if dur >= min_note_len:
                    midi_notes.append((prev_note, note_start, dur))
                prev_note = None
                note_start = None

    if prev_note is not None and note_start is not None:
        dur = t[-1] - note_start
        if dur >= min_note_len:
            midi_notes.append((prev_note, note_start, dur))

    # MIDIファイル生成
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    ticks_per_beat = mid.ticks_per_beat
    last_tick = 0
    for note, start, dur in midi_notes:
        start_ticks = int(start * ticks_per_beat * 2) - last_tick
        dur_ticks = int(dur * ticks_per_beat * 2)
        track.append(mido.Message('note_on', note=note, velocity=64, time=start_ticks))
        track.append(mido.Message('note_off', note=note, velocity=64, time=dur_ticks))
        last_tick = int(start * ticks_per_beat * 2) + dur_ticks

    mid.save(output_midi)


# ==== メインウィンドウ ====
class MidiConverterApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        self.actionOpen_Midi_Window.triggered.connect(self.open_midi_window)
        self.midi_window = None

        # Piano Roll用のUIも同様にロード
        self.piano_ui = Ui_Form()
        self.piano_widget = QWidget()
        self.piano_ui.setupUi(self.piano_widget)


        self.recording_counter = 1  # 録音ファイル用カウンタ
        self.conversion_counter = 1  # 変換ファイル用カウンタ
        self.is_recording = False
        self.is_playing = False

        # デバイス選択
        self.devices = sd.query_devices()
        self.input_devices = [
            (i, d['name']) for i, d in enumerate(self.devices) if d['max_input_channels'] > 0
        ]
        for idx, name in self.input_devices:
            self.device_combo.addItem(f"{name}", idx)

        # チャンネル選択
        self.update_channel_options()  # 初期化
        self.device_combo.currentIndexChanged.connect(self.update_channel_options)

        # パラメータ設定
        self.min_note_len_dial.setRange(1, 100)  # 1 = 0.01s, 100 = 1.00s
        self.min_note_len_dial.setValue(5)       # 0.05s
        self.min_note_len_dial.valueChanged.connect(lambda v: self.log_message(f"最小ノート長: {v/100:.2f} s"))
        

        self.amp_thresh_dial.setRange(1, 100)  # 0.001〜0.1 のスケーリングは後で適用
        self.amp_thresh_dial.setValue(20)      # 0.02
        self.amp_thresh_dial.valueChanged.connect(
            lambda v: self.log_message(f"しきい値: {v/1000:.3f}"))
        

        # 録音・停止
        self.btn_record.clicked.connect(self.toggle_recording)
        # 再生ボタン（トグル動作）
        self.btn_play.clicked.connect(self.toggle_playback)
        # Midi変換
        self.btn_convert.clicked.connect(lambda: self.convert_to_midi(auto_plot=True))
        # ファイル読み込み
        self.btn_load.clicked.connect(self.load_wav)
        # ログ表示
        self.log.setReadOnly(True)
        # === グラフ・スライダー表示エリア ===
        self.fig_wave = Figure(figsize=(6, 2))
        self.canvas_wave = FigureCanvas(self.fig_wave)
        layout = QVBoxLayout(self.frame_wave) # uiでQFrameを"frame_wave"にしておく
        layout.addWidget(self.canvas_wave)
        self.wave_slider.setRange(0, 100)
        self.wave_slider.setValue(0)
        self.wave_slider.valueChanged.connect(self.update_wave_view)
        

    # メインウィンドウ内（MidiConverterAppなど）
    def open_midi_window(self, midi_path):
        # サブウィンドウを生成
        self.piano_window = PianoWindow()
        self.piano_window.show()

        # MIDIを描画
        self.piano_window.plot_midi_notes(midi_path)

       

    def update_channel_options(self):
        self.channel_combo.clear()
        device_idx = self.device_combo.currentData()
        if device_idx is not None:
            max_channels = self.devices[device_idx]['max_input_channels']
            for i in range(max_channels):
                self.channel_combo.addItem(f"チャンネル {i+1}", i)

    def log_message(self, text):
        self.log.append(text)

    def toggle_recording(self):
        if not self.is_recording:
            # === 録音開始 ===
            while True:
                self.wav_path = f"input_{self.recording_counter:03d}.wav"
                if not os.path.exists(self.wav_path):
                    break
                self.recording_counter += 1

            device_id = self.device_combo.currentData()
            channel_idx = self.channel_combo.currentData()
            if device_id is None or channel_idx is None:
                self.log_message("デバイスとチャンネルを選択してください")
                return

            max_channels = self.devices[device_id]['max_input_channels']
            if channel_idx >= max_channels:
                self.log_message(f"選択したデバイスは{max_channels}チャンネルまでしかサポートしていません")
                return

            self.record_thread = RecordThread(
                filename=self.wav_path,
                samplerate=44100,
                channels=max_channels,
                device=device_id,
                input_channel=channel_idx
            )
            self.record_thread.update_log.connect(self.log_message)
            self.record_thread.start()

            self.btn_record.setText("録音停止")
            self.is_recording = True
            self.recording_counter += 1

        else:
            # === 録音停止 ===
            if self.record_thread:
                self.record_thread.stop()
                self.record_thread.wait()

            if self.wav_path and os.path.exists(self.wav_path):
                self.plot_waveform(self.wav_path)
                # self.convert_to_midi(auto_plot=True)　録音後に必ずmidi化するならon

            self.btn_record.setText("録音開始")
            self.is_recording = False

    def toggle_playback(self):
        if not self.wav_path or not os.path.exists(self.wav_path):
            self.log_message("再生するWAVファイルがありません")
            return

        if not self.is_playing:
            # 再生開始
            import sounddevice as sd
            import soundfile as sf
            data, samplerate = sf.read(self.wav_path)
            sd.play(data, samplerate)
            self.btn_play.setText("再生停止")
            self.is_playing = True
        else:
            # 再生停止
            import sounddevice as sd
            sd.stop()
            self.btn_play.setText("再生")
            self.is_playing = False

    #波形描画
    def plot_waveform(self, wav_path):
        from scipy.io import wavfile
        sample_rate, audio_data = wavfile.read(wav_path)
        time = np.arange(0, len(audio_data)) / sample_rate
        self._wave_data = {"time": time, "audio": audio_data}

        self.fig_wave.clear()
        ax = self.fig_wave.add_subplot(111)
        ax.plot(time, audio_data, linewidth=0.5, color='blue')
        ax.set_title("Audio Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(alpha=0.3)
        self.canvas_wave.draw()


    def update_wave_view(self, value):
        if not hasattr(self, "_wave_data"):
            return
        ax = self.fig_wave.axes[0]
        total_time = self._wave_data["time"][-1]
        view_width = total_time / 5  # 表示幅を全体の1/5に固定
        start = (total_time - view_width) * (value / 100)
        ax.set_xlim(start, start + view_width)
        self.canvas_wave.draw()


    def load_wav(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "WAVファイルを選択", "", "WAV Files (*.wav)")
        if file_path:
            self.wav_path = file_path
            self.log_message(f"読み込み: {file_path}")

    
    def convert_to_midi(self, auto_plot=False):
        if not self.wav_path or not os.path.exists(self.wav_path):
            self.log_message("WAVファイルがありません")
            return
        try:
            self.log_message("MIDI変換中...")
            min_len = self.min_note_len_dial.value()
            amp_thr = self.amp_thresh_dial.value()

            base_name = os.path.splitext(os.path.basename(self.wav_path))[0]
            while True:
                midi_path = f"{base_name}_{self.conversion_counter:03d}.mid"
                if not os.path.exists(midi_path):
                    break
                self.conversion_counter += 1

            # WAV → MIDI 変換
            audio_to_midi(self.wav_path, midi_path, min_note_len=min_len, amp_thresh=amp_thr)
            self.log_message(f"MIDI保存完了: {midi_path}")
            self.conversion_counter += 1

            # 変換後に piano roll を開いて描画
            self.open_midi_window(midi_path)

        except Exception as e:
            self.log_message(f"エラー: {str(e)}")

    

class PianoWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)   # ← ui_Gt_midi_piano.ui を反映

        # MatplotlibのFigureを用意
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

        self.fig_piano = Figure(figsize=(6, 3))
        self.canvas_piano = FigureCanvas(self.fig_piano)
        # スライダーの初期設定
        self.midi_slider.setRange(0, 100)
        self.midi_slider.setValue(0)
        self.midi_slider.valueChanged.connect(self.update_midi_view)

        # レイアウトにグラフを追加（uiにplace_holderがあるとベスト）
        layout = QVBoxLayout(self.frame_piano)  # 例: ui側でQFrameをframe_pianoに
        layout.addWidget(self.canvas_piano)

        self._midi_frames = 0


    def plot_midi_notes(self, midi_path):
        import pretty_midi
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        piano_roll = midi_data.get_piano_roll(fs=100)
        self._midi_frames = piano_roll.shape[1]

        self.fig_piano.clear()
        ax = self.fig_piano.add_subplot(111)
        img = ax.imshow(piano_roll, aspect='auto', cmap='viridis', origin='lower')
        ax.set_title("MIDI Piano Roll")
        ax.set_xlabel("Time (frames)")
        ax.set_ylabel("Note Number (MIDI)")
        self.fig_piano.colorbar(img, ax=ax, label="Velocity")
        self.canvas_piano.draw()
    

    def update_midi_view(self, value):
        if self._midi_frames == 0:
            return
        ax = self.fig_piano.axes[0]
        total_frames = self._midi_frames
        view_width = total_frames / 5
        start = (total_frames - view_width) * (value / 100)
        ax.set_xlim(start, start + view_width)
        self.canvas_piano.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MidiConverterApp()
    window.show()
    sys.exit(app.exec())