import sounddevice as sd
import numpy as np

SAMPLE_FREQ = 44100

def gaussian (x, mu, sig):
    return np.exp(-np.power(x-mu, 2.) / (2* np.power(sig, 2.)))

def stepf(size, steps):
    return np.floor(np.arange(size)/(size/steps))

def argrow(array, size):
    return np.repeat(array, size/len(array)) 

def artone(x, fs):
    t = np.arange(len(x))/fs #/fs -> #sec
    return np.sin((2*np.pi*110*x)*t)

def stepsmooth(ar, l):
    re = np.zeros(len(ar)-l)
    for i in range(l):
        re += (ar[:-l] + ar[l:]) / (2.0)
    return re/l

def reflect(x, l):
    fs = 44100
    return np.append(x[:l], x[l:] + x[:-l])

def play(sounddata):
    fs = 44100
    sd.Stream.write(sounddata)

def get_test():
    fs = 44100
    duration = 2*10

    #intro
    intro1 = np.sin(np.arange(0, fs*duration)*2*np.pi/(fs*duration))
    intro2 = gaussian(np.arange(len(intro1)), 0, len(intro1)/4)
    intro = artone(intro1, fs) + artone(intro2, fs)

    #melody
    melody = np.array([1, 2, 3, 4, 6, 5, 4, 3, 5, 4, 3, 2], dtype='float32')
    bass = np.array([1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], dtype='float32')/2
    beat = artone(argrow(melody, fs*5), fs) + artone(argrow(bass, fs*5), fs)

    signal = np.append(intro, beat)

    sd.play(signal, fs)
    return signal
sd.default.samplerate = 44100


