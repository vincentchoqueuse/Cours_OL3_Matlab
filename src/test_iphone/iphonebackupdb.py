#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
#
# $Id: iphonebackupdb.py,v 1.2 2010/05/28 08:30:38 mstenber Exp $
#
# Author: Markus Stenberg <fingon@iki.fi>
#
#  Copyright (c) 2009 Markus Stenberg
#       All rights reserved
#
# Created:       Tue Mar 31 13:44:03 2009 mstenber
# Last modified: Fri Oct 14 00:22:09 2011 mstenber
# Edit time:     209 min
#
"""

This is a minimalist module which abstracts the iPhone backup
directory's contents (in the Library/Applicatuon
Support/MobileSync/backup) as a filesystem. Only supported operation
is right now copying a file for read-only use, but in theory some
other things might be also diable later on (listdir etc).

XXX - turn this to a FUSE module?

On the other hand, why bother.. Currently this is like 4th version of
iTunes backup DB that I'm supporting;

- pre-8.1 (.mdbackup files, plists with binary content)
- 8.2+ (.mdinfo files, readable plists with nested plists)
- 9.2+ (.mbdb, .mbdx index files + files as-is)
- 10.5+ (.mbdb - .mdbx files disappeared)

Disclaimer: This module is published for information purposes, and
it's usefulness for anyone else except me may be highly
questionable. However, it might serve some useful purpose to other
people too, so I keep it on my web site.. ;-)

(I know quite a bit more about the un-decoded fields in the .mbdb, but
as my application only needs this stuff, I can't be arsed to decode
them anytime soon.. basic UNIX backup stuff like permissions, uid/gid,
and so forth.)

"""
import os, os.path
import ms.debug, ms.util
import ms.hexdump
import ms.cstruct
import hashlib

#ms.debug.setModuleLevel('.*', 3)
(error, log, debug) = ms.debug.getCalls('iphonebackupdb')

BACKUPPATH=os.path.join(os.environ['HOME'], 'Library',
                        'Application Support',
                        'MobileSync', 'backup')

# Test data - not really used for anything if system works correctly,
# but they were useful when debugging the format
KNOWN = {'documents/rahat.pdb' : 'b07ac15b5c745a287d3ecdc60bb6f6b955c0f229',
         'documents/untitled.pdb': '27fe99e8746b43a9db00c332966d028998bc3a03',
         'Documents/Py%F6r%E4ily.PDB'.lower(): '95ef4154eedac2fcc458cf21ec93c8c3895d9fcb'}

def getMTime():
    mtime = None
    for iphone in os.listdir(BACKUPPATH):
        ipath = os.path.join(BACKUPPATH, iphone)
        imtime = ms.util.file_mtime(ipath)
        if mtime is None or mtime < imtime:
            mtime = imtime
    return imtime

def getS(data, ofs, defaultFF=False):
    if defaultFF:
        if data[ofs] == chr(0xFF):
            assert data[ofs+1] == chr(0xFF)
            return ofs+2, ''
    # Assume first digit is zero or some small value.. smirk. Seems to
    # be a short.
    #
    # For the time being, we assume strings < 512 bytes to keep sanity
    # checking valid (initial guess was < 256, which wasn't)
    assert data[ofs] in [chr(0), chr(1)], 'not 0/1: %s' % ord(data[ofs])
    l0 = ord(data[ofs])
    ofs += 1
    l = ord(data[ofs]) + 256 * l0
    ofs += 1
    return ofs+l, data[ofs:ofs+l]

def getN(data, ofs, count):
    return ofs+count, data[ofs:ofs+count]

def decodeMBDB(data):
    ofs = 6
    lofs = -1
    filenames = []
    while (ofs+20) < len(data):
        #debug('iter %r', ofs)
        assert ofs != lofs
        #print ms.hexdump.hexdump(data[ofs:ofs+150])
        lofs = ofs
        ofs, vendor = getS(data, ofs)
        ofs, filename = getS(data, ofs)
        #print vendor, filename
        ofs, bonus1 = getS(data, ofs, True)
        ofs, bonus2 = getS(data, ofs, True)
        ofs, bonus3 = getS(data, ofs, True)
        #print ms.hexdump.hexdump(data[ofs:ofs+100])
        ofs, garbage = getN(data, ofs, 39)
        ofs, cnt = getN(data, ofs, 1)
        filenames.append([lofs, vendor, filename, bonus1])
        bonuscount = ord(cnt)
        assert bonuscount <= 6, bonuscount
        bonus = []
        if bonuscount:
            for i in range(bonuscount):
                ofs, xxx = getS(data, ofs)
                ofs, yyy = getS(data, ofs)
                bonus.append((xxx, yyy))
        debug('idx#%d ofs#%d->%d %r %r (%d bonus %s)', len(filenames), lofs, ofs, vendor, filename, bonuscount, bonus)
    return filenames

def getBackups():
    l = []
    for iphone in os.listdir(BACKUPPATH):
        ipath = os.path.join(BACKUPPATH, iphone)
        l.append((os.stat(ipath).st_mtime, iphone, ipath))
    l.sort()
    l.reverse()
    return l

def iterBackups(iterator):
    l = getBackups()
    for _, iphone, ipath in l:
        debug('ipath:%r', ipath)
        filename = os.path.join(ipath, 'Manifest.mbdb')
        debug('opening %r', filename)
        data = open(filename).read()
        filenames = decodeMBDB(data)
        log('decoded %d filenames', len(filenames))
        # Create
        # - convenience mapping of file-name => file-ofs from 'filenames'
        # - convenience mapping of domain+file-name => file-ofs
        # - convenience mapping of file-ofs => hash-name from 'shas'
        fileMap = {}
        fFileMap = {}
        for lofs, vendor, filename, bonus1 in filenames:
            lofs -= 6 # 6 = start of mbdb
            lfilename = filename.lower()
            #fFileMap[vendor,filename] = lofs # just replaced by next step
            h = hashlib.sha1()
            h.update(vendor+'-'+filename)
            sha = h.digest().encode('hex')
            fileMap[lfilename] = sha
            k = vendor,lfilename
            fFileMap[k] = sha
        rv = iterator(ipath, fileMap, fFileMap)
        if rv is not None:
            return rv

def _copy(fromname, toname):
    open(toname, 'w').write(open(fromname).read())


def getFileToFilename(backuppath, destfilename):
    """ iphone database format 4 reader/decoder - this is 'simplified'
    version which will hopefully eventually work correctly."""
    bpl = backuppath.lower()
    def _iterator(ipath, fileMap, fFileMap):
        # Test how many of the files really exists
        # Hardcoded check
        sha = fileMap.get(bpl, '')
        if sha:
            if KNOWN.has_key(bpl):
                if sha != KNOWN[bpl]:
                    log('!!! WRONG sha: %s <> %s', sha, KNOWN[bpl])
                    sha = KNOWN[bpl]
            path = os.path.join(ipath, sha)
            log('found potential sha candidate %r', path)
            if ms.util.file_exists(path):
                log('and it even existed! yay')
                _copy(path, destfilename)
                return True
            else:
                log('Path %r not found', path)
        else:
            log('No sha found for %r', bpl)
    return iterBackups(_iterator)

# We care only about most recent backup by default, from most recent
# device..
def getDomainToDirectory(domain, directory, onlyMostRecentDevice=True):
    def _iterator(ipath, fileMap, fFileMap):
        dumped, skipped = 0, 0
        for (vendor, filename), sha in fFileMap.items():
            if vendor != domain:
                continue
            fromname = os.path.join(ipath, sha)
            if ms.util.exists(fromname):
                dumped += 1
                dirname = os.path.dirname(filename)
                basename = os.path.basename(filename)
                newdirname = os.path.join(directory, dirname)
                try:
                    os.makedirs(newdirname)
                except OSError:
                    pass
                toname = os.path.join(newdirname, basename)
                _copy(fromname, toname)
            else:
                skipped += 1
        if dumped:
            print 'Copied %d files' % dumped
        if skipped:
            print 'Skipped %d files' % skipped
        if onlyMostRecentDevice:
            return True
    return iterBackups(_iterator)

def dumpDirectory():
    def _iterator(ipath, fileMap, fFileMap):
        for (vendor, filename), sha in fFileMap.items():
            print ipath, vendor, filename, sha
        #return True # rather dump all devices?
    return iterBackups(_iterator)

if __name__ == '__main__':
    import sys
    import ms.util
    (opts, args) = ms.util.Getopt(format="d:o:l")
    if opts['d'] and opts['o']:
        apprefix, todir = opts['d'], opts['o']
        getDomainToDirectory(apprefix, todir)
    elif opts['l']:
        dumpDirectory()
    if 0:
        tfilename = '/tmp/test-iphonebackupdb.dat'
        assert getFileToFilename('documents/rahat.pdb', tfilename)
        assert not getFileToFilename('documents/rahat.pdbxxx', tfilename)
        os.unlink(tfilename)


