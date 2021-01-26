# max-plank

This script is designed to be used in Elementary OS. It draws a black background under the dock when there is a maximized window.

Installation:
1) Clone this repository to ~/max-plank.
2) Run the following command to start Max Plank:
  sh ~/max-plank/max-plank.sh
3) To run max-plank in your system startup, open System Settings > Applications > Startup > Add Startup App..., and type this in the custom command field:
  sh ~/max-plank/max-plank.sh

If you notice it's taking too much CPU usage, you can change the last line of max-plank.py from time.sleep(.1) to time.sleep(.5) or time.sleep(.8). This is the time interval Max Plank will wait until checking if there are maximized windows.

Have fun, and let me know if there's any problem!
