#!/usr/bin/env python
"""print true if VLC playing"""
import vlc

if __name__ == "__main__":
    if vlc.playing():
        print("true")
