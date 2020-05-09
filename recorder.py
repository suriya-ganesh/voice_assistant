import sys

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
if len(sys.argv) > 1:
    write(f'input/{sys.argv[1]}.wav', fs, myrecording)  # Save as WAV file
else:
    write('input/recording.wav', fs, myrecording)