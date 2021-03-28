# Comments

import notify

def beep(tune=False, freq = 600, duration = .1):

    # 'play' requires: brew install sox
    
    import os
    cmd_play = os.popen('find / -name play -print -quit 2> /dev/null').read().strip()
    duration = duration  # second
    freq = freq  # Hz
    if tune:
        for i in [1,2,1.2,1.5]:
            os.system(f'{cmd_play} --no-show-progress --null --channels 2 synth {duration} sine {freq / i}')
    else:
        os.system(f'{cmd_play} --no-show-progress --null --channels 2 synth {duration} sine {freq}')
        

def prowl_notify(event = 'Done!', app = 'Prowl', beep = False):
    import requests
    from requests.exceptions import HTTPError

    import json
    from pathlib import Path
    
    home = str(Path.home())

    prowl_url = 'https://api.prowlapp.com/publicapi/add'

    try:
        with open(home + '/.keys/.prowl') as f:
            key = f.readline().strip()
            if key == '[Enter API Key]':
                print('Error: API Key missing at ~/.keys/.prowl')
                return
                
        d_data = {
            'apikey': key,
            'application': app,
            'event': event
        }

        req = requests.post(prowl_url,d_data)
        if req.status_code != 200:
            print('Error: Check URL and API Key at ~/.keys/.prowl')


    except FileNotFoundError:
        print('Error: Config file missing at ~/.keys/.prowl')
    except HTTPError:
        print('Error: Check URL and API Key at ~/.keys/.prowl')

    if beep:
        notify.beep()