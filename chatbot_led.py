
# coding: utf-8

# In[4]:

from chatterbot import ChatBot
from gtts import gTTS
import os
import pygame
from pygame.locals import *
import speech_recognition as sr
import serial


chatbot_test = ChatBot('holo_chatbot', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

#os.chdir(r'C:\\Users\\Admin\Desktop\\chatbot_test')

#THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#my_file = os.path.join(THIS_FOLDER, 'wittgenstein.yml')

#chatbot_test.train(my_file)

chatbot_test.train('chatterbot.corpus.english.conversations')

#объявляем устройство
ser = serial.Serial('/dev/tty.usbserial', 9600)

#функция, создающая уникальное имя файла
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


alphabet_colours = ('r','g','b','y','c','m')

def str_gen(alphabet_colours):
    for i in range(9):
        return random.choice(alphabet_colours)
        
#функция которая убивает процесс
def kill_by_process_name_shell(name):
    os.system("taskkill /f /im " + name)

import time

def play_movie(path):
    from os import startfile
    startfile(path)
    time.sleep(10)
    kill_by_process_name_shell('mplayerc.exe')

#получить ответ чатбота,напечатав вопрос
def get_chatbot_response(text):
    text = input()
    response = chatbot_test.get_response(text)
    response_str = str(response)
    tts = gTTS(text=response_str, lang='en-us', slow=False)
    file_name = str(id_generator(6))                   #добавить неповторяющееся имя файла  
    file = tts.save('%s.mp3' % file_name)
    print(response_str)
    pygame.mixer.init()
    #pygame.mixer.music.load('%s.mp3' % file_name)     
    pygame.mixer.music.load('%s.mp3' % file_name)
    pygame.mixer.music.play()
    #play_movie('conversation.mp4')

#получить ответ чатбота, задав вопрос голосом      
def get_chatbot_response2(rec_text):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('chatbot is listening')
        audio = r.listen(source)
    rec_text = r.recognize_google(audio)
    print(rec_text)
    '''
     try:
            result = recognizer_function(audio)                               #TODO:небольшой обработчик ошибок для распознавания речи
            return Statement(result)
        except speech_recognition.UnknownValueError:
            return Statement('I am sorry, I could not understand that.')
        except speech_recognition.RequestError as e:
            m = 'My speech recognition service has failed. {0}'
            return Statement(m.format(e))
    '''
    response = chatbot_test.get_response(rec_text)
    response_str = str(response)
    tts = gTTS(text=response_str, lang='en-us', slow=False)
    file_name = str(id_generator(6))                   #добавить неповторяющееся имя файла  
    file = tts.save('%s.mp3' % file_name)             
    print(response_str)
    pygame.mixer.init()
    pygame.mixer.music.load('%s.mp3' % file_name)     
    pygame.mixer.music.play()
    #play_movie('conversation.mp4')
    
#функция проверяющая наличие подключения к интернету
import requests

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

#нажатие клавиши пользователя в питоновской консоли
def get_response():
    if connected_to_internet() is True:
        get_chatbot_response('enter')
        #get_chatbot_response2('rec_text')
    if connected_to_internet() is False:
        pygame.mixer.init()
        pygame.mixer.music.load("Tell me about your self.mp3")     
        pygame.mixer.music.play()

#запустить голосовое распознавание вопроса
def v():
    if connected_to_internet() is True:
        #get_chatbot_response('enter')
        get_chatbot_response2('rec_text')
    if connected_to_internet() is False:
        pygame.mixer.init()
        pygame.mixer.music.load("Tell me about your self.mp3")     
        pygame.mixer.music.play()
        
        
while True:
    try:
        get_response()
        ser.write(str_gen(alphabet_colours))        #maybe ser.write(b'response_str')
    except (KeyboardInterrupt, EOFError, SystemExit):
        break