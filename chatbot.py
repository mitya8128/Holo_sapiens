from chatterbot import ChatBot
from gtts import gTTS
import os
import pygame
from pygame.locals import *
import speech_recognition as sr
import string
import random
import time
import requests
from os import startfile

chatbot_2 = ChatBot('holo_chatbot2', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

chatbot_2.train('chatterbot.corpus.english')


# unique filename
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# kill process
def kill_by_process_name_shell(name):
    os.system("taskkill /f /im " + name)


def play_movie(path):
    startfile(path)
    time.sleep(10)
    kill_by_process_name_shell('mplayerc.exe')


# get response
def get_chatbot_response(text):
    text = input()
    response = chatbot_2.get_response(text)
    response_str = str(response)
    tts = gTTS(text=response_str, lang='en-us', slow=False)
    file_name = str(id_generator(6))  # unique filename
    file = tts.save('%s.mp3' % file_name)
    print(response_str)
    pygame.mixer.init()
    # pygame.mixer.music.load('%s.mp3' % file_name)
    pygame.mixer.music.load('%s.mp3' % file_name)
    pygame.mixer.music.play()
    # play_movie('conversation.mp4')


# get response through voice recognition
def get_chatbot_response2(rec_text):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('chatbot is listening')
        audio = r.listen(source)
    rec_text = r.recognize_google(audio)
    print(rec_text)
    '''
     try:
            result = recognizer_function(audio)                               #TODO:exceptions worker
            return Statement(result)
        except speech_recognition.UnknownValueError:
            return Statement('I am sorry, I could not understand that.')
        except speech_recognition.RequestError as e:
            m = 'My speech recognition service has failed. {0}'
            return Statement(m.format(e))
    '''
    response = chatbot_2.get_response(rec_text)
    response_str = str(response)
    tts = gTTS(text=response_str, lang='en-us', slow=False)
    file_name = str(id_generator(6))
    file = tts.save('%s.mp3' % file_name)
    print(response_str)
    pygame.mixer.init()
    pygame.mixer.music.load('%s.mp3' % file_name)
    pygame.mixer.music.play()
    # play_movie('conversation.mp4')


# check internet connection

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


# typing scenario
def get_response():
    if connected_to_internet() is True:
        get_chatbot_response('enter')
        # get_chatbot_response2('rec_text')
    if connected_to_internet() is False:
        pygame.mixer.init()
        pygame.mixer.music.load("Tell me about your self.mp3")
        pygame.mixer.music.play()


# voice recognition scenario
def v():
    if connected_to_internet() is True:
        # get_chatbot_response('enter')
        get_chatbot_response2('rec_text')
    if connected_to_internet() is False:
        pygame.mixer.init()
        pygame.mixer.music.load("Tell me about your self.mp3")
        pygame.mixer.music.play()


while True:
    try:
        get_response()
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
