import subprocess
import time
import json
import os

# get home directory
homedir = os.path.expanduser('~')

#copy black theme to plank themes path
subprocess.call('cp '+homedir+'/max_plank/dock.theme '+homedir+'/.local/share/plank/themes/Black/dock.theme',shell=True)

while True:
    try:
        # get list of open windows
        windows_list = str(subprocess.check_output('wmctrl -l',shell=True)).split('\\n')
        windows = []
        for item in windows_list:
            windows.append(item.split(' ')[0])
        # see if any of them is maximized
        for window in windows:
            try:
                if not window.startswith('0x'):
                    window = window[2:]
                if window.startswith('0x'):
                    window_state = str(subprocess.check_output('xprop -id '+window,shell=True))
                    if '_NET_WM_STATE_MAXIMIZED_HORZ, _NET_WM_STATE_MAXIMIZED_VERT' in window_state and 'window state: Iconic' not in window_state:
                        maximized = 1
                        break
                    else:
                        maximized = 0
            except:
                pass
    except:
        maximized = 0

    # store previous plank config
    theme = str(subprocess.check_output('dconf read /net/launchpad/plank/docks/dock1/theme',shell=True)).split("'")[1]
    pos = str(subprocess.check_output('dconf read /net/launchpad/plank/docks/dock1/alignment',shell=True)).split("'")[1]
    try:
        with open(homedir+'/.config/plank/settings.json','r') as file:
            plank_settings = json.load(file)
    except:
        plank_settings = {'theme':theme,'pos':pos}
    if 'Black' not in theme:
        with open(homedir+'/.config/plank/settings.json','w') as file:
            json.dump(plank_settings,file)

    # change dconf based on maximized state
    if not maximized:
        subprocess.call('dconf write /net/launchpad/plank/docks/dock1/theme \"\''+plank_settings['theme']+'\'\"',shell=True)
        subprocess.call('dconf write /net/launchpad/plank/docks/dock1/alignment \"\''+plank_settings['pos']+'\'\"',shell=True)
    else:
        subprocess.call('dconf write /net/launchpad/plank/docks/dock1/theme \"\'Black\'\"',shell=True)
        subprocess.call('dconf write /net/launchpad/plank/docks/dock1/alignment \"\'fill\'\"',shell=True)
    time.sleep(.1)
