# RhythmRemote

The goal of this project is to create a fully functional mobile web-interface for Rhythmbox.
It's implemented as an Rhythmbox plugin written in python. The plugin starts a local webserver
on 0.0.0.0:8001 (or localhost), which handles the requests of the browser.

## Screenshots
![Search interprets](https://raw.github.com/erti/rhythmbox-rhythmremote/master/screenshots/interprets.png "Search interprets")

![Play track](https://raw.github.com/erti/rhythmbox-rhythmremote/master/screenshots/play.png "Play tracks")

![Queue](https://raw.github.com/erti/rhythmbox-rhythmremote/master/screenshots/queue.png "Queue")

## Prerequisites

* Rhythmbox 3.1+
* Python 3
* Bottle (python module)
* Modern Webrowser (HTML5 enabled)

The plugin has been tested with Rhythmbox 3.1 on fedora 21 with Firefox 33.1 and a Nokia x7 smartphone.

## Installation

Simply run the python script make.py without arguments. The script will check the dependencies, 
create the plugin folder and symlink the plugin into that folder. Additionally it will start 
rhythmbox without debug output enabled for the plugin. It will also create a local schema directory
and file so that root priveledges are not needed to install the plugin in a users plugin directory.

If you want to install the plugin, run:

```bash
python3 make.py install
```

This will copy the plugin-files to ~/.local/share/rhythmbox/plugins/
and copy a schema file to ~/.local/glib-2.0/schemas/

The repository also includes an Eclipse-Project (with PyDev Extension) with configured Debug/Run configurations. 

## Functionality

### What is working

* Browsing the music-database in a very strict way (Interprets -> Albums -> Tracks)
* Browsing playlists
* Adding to queue and play the queue
* Choose single title to play
* Choose an album to play or add an album to the queue
* Play/Pause/Stop
* Previous/Next (if a playlist was chosen inside Rhythmbox)
* Adjust Volume
* Seek
