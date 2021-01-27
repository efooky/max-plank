import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gdk
import time
import threading
import subprocess
import os
import json

# plank em outras posiçoes
# ler config durante operacao

homedir = os.path.expanduser('~')
previous = None
resolution = {'hor':0,'ver':0}
config = {'delay':600,'transition':150,'min_opacity':0.1,'max_opacity':0.9}
try:
    with open(homedir+'/.config/max-plank/config.json','r') as config_f:
        config_n = json.load(config_f)
    for item in config_n:
        config[item] = float(config_n[item])
        print(config[item])
    config['delay'] = int(config['delay'])
    config['transition'] = int(config['transition'])
    print('Config:',config)
except Exception as e:
    print(e)
    subprocess.call('mkdir '+homedir+'/.config/max-plank',shell=True)
with open(homedir+'/.config/max-plank/config.json','w') as config_f:
    json.dump(config,config_f)
delay = config['delay']/1000

win = Gtk.Window()
#win.connect("destroy", Gtk.main_quit)
win.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("black"))
win.set_default_size(1366,100) # ver tamanho plank,loop
win.set_keep_below(True)
win.set_decorated(False)
win.set_type_hint(Gdk.WindowTypeHint.DOCK)
win.show_all()
win.set_opacity(0)

def update(maximized):
    # definir opacidade minima e maxima
    try:
        min_opacity = config['min_opacity']
        max_opacity = config['max_opacity']
        n = 5
        t = config['transition']/1000
        step = (max_opacity-min_opacity)/n
        step_time = t/n
        if maximized:
            opacity = min_opacity
            while opacity<max_opacity:
                opacity += step
                print('Opacity:',opacity)
                win.set_opacity(opacity)
                time.sleep(step_time)
            win.set_opacity(max_opacity)
        else:
            opacity = max_opacity
            while opacity>min_opacity:
                opacity -= step
                print('Opacity:',opacity)
                win.set_opacity(opacity)
                time.sleep(step_time)
            win.set_opacity(min_opacity)
    except Exception as e:
        print(e)

def check():
    global previous, resolution, config
    try:
        theme = str(subprocess.check_output('dconf read /net/launchpad/plank/docks/dock1/theme',shell=True)).split("'")[1]
        with open(homedir+'/.local/share/plank/themes/'+theme+'/dock.theme','r') as theme_file:
            content = theme_file.read()
            top = ''
            bottom = ''
            for line in content.splitlines():
                if 'TopPadding' in line:
                    top = line.split('=')[1]
                if 'BottomPadding' in line:
                    bottom = line.split('=')[1]
                if len(top)>0 and len(bottom)>0:
                    top=float(top)
                    bottom=float(bottom)
                    if top<0:
                        top=0
                    if bottom<0:
                        bottom=0
                    break
        icon_size = int(subprocess.check_output('dconf read /net/launchpad/plank/docks/dock1/icon-size',shell=True))
        height = icon_size+icon_size*top/10+icon_size*bottom/10
        res = str(subprocess.check_output("xdpyinfo | grep dimensions",shell=True)).split()[2]
        res = str(res).split('x')
        #print('res:',res)
        hor = int(res[0])
        ver = int(res[1])
        if ver != resolution['ver']:
            win.move(0,ver-height)
        resolution = {'hor':hor,'ver':ver}
    except Exception as e:
        print('erro res:',e)
    maximized = 0
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
                    try:
                        state1 = str(subprocess.check_output('xprop -id '+window+' | grep _NET_WM_STATE_MAXIMIZED_VERT',shell=True))
                    except:
                        state1 = ''
                    try:
                        state2 = str(subprocess.check_output('xprop -id '+window+' | grep Iconic',shell=True))
                    except:
                        state2 = ''
                    maximized = 0
                    if len(state1)>0 and len(state2)==0:
                        maximized = 1
                        break
            except Exception as e:
                print(e)
    except Exception as e:
        print('erro maximized',e)
        maximized = 0
    if previous is None:
        win.set_opacity(config['min_opacity'])
        previous = 0
    if maximized != previous:
        print('Maximized:',maximized)
        update(maximized)
    previous = maximized
    tr = threading.Timer(config['delay']/1000,check)
    tr.start()
    #time.sleep(0.6)
    #check()

tr = threading.Timer(1,check)
tr.start()
Gtk.main()
