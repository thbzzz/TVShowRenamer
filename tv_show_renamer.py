#!/usr/bin/env python3

import os
import shutil

from docopt import docopt

usage = """TV Show Renamer

Usage:
  tv_show_renamer.py -d <dirname> -n <tv_show_name> -s <season> [--brave] [-v]
  tv_show_renamer.py (-h | --help)

Options:
  --brave   Be brave and move instead of copying
  -v        Verbose mode
"""

class TVShow():
    """"""
    def __init__(self, dirname: str, tvshowname: str, season: int, brave: bool, verbose: bool):
        """"""
        self.dirname = str(dirname)
        self.tvshowname = str(tvshowname)
        self.season = int(season)
        self.extension = ""
        self.brave = bool(brave)
        self.run()

    def run(self):
        """"""
        if self.brave:
            if not self.warning():
                print("[*] Cancelled")
                exit()

        files_old, files_new = self.gen()

        if self.brave:
            if self.warning():
                self.moveFiles(files_old, files_new)
            else:
                print("[*] Cancelled")
        else:
            self.copyFiles(files_old, files_new)

    def copyFiles(self, old, new):
        """"""
        for old_new in zip(old, new):
            shutil.copyfile(old_new[0], old_new[1])

    def format(self, index):
        """"""
        formatted = "%s S%sE%s.%s" % (self.tvshowname, str(self.season).zfill(2), str(index).zfill(2), self.extension)
        return os.path.join(self.dirname, formatted)

    def gen(self):
        """"""
        files_src = os.listdir(self.dirname)
        files_dst = []

        self.extension = os.path.splitext(files_src[0])[1][1:]

        for i in range(len(files_src)):
            files_src[i] = os.path.abspath(os.path.join(self.dirname, files_src[i]))

        for f in files_src:
            files_dst.append( self.format(files_src.index(f) + 1) )

        return (files_src, files_dst)

    def moveFiles(self, old, new):
        """"""
        for old_new in zip(old, new):
            shutil.move(old_new[0], old_new[1])

    def warning(self):
        """"""
        warning_msg = "[!] Warning: This will permanently rename ALL FILES in %s.\n\
             Renaming is based on files' current order, this might MESS UP your files.\n" % (self.dirname)

        print(warning_msg)
        yn = input("[?] Are your episodes in correct order? (y/n) ").lower() == 'y'

        return yn


if __name__ == "__main__":
    args = docopt(usage , version="0.1")

    tvshow = TVShow(
        args["<dirname>"],
        args["<tv_show_name>"],
        args["<season>"],
        args["--brave"],
        args["-v"]
    )
