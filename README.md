MusicSync
=====
A simple python program that uses a m3u playlist to copy files from a source
folder (e.g. a music library to elsewhere (e.g. a device or another directory. 

Aim is to allow sync of selected files between library and device. Currently
device can be synched with library but not vice versa.

Usage
<pre>
musicsync.py [-h] [-if <file name>] [-t <directory path>] [-s <directory path>] 
[-q [True]] [-d [True]]

optional arguments:
  -h, --help      show this help message and exit
  -if <file path>, --infile <file path>
                  input file, an m3u playlist, defaults to playlist.m3u
  -t <directory path>, --target <directory path>
                  target, path to a directory defaults to ./Copiedfiles/
  -s <directory path>, --source <directory path>
                  source directory, a good default is guessed
  -q [True], --quick [True]
                  Do only a quick check for existing files
  -d [True], --delete [True]
                  Delete music files on target if not in playlist
</pre>
Notes
---
Can crash and burn if there a folders which differ only by letter case in the
library and the target device does not support case sensitive file paths. 

The source parameter is used to avoid adding the path to the library under the 
target directory. If no value for source is supplied, one will be guessed as the 
longest common string at the start of the paths of the files listed in the 
playlist. This will be removed from path for the files within the target 
directory. Depending on how you have files organised in the library and on your
device, this does not work well if all the files being copied are from the same 
subdriectory in the library. For example if you want your files organsied in 
subdirectories according to `<path>/<to>/<library>/<artist>/<album>/songname.ext`,
when copying just a single album, the artist and album folders will be removed 
as part of the common source. To avoid this supply the path to the library as
the source option.

The ```--quick``` or ```-q``` flag causes the programme to look only for files with the
same name in the target before skipping copying these. Without this option,
files with the same name will be checked to see whether they are different and
newer before before deciding to skip copying them. Difference is based on file
stat (not byte by byte comparison).

