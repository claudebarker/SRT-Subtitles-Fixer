""" 
Version 0.5.1
Written in python 2.7.6 by Megalon

This is a simple command line program to delay or speed up the timing of a ".srt" subtitle file.
It reads all of the lines of the SRT file as a text document, parses the SRT timecode data, and applies
a offset (positive or negative delay) to the timing of every subtitle.
"""

import argparse

# Method to convert the SRT timecode 00:00:00,000 string to an integer in milliseconds
def convertToMilliseconds(time):
	# Strip the comma
	time = time.replace(',', '')
	
	# Convert everything to milliseconds and int values
	hours = int(time[:2]) * 60 * 60 * 1000
	minutes = int(time[3:5]) * 60 * 1000
	seconds = int(time[6:8]) * 1000
	milli = int(time[8:])
	
	# Time in milliseconds
	fixedTime = hours + minutes + seconds + milli
	return fixedTime
	
# Method to convert milliseconds to SRT timecode 00:00:00,000 
def convertToSRTTimeCode(time):
	# Convert back to hours, minutes, seconds, and milliseconds
	hours, time = divmod(time,  3600000)
	minutes, time = divmod(time, 60000)
	seconds, time = divmod(time, 1000)
	milli = time
	
	# Convert to strings
	hours = str(hours)
	minutes = str(minutes)
	seconds = str(seconds)
	milli = str(milli)
	
	# Add zeros where there are empty spots
	if len(hours) == 1:
		hours = '0' + hours
	if len(minutes) == 1:
		minutes = '0' + minutes
	if len(seconds) == 1:
		seconds = '0' + seconds
	# For milliseconds, check if there is one empty spot, or two
	if len(milli) == 2:
		milli = '0' + milli
	elif len(milli) == 1:
		milli = '00' + milli
		
	# Format the output correctly. 00:00:00,000
	fixedString = hours + ':' + minutes + ':' + seconds + ',' + milli
	return fixedString

# Method to convert to milliseconds, then apply the time offset, then convert back to SRT timecode.
def modifyTime(time, offset, startTime):
	time = convertToMilliseconds(time)
	if convertToMilliseconds(startTime) < time:
		time = time + offset
	time = convertToSRTTimeCode(time)
	return time

# Method to modify the lines from the input file. Called for every line with SRT timecode.
def modifyLine(line, offset, startTime):
	# The starting time for this subtitle text
	start = line[0:12]
	# The ending time for this subtitle text
	end = line[-13:]
	
	# Call the method to change the time for the start and end times
	start = modifyTime(start, offset, startTime)
	end = modifyTime(end, offset, startTime)
	
	# Return the full string, with both the start and end times, in the correct format
	return start + " --> " + end + "\n"
	
def main():
	parser = argparse.ArgumentParser(description="\
	------------------------------------------------------------------------------\n \
	 ------------------------- SRT Subtitle Fixer v0.5.1 --------------------------\n \
	------------------------------------------------------------------------------\n \
	 -- Alter the timing of an SRT subtitle file. ---------------------------------\n \
	 -- Example: SRT_Subtitle_Fixer.py C:\\Input.srt C:\\Output.srt \n\
	00:00:05,000 -5000 \
	------------------------------------------------------------------------------")
	parser.add_argument('inputPath', metavar='inputPath', default=None, help='Input file path')
	parser.add_argument('outputPath', metavar='outputPath', default=None, help='Output file path')
	parser.add_argument('startTime', default='00:00:00,000', help='When to begin applying the offset to the srt timecodes. Default is 00:00:00,000')
	parser.add_argument('delayTime', help='How much time, in milliseconds, to offset the timing in the srt file. Positive, or negative.')
	parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output. Prints every change in SRT timecode.')
	args = parser.parse_args()
	inputPath = args.inputPath
	outputPath = args.outputPath
	startTime = args.startTime
	offset = int(args.delayTime)
	
	# The startTime can also be entered as 0, so the user does not have to enter 00:00:00,000 each time
	if startTime == '0':
		startTime = '00:00:00,000'
	
	print "\nDelaying subtitles " + inputPath + " by " + str(offset) + " milliseconds, and writing to file " + outputPath
	
	input = open(inputPath, 'r')
	output = open(outputPath, 'w')
	
	# Variable that holds the number of subtitles in the document.
	subtitlesCount = -1
	# Boolean that tells if the next line is a counting line that tells the subtitle number.
	nextCount = True
	
	for line in input:
		if nextCount == True:
			subtitlesCount = subtitlesCount + 1
			output.write(str(subtitlesCount) + "\n")
			nextCount = False
		# Check if the line is a timing line. 00:00:00,000 If not, simply write the line to the output file.
		# 30 characters is the lenght of the timing lines
		elif len(line) == 30:
			if line[2] == ':' and line[5] == ':' and line[8] == ',':
				# Call the method to modify this line to the new time, then write to the output file
				modifiedLine = modifyLine(line, offset, startTime)
				# Check for the verbose option
				if args.verbose:
					print subtitlesCount
					print "Changing " + line + " to      " + modifiedLine
				output.write(modifiedLine)
			else:
				output.write(line)
		elif line == "\n":
			nextCount = True
			output.write(line)
		else:
			output.write(line)
	print "Done!"
	print "Delayed subtitles " + inputPath + " by " + str(offset) + " milliseconds, starting at " + startTime + " and wrote to file " + outputPath + "!"
		
if __name__ == "__main__":
	main()