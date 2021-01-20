import requests
from flask import Flask, jsonify, request, url_for
import json
from sklearn import svm
from pycm import *
from os import walk
import librosa 
import numpy as np
import pickle
import base64
import os.path

app = Flask(__name__)

def extractMelSpectrogram_features(folder):
    hop_length = 512
    n_fft = 2048
    n_mels = 128
    labels = {'blues': 0, 'classical': 1, 'country': 2, 'disco': 3, 'hiphop': 4, 'jazz': 5, 'metal': 6, 'pop': 7, 'reggae': 8, 'rock': 9}
    a = []
    b = []
    print("aaaaaaaaaaaaaaaaaaaaaaa")
    for nametype in list(labels.keys()):
        _wavs = []
        wavs_duration = []
        for (_,_,filenames) in walk(folder+nametype+"/"):
            _wavs.extend(filenames)
            break
        Mel_Spectrogram = []
        for _wav in _wavs:
            if(".wav" in _wav): 
                file = folder +nametype+"/"+_wav
                print ("-"+file)
                signal, rate = librosa.load(file)  
                S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
                S_DB = librosa.power_to_db(S, ref=np.max)
                S_DB = S_DB.flatten()[:1200]
                a.append(S_DB)
                b.append(labels[nametype])
                
    return a, b

def getPrediction(soundfile,clf):
	hop_length = 512
	n_fft = 2048
	n_mels = 128
	types = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}   
	signal, rate = librosa.load(soundfile)  
	S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
	S_DB = librosa.power_to_db(S, ref=np.max)
	S_DB = S_DB.flatten()[:1200]
	y_pred = clf.predict([S_DB])[0]

	return types[y_pred]  
	
@app.route("/")
def home():
	return "Hello !!"
	
@app.route("/prediction/", methods=["POST"])
def prediction():

	requestedData = request.get_json()
	cible = open("cible.wav", "wb")
	receivedFile=requestedData["file"]
	decodedFile = base64.b64decode(receivedFile.encode("utf-8"))
	cible.write(decodedFile)

	folder = "./datasetaudio/"
	a, b = extractMelSpectrogram_features(folder)

	clf = svm.SVC()
	clf = svm.SVC(kernel="rbf")
	clf.fit(a,b)	

	y = getPrediction("cible.wav",clf)

	return "************* Genre of file : " + y +" *************\n"

		
		
if __name__ == '__main__':
   app.run(debug=True, port=5050, host='0.0.0.0')
