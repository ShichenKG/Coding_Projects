#########################################
# Shane Donivan
# PM Class
# Senior
# 9/10/21
# Text to Speech API
# A window to voice and say things aloud
##########################################


import requests, json, time, random, base64
import PySimpleGUI as sg

baseUrl = "https://api.voicerss.org/"

endpoint = "?key=10eedf43b3cf44568cdb0a03e6cc136b&hl=en-ca&c=MP3&f=16khz_16bit_stereo&src=Hello"

sendRequest = baseUrl + endpoint
print(sendRequest)
response = requests.get(sendRequest)
print(response.content)



"""

font = ['Comic Sans MS', 14]
keepPlaying = True

sg.theme('DarkAmber')
layout = [[sg.Text('Powered by James Rumsey',enable_events=True,font=(font),key='-Rumsey-')],
          [sg.Text('Text to Speech',relief='sunken',font=(font),enable_events=True, key='-text-', justification='center')],
          [sg.MLine(size=(60, 10), key='-Response-', reroute_stdout=True, auto_refresh=True,
                    do_not_clear=True,font=(font))],
          [sg.InputText(size=(54, 1),key='-Entry-',font=(font),focus=True),
           sg.Button('Submit',key='-Submit-',font=(font),bind_return_key=True)],
          [sg.StatusBar("This is my status bar",key='-stat-',font=(font))]]

window = sg.Window('Talk!', layout, size=(800,500),finalize=True)

while keepPlaying:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

"""