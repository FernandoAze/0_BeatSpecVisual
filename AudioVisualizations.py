import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

filename = "/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/Chopin_op10_n3_11/Chopin_op10_no3_p11.wav"

# Set the type of visualization to generate
# Options: "SpectogramLinear", "SpectogramLog", "SpectogramMel", "SpectogramCQT", "Chronogram", "Spectrum", "Waveform"
generate_viz_type = "SpectogramLinear"

output_path = "/home/macacomalandro/Documents/GitHub/TESE-do-Nando"

y, sr = librosa.load(filename)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)


def linearSpectogram():
    plt.figure(figsize=(12,8))
    librosa.display.specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear-frequency power spectrogram')
    plt.savefig(f"{output_path}/SpectogramLinear.png")

def logSpectogram():
    plt.figure(figsize=(12,8))
    librosa.display.specshow(D, y_axis='log', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log-frequency power spectrogram')
    plt.savefig(f"{output_path}/SpectogramLog.png")

def melSpectogram():
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    plt.figure(figsize=(12,8))
    librosa.display.specshow(S_dB, y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.savefig(f"{output_path}/SpectogramMel.png")

def cqtSpectogram():
    CQT = librosa.amplitude_to_db(np.abs(librosa.cqt(y, sr=sr)), ref=np.max)
    plt.figure(figsize=(12,8))
    librosa.display.specshow(CQT, x_axis='time', y_axis='cqt_hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (Hz)')
    plt.savefig(f"{output_path}/SpectogramCQT.png")

def chronogram():
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.figure(figsize=(12,8))
    librosa.display.specshow(C, x_axis='time', y_axis='chroma')
    plt.colorbar()
    plt.title('Chromagram')
    plt.savefig(f"{output_path}/Chronogram.png")
def MFCC():
    ##mau
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    plt.figure(figsize=(12,8))
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.savefig(f"{output_path}/MFCC.png")
def spectrum():
    S = np.abs(librosa.stft(y))
    S_dB = librosa.amplitude_to_db(S, ref=np.max)
    freqs = librosa.fft_frequencies(sr=sr)
    plt.figure(figsize=(12,8))
    plt.plot(freqs, S_dB.mean(axis=1))
    plt.xlim(0, 4000)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Spectrum')
    plt.savefig(f"{output_path}/Spectrum.png")
def waveform():
    plt.figure(figsize=(12,8))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Waveform')
    plt.savefig(f"{output_path}/Waveform.png")

#Spectogram Visualizations:
# linearSpectogram()
# logSpectogram()
# melSpectogram()
# cqtSpectogram()
# chronogram()
# spectrum()
# waveform()
# MFCC()