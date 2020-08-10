import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import urllib
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
import time
import datetime
from time import strftime
import applescript
import subprocess
import aiml
import Alfred

lastCommand = ""
isActive = True
requireAlfred = False
followUp = False
positive = []
negative = []
confirmations = []
notCommands = []

def myCommand():
    global isActive
    global followUp
    followUp = False
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if isActive == True or requireAlfred == True:
            print('Say something...')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        if isActive == True or requireAlfred == True:
            print('You said: ' + command + '\n')
        lastCommand = command
#loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        if isActive == True or requireAlfred == True:
            print('....')
        command = myCommand();
    return command
    
def leroyResponse(audio):
    print(audio)
    for char in audio.splitlines():
        os.system("say -v Daniel '[[rate 210]] '" + audio)

def kernelResponse(command):
    alfredResponse = kernel.respond(command)
    leroyResponse(alfredResponse)
            
def recentCommand():
    return lastCommand
        
def assistant(command):
    global isActive
    global requireAlfred
    global positive
    global negative
    global confirmations
    global followUp
    
    if 'alfred' in command:
        isActive = True
    
    if isActive == True and requireAlfred == False or 'alfred' in command:
        if 'open' in command or 'pull up' in command:
            string = command.replace("open ", "")
            leroyResponse('what do you want the key word to be called')
            keycode = myCommand()
            for word in string.split():
                word.capitalize()
            print(string)
            applescript.AppleScript("tell application \"" + string + "\" to activate").run()
            f = open('/Users/kalp/Alfred/Alfred.py', 'r')
            data = f.read()
            f.close()
            data = data.replace("""elif 'open' in command or 'pull up' in command:
            if followUp == False:
                leroyResponse(random.choice(confirmations))
            if""", """elif 'open' in command or 'pull up' in command:
            if followUp == False:
                leroyResponse(random.choice(confirmations))
            if \'%s\' in command:
                apple(\"""tell application \"%s\" to activate\""")
                followUp = True
                command = command.replace('%s', '')
                assistant(command)
            elif""" % (keycode, string, keycode))
            f = open('/Users/kalp/Alfred/Alfred.py', 'w')
            f.write(data)
            f.close()
            leroyResponse('Command added sir')
            os.system("python Alfred.py")
            sys.exit()
#                except:
#                    print(".")
            leroyResponse('No program as such exists sir')
        elif 'play' in command:
            if 'song' in command:
                leroyResponse('Which song would you like me to play sir?')
                answer = myCommand()
                try:
                    applescript.AppleScript("""tell application "Music" to activate""").run()
                    applescript.AppleScript("""tell application "Music" to play """ + answer).run()
                except:
                    leroyResponse('You have not downloaded that song sir. Would you still like me to play a song.')
                    answer = myCommand()
                    if any(word in answer for word in positive):
                        assistant('play a song')
                    else:
                        leroyResponse(random.choice(confirmations))
        elif 'time' in command:
            now = datetime.datetime.now()
            timeOfDay = "a.m."
            if now.hour > 12:
                newHour = now.hour - 12
                timeOfDay = "p.m."
            else:
                newHour = now.hour
            if now.minute == 0:
                minuteText = ""
            elif now.minute < 10:
                minuteText = "o " + str(now.minute)
            else:
                minuteText = "" + str(now.minute)
            leroyResponse('Currently, it is %d %s %s\n' % (newHour, minuteText, timeOfDay))
        elif 'send' in command:
            if 'message' in command:
                if 'darsh' in command:
                    leroyResponse('What would you like the message to be sir')
                    message = myCommand()
                    applescript.AppleScript("""tell application "Messages"
    send """ + message + """ to buddy "Darsh"
    quit
end tell""").run()
                    leroyResponse('Message has been sent')
                else:
                    leroyResponse('Who would you like to send the message too?')
                    assistant(myCommand() + 'send message')
        elif 'unread' in command:
            if 'mail' in command:
                leroyResponse('One moment sir')
                unread = applescript.AppleScript("""tell application "Mail"
    set a to 0
    repeat with theAccount in (every account)
        repeat with theBox in (every mailbox of theAccount)
            set a to a + (count (messages in theBox where read status is false))
        end repeat
    end repeat
    quit
end tell
return a""").run()
                leroyResponse('You have ' + str(unread) + ' unread e mails sir')
        elif any(phrase == command for phrase in notCommands):
            leroyResponse('')
        else:
            if followUp == False:
                leroyResponse('I am not sure how to answer that, would you like me to add it to future commands list?')
                answer = myCommand()
                if 'again' in answer:
                    leroyResponse('What is the command sir?')
                    assistant(myCommand())
                elif any(word in answer for word in positive):
                    leroyResponse(random.choice(confirmations))
                    f = open('/Users/kalp/Alfred/FutureCommands.txt', 'a')
                    f.write(command + '\n\n')
                    f.close()
                    leroyResponse('Command has been noted sir.')
                    os.system("python Alfred.py")
                    sys.exit()
                elif any(word in answer for word in negative):
                    leroyResponse(random.choice(confirmations))
                    os.system("python Alfred.py")
                    sys.exit()

f = open('/Users/kalp/Alfred/Setup/Positive.txt', 'r')
data = f.read()
for line in data.splitlines():
    positive.append(line)
f.close()

f = open('/Users/kalp/Alfred/Setup/Negative.txt', 'r')
data = f.read()
for line in data.splitlines():
    negative.append(line)
f.close()

f = open('/Users/kalp/Alfred/Setup/Confirmations.txt', 'r')
data = f.read()
for line in data.splitlines():
    confirmations.append(line)
f.close()

f = open('/Users/kalp/Alfred/Setup/NotCommands.txt', 'r')
data = f.read()
for line in data.splitlines():
    notCommands.append(line)
f.close()

leroyResponse('What is the command sir?')

while True:
    assistant(myCommand())
