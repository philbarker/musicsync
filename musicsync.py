#!/usr/bin/env python3
import sys, os, argparse
from shutil import copy2
from filecmp import cmp as compare
from time import sleep

class Playlist(list):
    def __init__(self, infile_name):
        self.fn = infile_name
        self.t = './Copiedfiles/'
        self.s = ''
        self.q = False
        
        try:
            print('INFO: reading playlist from %s.' % self.fn)
            infile = open(self.fn)
        except:
            msg = 'FATAL error: could not open '+ self.fn
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

    def _copyfile(self, ifn, ofn, q):
        if not os.path.exists(os.path.dirname(ofn)):
            try:
                print('INFO: making destination folder',
                      os.path.dirname(ofn))
                os.makedirs(os.path.dirname(ofn))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if os.path.exists(ofn):
            if q: # skip if file exists with same name 
                print('INFO: file with name already exists %s' % ofn)
                return
            else:  # check file with same name, copy if source is diff & newer
                if compare(ifn, ofn):
                    # do nothing if output file already same as input
                    print('INFO: file already exists %s' % ofn)
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
            except Exception as e:
                if e.errno == 95: # raised becaused permission cannot be set 
                    pass
                else:
                    print('WARNING: could not copy %s \n\t to %s' % (ifn, ofn))
                    print(str(e))

    def copyfiles(self, first=1, last=0):
        ofn = str('')         # output file name
        ifn = str('')         # input file name
        discard = len(self.s)
        if (last < first):
            last = len(self)  # default to processing all of list
        try:
            if os.path.isdir(self.t):
                for ifn in self[first:last]:
                    if ifn.startswith(self.s):
                        ofn = self.t + ifn[discard:] # strips source directory
                        self._copyfile(ifn, ofn, self.q)
                    else:
                        print('INFO: file is not in source directory.')
                        print('INFO: skipping file %s.' % ifn)
            else:
                msg = 'FATAL ERROR: Target directory does not exist %s' % self.t
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
        self.s = common_start
        

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='musicsync.py',
                description='sync music from library to device using an m3u playlist')
    parser.add_argument('-if', '--infile', type=str, default='playlist.m3u',
                        metavar='<file name>',
                        help='input file, an m3u playlist, defaults to playlist.m3u')
    parser.add_argument('-t', '--target', type=str, default='./Copiedfiles/',
                        metavar='<directory path>',
                        help='target, path to a directory defaults to ./Copiedfiles/')
    parser.add_argument('-s', '--source', type=str, 
                        metavar='<directory path>',
                        help='source directory, a good default is guessed')
    parser.add_argument('-q', '--quick',type=str2bool, nargs='?',
                        const=True, default=False, metavar='True',
                        help='Do only a quick check for existing files')
    parser.add_argument('-d', '--delete',type=str2bool, nargs='?',
                        const=True, default=False, metavar='True',
                        help='Delete music files on target if not in playlist')
    parser.add_argument('-c', '--copy',type=str2bool, nargs='?',
                        const=True, default=True, metavar='False',
                        help='Copy files to target. Defualt is True')
    
    args = parser.parse_args()

    playlist = Playlist(args.infile)
    if args.target.endswith('/'):
        playlist.t = args.target
    else:
        playlist.target = args.target + '/'
    print('INFO: target directory is %s' % playlist.t)
    if args.source:
        if args.source.endswith('/'):
            playlist.s = args.source
        else:
            playlist.s = args.source + '/'
    else:
        playlist.guess_source()
    playlist.q = args.quick
    if playlist.q:
        print('INFO: quick option selected')
        print('\tWill skip copying if file of name name exists on device')
        print('\teven if it is different from source file.')
    print('INFO: source is %s,' % playlist.s)
    print('\tpath to source will be ignored when creating sub directories in target')
    if args.copy:
        playlist.copyfiles()
    else:
        print('INFO: not copying, -c option is', args.copy)
    
