#!/usr/bin/env python3
import sys, os, argparse
from shutil import copy2
from filecmp import cmp as compare
from time import sleep

class Playlist(list):
    def __init__(self, infile_name):
        try:
            print('INFO: reading playlist from %s.' % infile_name)
            infile = open(infile_name)
        except:
            msg = 'FATAL error: could not open '+ infile_name
            exit(msg)
        try:
            for line in infile.readlines():
                if not line.startswith('#'):
                    self.append(line.rstrip())
        except SystemExit as err:
            exit(str(err))
        except:
            msg = 'FATAL ERROR: could not read playlist file.'
            exit(msg)   
        finally:
            print('INFO: closing playlist file.')
            infile.close()

    def _copyfile(self, ifn, ofn):
        if not os.path.exists(os.path.dirname(ofn)):
            try:
                print('INFO: making destination folder',
                      os.path.dirname(ofn))
                os.makedirs(os.path.dirname(ofn))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if os.path.exists(ofn):
            if compare(ifn, ofn):  # do nothing if output file already same as input
                print('INFO: file already exists. %s' % ofn)
                return
            elif (os.path.getmtime(ifn) < os.path.getmtime(ofn)):
                print('INFO: not copying over newer file.')
                print('INFO: %s is newer than %s' % (ofn, ifn))
            else:
                pass
        else:
            try:
                print('INFO: Copying %s \n\t to %s' % (ifn, ofn))
                copy2(ifn, ofn)
            except:
                print('WARNING: could not copy %s \n\t to %s' % (ifn, ofn))

    def copyfiles(self, target, source, first=1, last=0):
        ofn = str('')         # output file name
        ifn = str('')         # input file name
        discard = len(source)
        if (last < first):
            last = len(self)  # default to processing all of list
        try:
            if os.path.isdir(target):
                for ifn in self[first:last]:
                    if ifn.startswith(source):
                        ofn = target + ifn[discard:] # strips source directory
                        self._copyfile(ifn, ofn)
                    else:
                        print('INFO: file is not in source directory.')
                        print('INFO: skipping file %s.' % ifn)
            else:
                msg = 'FATAL ERROR: Target directory does not exist %s' % target
                raise IOError(msg)
        except IOError as err:
            print(str(err))
        finally:
            pass
        return

    def guess_source(self):
        common_start = self[0]
        def _iter(s1, s2):
            for a, b, in zip(s1, s2):
                if a == b:
                    yield a
                else:
                    return

        for i in range(len(self)):
            common_start = ''.join(_iter(self[i], common_start))
        return common_start
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='./musicsync.py',
                description='sync music from library to device using an m3u playlist')
    parser.add_argument('-if', '--infile', type=str, default='playlist.m3u',
                        metavar='<file name>',
                        help='input file, an m3u playlist, defaults to playlist.m3u')
    parser.add_argument('-t', '--target', type=str, default='./Copiedfiles/',
                        metavar='<directory name>',
                        help='target, path to a directory defaults to ./Copiedfiles/')
    parser.add_argument('-s', '--source', type=str, 
                        metavar='<directory name>',
                        help='source, path to a directory, a good default is guessed')
    args = parser.parse_args()

    infile = args.infile
    if args.target.endswith('/'):
        target = args.target
    else:
        target = args.target + '/'
    print('INFO: target directory is %s' % target)
    playlist = Playlist(infile)
    if args.source:
        if args.source.endswith('/'):
            source = args.source
        else:
            source = args.source + '/'
    else:
        source = playlist.guess_source()
    print('INFO: source is %s,' % source)
    print('INFO: path to source will be ignored when creating sub directories in target')


    playlist.copyfiles(target, source, 0, 10)
