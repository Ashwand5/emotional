from django.shortcuts import render, redirect,HttpResponse
from requests.adapters import HTTPAdapter
from django.contrib.auth.models import User, auth
from urllib3.util.retry import Retry
from django.core.files.storage import default_storage
import requests
import os
from django.conf import settings

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('signup')
    return render(request, 'login.html')
#
#
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pass = request.POST['confirmpass']
        if password == confirm_pass:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        print(username)
    return render(request, 'signup.html')




from django.shortcuts import render

from django.shortcuts import render

from django.conf import settings
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == 'POST' or request.method == 'GET':
        print("POST request received")
        print(request.FILES)
        if 'audio-input' in request.FILES:
            print("File received")
            audio = request.FILES['audio-input']
            fs = FileSystemStorage()
            audio_path = fs.save(audio.name, audio)
            audio_path = fs.path(audio_path)
            audio_emotion = audio_model(audio_path)
            return render(request, 'home.html', {'audio_emotion': audio_emotion})
        if request.method == 'GET':
            text = request.GET.get('text-input')
            print(f'Received text: {text}')
            if text:
                text_emotion = text_model(text)
                return render(request, 'home.html', {'text_emotion': text_emotion})
    return render(request, 'home.html')

    # elif 'audio-input' in request.GET:  # Change this to request.GET
        #     audio = request.GET['audio-input']  # Change this to request.GET
        #     audio_emotion = voice_model(audio)
        #     return render(request, 'home.html', {'audio_emotion': audio_emotion})



import pickle
from keras.models import load_model
import numpy as np
import librosa
import pandas as pd


with open('text_emotion.pkl','rb') as file:
    clf=pickle.load(file)
def text_model(text):
    print('text ode')
    labels = {0: 'sadness ', 1: 'joy', 2: 'love', 3: 'anger', 4: 'fear', 5: 'surprise'}
    prediction = clf.predict([text])
    return labels[prediction[0]]

def audio_model(audio):
    model = load_model("audio_emotion.h5")
    X_new = extract_mfcc(audio)
    X_new = np.expand_dims(np.expand_dims(X_new, axis=0), axis=-1)
    predictions = model.predict(X_new)
    emotion_labels = ['fear', 'angry', 'disgust', 'neutral', 'sad', 'pleasant suprise', 'happy']
    predicted_label_index = np.argmax(predictions)
    predicted_emotion = emotion_labels[predicted_label_index]
    return predicted_emotion

def extract_mfcc(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return mfcc
