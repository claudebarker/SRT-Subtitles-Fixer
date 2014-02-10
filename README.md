SRT-Subtitles-Fixer
===================

<b>Written in python 2.7.6 by Megalon</b>

This is a simple command line program to delay or speed up the timing of a ".srt" subtitle file.
It reads all of the lines of the SRT file as a text document, parses the SRT timecode data, and applies
an offset (positive or negative delay) to the timing of every subtitle.

SRT Timecode is in the format "00:00:00,000" which translates to "hours:minutes:seconds,milliseconds"

|

<b>Command line argument formatting:</b> SRT_Subtitle_Fixer.py inputPath outputPath delayTime

inputPath: The file path for the initial .srt subtitles file.

outputPath: The file path for the fixed .srt subtitles file.

delaytime: The amount of time, in milliseconds, to delay the subtitle timings in the input file. Positive numbers delay, negative numbers hasten. i.e. 5000 makes the subtitles appear 5 seconds later, while -5000 makes them appear 5 seconds sooner.

|

<b>Options include:</b>

-h    Help. Displays all arguments and options.

-v    Verbose output. Shows every change made to the original timing.

-s    Start time. When to begin applying the offset to the srt timecodes. Default is 00:00:00,000

-i    Insert a new subtitle at any given time in 00:00:00,000 format.

|

<b>Complete example:</b> SRT_Subtitle_Fixer.py C:\Input.srt C:\Output.srt -5000 -v -s 00:05:00,000 -i 00:25:00,000

This example reads the file "C:\Input.srt" and writes to file "C:\Output.srt". "-5000" speeds up the subtitles by 5 seconds (-5000 milliseconds delay). "-v" prints the verbose output. "-s 00:05:00,000" tells the script to delay the subtitles that occur after 5 minutes. "-i 00:25:00,000" inserts a new blank, zero length subtitle at the 25 minute mark.
