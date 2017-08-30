#!/usr/bin/env python3
import sys
import os

class Playlist(list):
    def __init__(self, infile_name):
        try:
            infile = open(infile_name)
        except:
            msg = 'could not open '+ infile_name
            exit(msg)
        for line in infile.readlines():
            if not line.startswith('#'):
                self.append(line.rstrip())
            
    def copyfiles(self, target, first=1, last=0):
        try:
            if os.path.isdir(target):
                for fn in self[first:last]:
                    print(fn)
                pass
            else:
                msg = 'FATAL ERROR: Target directory %s does not exist' % target
                raise IOError(msg)
        except IOError as err:
            print(str(err))
        finally:
            pass
        return
    
if __name__ == "__main__":
    print("Running with defaults is better than running with knives")
    infile_name = "playlist.m3u"
    target = "./Copiedfiles"
    playlist = Playlist(infile_name)
#    for line in playlist[0:9]:
#        print(line)
    playlist.copyfiles(target, 0, 9)
