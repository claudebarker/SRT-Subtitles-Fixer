SRT-Subtitles-Fixer
===================

Written in python 2.7.6 by Megalon

This is a simple command line program to delay or speed up the timing of a ".srt" subtitle file.
It reads all of the lines of the SRT file as a text document, parses the SRT timecode data, and applies
an offset (positive or negative delay) to the timing of every subtitle.

Options include:

-i Insert a new subtitle at any given time in 00:00:00,000 format.

-v Verbose output. Shows every change made to the original timing.
