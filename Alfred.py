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
import UpdateAlfred

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
    
def apple(string):
    applescript.AppleScript(string).run()
        
def assistant(command):
    global lastCommand
    global isActive
    global requireAlfred
    global positive
    global negative
    global confirmations
    global followUp
    
    if 'alfred' in command:
        isActive = True
    
    if isActive == True and requireAlfred == False or 'alfred' in command:
        if 'system' in command and 'deactivate' in command:
            leroyResponse('Bye Sir. Have a good day.')
            sys.exit()
        elif 'standby' in command:
            leroyResponse('Standing by until further notice sir')
            isActive = False
        elif 'require alfred' in command: 
            if 'deactivate require alfred' in command or 'turn off require alfred' in command or 'disable require alfred' in command:
                if requireAlfred == True:
                    requireAlfred = False
                    leroyResponse('Deactivated require alfred')
                else:
                    leroyResponse('Require alfred is alrady inactive.')
            elif 'activate require alfred' in command or 'turn on require alfred' in command or 'initiate require alfred' in command or 'enable require alfred' in command:
                if requireAlfred == False:
                    requireAlfred = True
                    leroyResponse('Activated require Alfred.')
                else:
                    leroyResponse('Require alfred is already active.')
        elif 'everything' in command or 'all' in command:
            if 'close' in command or 'quit' in command:
                leroyResponse('Are you sure sir?')
                answer = myCommand()
                if any(word in answer for word in negative):
                    leroyResponse(choice.random(confirmations))
                elif any(word in answer for word in positive):
                    apple("""tell application "System Events" to set quitapps to name of every application process whose visible is true and name is not "Terminal"
repeat with closeall in quitapps
    quit application closeall
end repeat""")
                followUp = True
                assistant(answer)
        elif 'open' in command or 'pull up' in command:
            if followUp == False:
                leroyResponse(random.choice(confirmations))
            if 'unity' in command:
                apple("""tell application "unity hub" to activate""")
                followUp = True
                command = command.replace('unity', '')
                assistant(command)
            elif 'chrome' in command:
                apple("""tell application "google chrome" to activate""")
                followUp = True
                command = command.replace('chrome', '')
                assistant(command)
            elif 'photos' in command:
                apple("""tell application "photos" to activate""")
                followUp = True
                command = command.replace('photos', '')
                assistant(command)
            elif 'chess' in command:
                apple("""tell application "chess" to activate""")
                followUp = True
                command = command.replace('chess', '')
                assistant(command)
            elif 'calendar' in command:
                apple("""tell application "Calendar" to activate""")
                followUp = True
                command = command.replace('calendar', '')
                assistant(command)
            elif 'safari' in command:
                apple("""tell application "Safari" to activate""")
                followUp = True
                command = command.replace('safari', '')
                assistant(command)
            elif 'code' in command:
                apple("""tell application "Visual Studio Code" to activate""")
                followUp = True
                command = command.replace('code', '')
                assistant(command)
            elif 'messages' in command:
                apple("""tell application "Messages" to activate""")
                followUp = True
                command = command.replace('messages', '')
                assistant(command)
            elif 'rpg project' in command:
                apple("""open file "Macintosh HD/Users/kalp/Documents/VSCode/RPGGame/FirstTry.java" """)
                followUp = True
                command = command.replace('rpg', '')
                assistant(command)
            elif 'music' in command or 'itunes' in command:
                apple("""tell application "Music" to activate""")
                followUp = True
                command = command.replace('music', '')
                assistant(command)
            elif 'mail' in command:
                apple("""tell application "Mail" to activate""")
                followUp = True
                command = command.replace('mail', '')
                assistant(command)
            elif followUp == False:
                assistant('')
        elif 'play' in command:
            if 'song' in command:
                if 'next' in command:
                    apple("tell application \"Music\" to play next track")
                elif 'previous' in command:
                    apple("tell application \"Music\" to play previous track")
                else:
                    leroyResponse('Which song would you like me to play sir?')
                    answer = myCommand()
                    try:
                        apple("""tell application "Music" to activate""")
                        apple("""tell application "Music" to play track \"%s\"""" % (answer))
                    except:
                        leroyResponse('You have not downloaded that song sir. Would you still like me to play a song.')
                        answer = myCommand()
                        if any(word in answer for word in positive):
                            assistant('play a song')
                        else:
                            leroyResponse(random.choice(confirmations))
        elif 'your name' in command:
            leroyResponse('My name is Alfred sir.')
        elif 'meet alfred' in command:
            leroyResponse('Hello there. How are you doing?')
            response = myCommand()
            if any(word in response for word in positive):
                leroyResponse("That is good to hear.")
            elif any(word in response for word in negative):
                leroyResponse("That is not very good.")
            else:
                leroyResponse("Alright, lets just ignore my question then.")
                assistant(response)
        elif 'empty' in command and 'trash' in command:
            leroyResponse(random.choice(confirmations))
            apple("""tell application "Finder" empty trash""")
        elif ' time' in command or 'time ' in command:
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
        elif 'go to sleep' in command:
            leroyResponse(random.choice(confirmations))
            isActive = False
            os.system("osascript -e 'tell application \"Finder\" to sleep'")
        elif 'shut up' in command:
            leroyResponse('That. was uncalled for.')
            assistant('alfred standby')
        elif 'note' in command or 'jot' in command or 'create' in command:
            leroyResponse('What do you wish to call the file?')
            fileName = myCommand()
            fileName.replace(' ', '')
            leroyResponse('What would you like your message to be?')
            message = myCommand()
            message = message.replace('next line ', '\n')
            message.capitalize()
            leroyResponse('Where would you like to save your file sir?')
            location = myCommand()
            location = location.replace(" slash ", "/")
            location = location.replace(" ", "")
            for word in location.split():
                word.capitalize()
            f = open('/Users/kalp/' + location + '/' + fileName + '.txt', 'a')
            f.write(message + '\n\n')
            leroyResponse('Message has been noted sir.')
        elif 'send' in command:
            if 'message' in command:
                if 'darsh' in command:
                    leroyResponse('What would you like the message to be sir')
                    message = myCommand()
                    apple("""tell application "Messages"
    send """ + message + """ to buddy "Darsh"
    quit
end tell""")
                    leroyResponse('Message has been sent')
                else:
                    leroyResponse('Who would you like to send the message too?')
                    assistant(myCommand() + 'send message')
            elif 'mail' in command:
                if 'darsh' in command:
                    leroyResponse('What would you like the subject to be?')
                    subject = myCommand()
                    leroyResponse('What would you like the message to read?')
                    content = myCommand()
                    if content == 'nothing' or 'blank' in content:
                        content = ''
                    apple("""tell application "Mail"
    set theFrom to "Kalp Shah"
    set theTos to {"darshshah2000@gmail.com"}
    set theSubject to "%s"
    set theContent to "%s"
    set theAttachments to {}
    set theDelay to 1
    set theMessage to make new outgoing message with properties {sender:theFrom, subject:theSubject, content:theContent, visible:false}
    tell theMessage
        repeat with theTo in theTos
            make new recipient at end of to recipients with properties {address:theTo}
        end repeat
        repeat with theAttachment in theAttachments
            make new attachment with properties {file name:theAttachment as alias} at after last paragraph
            delay theDelay
        end repeat
    end tell
    send theMessage
    quit
end tell""" % (subject, content))
        elif 'unread' in command:
            if 'mail' in command:
                leroyResponse('One moment sir')
                unread = apple("""tell application "Mail"
    set a to 0
    repeat with theAccount in (every account)
        repeat with theBox in (every mailbox of theAccount)
            set a to a + (count (messages in theBox where read status is false))
        end repeat
    end repeat
    quit
end tell
return a""")
                leroyResponse('You have ' + str(unread) + ' unread e mails sir')
        elif 'google' in command or 'search' in command or 'look up' in command:
            leroyResponse(random.choice(confirmations))
            search = command
            search = search.replace('alfred', '')
            search = search.replace('google', '')
            search = search.replace('search for', '')
            search = search.replace('search', '')
            search = search.replace('look up', '')
            search = search.replace(' ', '+')
            apple("""do shell script "open -a Safari 'http://www.google.com/search?client=safari&rls=en&q=%s&ie=UTF-8&oe=UTF-8'\"""" % (search))
        elif 'turn' in command:
            if 'on' in command:
                if 'tv' in command:
                    leroyResponse(random.choice(confirmations))
                    apple("""tell application "System Preferences"
    set current pane to pane "com.apple.preference.displays"
    activate
end tell
tell application "System Events"
    tell process "System Preferences"
        click pop up button 1 of window 1
        click menu item 3 of menu 1 of pop up button 1 of window 1
        delay 1
        click pop up button 1 of window 1
        click menu item 1 of menu 1 of pop up button 1 of window 1
    end tell
end tell
tell application "System Preferences"
    quit
end tell""")
        elif 'solve' in command or 'calculate' in command or 'answer' in command:
            if 'quadratic' in command:
                leroyResponse('What is the first coefficient')
                a = int(myCommand())
                leroyResponse('What is the second coefficient')
                b = int(myCommand())
                leroyResponse('What is the third coefficient')
                c = int(myCommand())
                try:
                    quad_ans1 = (-b + (b**2 - 4*a*c)**0.5)/2*a
                    if quad_ans1 < 0:
                        answer1 = "negative " + str(quad_ans1 * -1)
                    else:
                        answer1 = str(quad_ans1)
                except ValueError:
                    answer1 = "non-existent"
                try:
                    quad_ans2 = (-b - (b**2 - 4*a*c)**0.5)/2*a
                    if quad_ans1 < 0:
                        answer2 = "negative " + str(quad_ans2 * -1)
                    else:
                        answer2 = str(quad_ans2)
                except ValueError:
                    answer2 = "non-existent"
                if answer1 != answer2:
                    leroyResponse('The first answer is ' + answer1 + ' and the second answer is ' + answer2)
                else:
                    leroyResponse('Both answers are ' + answer1)
            else:
                digit = False
                question = command
                question = question.replace('solve', '')
                question = question.replace('calculate', '')
                question = question.replace('times', ' * ')
                question = question.replace('divided by', ' / ')
                question = question.replace('open bracket', '(')
                question = question.replace('close bracket', ')')
                question = question.replace('equal', '')
                question = question.replace('equals what', '')
                for character in command:
                    if character.isdigit():
                        digit = True
                    else:
                        command.replace(character + ' ', '')
                if digit == True:
                    try:
                        answer = apple(question)
                        leroyResponse('The answer to that equation is ' + answer + ' sir.')
                    except:
                        leroyResponse('Something went wrong sir')
                        assistant('calculate')
                else:
                    leroyResponse('What would you like me to calculate sir?')
        elif 'louder' in command or 'too quiet' in command or 'quieter' in command or 'too loud' in command or 'volume' in command:
            leroyResponse('What percentage would you like to set the volume too?')
            volumeSet = myCommand()
            volumeSet = volumeSet.replace('%', '')
            apple("set volume output volume " + volumeSet)
            leroyResponse('Is this better sir?')
            answer = myCommand()
            if any(word in answer for word in negative):
                assistant('volume')
            elif any(word in answer for word in positive):
                leroyResponse(random.choice(confirmations))
        elif command == 'alfred':
            leroyResponse('Yes Sir.')
        elif 'not' in command and 'command' in command:
            f = open('/Users/kalp/Alfred/Setup/NotCommands.txt', 'a')
            f.write('\n' + lastCommand)
            f.close()
            if followUp == True:
                leroyResponse(random.choice(confirmations))
            else:
                leroyResponse('Added to not commands.')
        elif any(phrase == command for phrase in notCommands):
            leroyResponse('')
        elif followUp == False:
            if kernel.respond(command) != '':
                kernelResponse(command)
            else:
                leroyResponse('Wait. I am not sure how to answer that, would you like me to add this command sir?')
                answer = myCommand()
                if any(word in answer for word in positive):
                    leroyResponse(random.choice(confirmations))
                    os.system("python UpdateAlfred.py")
                elif any(word in answer for word in negative):
                    leroyResponse(random.choice(confirmations))
                    followUp = True
                    assistant(answer)
                    lastCommand = command
        
kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")

#leroyResponse('Booting up sir, one moment please.')

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

leroyResponse('Ready sir. Alfred at your service')

while True:
    assistant(myCommand())
    
#leroyResponse(random.choice(confirmations))
#command = command.replace("open", "")
#command = command.replace("and", "")
#command = command.replace("in", "")
#for word in command.split():
#    try:
#        word = word.replace("code", "Visual Studio Code")
#        word = word.replace("messenger", "All-in-One Messenger")
#        word = word.replace("chrome", "Google Chrome")
#        applescript.AppleScript("tell application \"" + word.capitalize() + "\" to activate").run()
#    except:
#        print("")
