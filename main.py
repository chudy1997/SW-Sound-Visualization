import pyaudio as pya
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)


def init_audio():
	pa=pya.PyAudio()
	sIn=pa.open(format=pya.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
	sOut=pa.open(format=pya.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)		
		
	return pa, sIn, sOut
	

def draw(data):
	sOut.write(data)
	

def clean_audio(pa, sIn, sOut):
	sIn.stop_stream()
	sOut.stop_stream()
	sIn.close()
	sOut.close()
	pa.terminate()
	

if __name__ == "__main__":
	#init
	pa, sIn, sOut = init_audio()

	#process
	for i in range(10000):
		data = np.fromstring(sIn.read(CHUNK),dtype=np.int16)
		draw(data)

	#clean
	clean_audio(pa, sIn, sOut)