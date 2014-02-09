""" 
Version 0.6.1
Written in python 2.7.6 by Megalon

This is a simple command line program to delay or speed up the timing of a ".srt" subtitle file.
It reads all of the lines of the SRT file as a text document, parses the SRT timecode data, and applies
an offset (positive or negative delay) to the timing of every subtitle.

Options include:
	-v Verbose output. Shows every change made to the original timing.
	-s Start time. When to begin applying the offset to the srt timecodes. Default is 00:00:00,000
	-i Insert a new subtitle at any given time in 00:00:00,000 format.
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
	if startTime < time:
		time = time + offset
	return time

# Method to split the timing line into beginning and end variables
def splitLine(line):
	# The starting time for this subtitle text
	beginning = line[0:12]
	# The ending time for this subtitle text
	end = line[-13:]
	return beginning, end
	
def main():
	parser = argparse.ArgumentParser(description="\
	------------------------------------------------------------------------------\n \
	------------------------- SRT Subtitle Fixer v0.6.1 --------------------------\n \
	------------------------------------------------------------------------------\n \
	-- Example: ------------------------------------------------------------------\n\
	SRT_Subtitle_Fixer.py C:\\Input.srt C:\\Output.srt \n\
	-5000 -s 00:05:00,000 \
	------------------------------------------------------------------------------")
	parser.add_argument('inputPath', metavar='inputPath', default=None, help='Input file path')
	parser.add_argument('outputPath', metavar='outputPath', default=None, help='Output file path')
	parser.add_argument('delayTime', help='How much time, in milliseconds, to offset the timing in the srt file. Positive, or negative.')
	parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output. Prints every change in SRT timecode.')
	parser.add_argument('-s', '--startTime', action='store', default='00:00:00,000', help='When to begin applying the offset to the srt timecodes. Default is 00:00:00,000')
	parser.add_argument('-i', '--insert', action='store', help='Insert a blank subtitle at specified time in 00:00:00,000 format.')
	args = parser.parse_args()
	inputPath = args.inputPath
	outputPath = args.outputPath
	startTime = args.startTime
	offset = int(args.delayTime)
	if args.insert != None:
		insertTime = convertToMilliseconds(args.insert)
	# The startTime can also be entered as 0, so the user does not have to enter 00:00:00,000 each time
	if startTime == '0' or startTime == 0:
		startTime = '00:00:00,000'
	startTime = convertToMilliseconds(startTime)
	
	print "\nDelaying subtitles " + inputPath + " by " + str(offset) + " milliseconds, and writing to file " + outputPath
	
	input = open(inputPath, 'r')
	output = open(outputPath, 'w')
	
	# Variable that holds the number of subtitles in the document.
	subtitlesCount = -1
	# Boolean that tells if the next line has the subtitle number.
	nextCount = True
	previousTime = 0
	
	for line in input:
		# If the line has a subtitle number, increase the subtitle count, and print it to the file.
		if nextCount == True:
			subtitlesCount = subtitlesCount + 1
			output.write(str(subtitlesCount) + "\n")
			nextCount = False
		# Check if the line is a timing line. 00:00:00,000 format. If not, simply write the line to the output file.
		# 30 characters is the lenght of the timing lines
		elif len(line) == 30:
			if line[2] == ':' and line[5] == ':' and line[8] == ',':				
				# Split the line into beginning time and end time
				beginning, end = splitLine(line)
				
				# Convert beginning and end time to milliseconds
				beginning = convertToMilliseconds(beginning)
				end = convertToMilliseconds(end)
				
				# Attempt to insert a new line if the option is chosen
				if args.insert != None:
					# Check if the insertTime is after the previous time, but before the current time
					# If so, insert a new blank subtitle, and increase the subtitle count
					if previousTime < insertTime and beginning > insertTime:
						subtitlesCount = subtitlesCount + 1
						insertedLine = convertToSRTTimeCode(insertTime) + " --> " + convertToSRTTimeCode(insertTime) + "\n"
						output.write(insertedLine + "\n" + str(subtitlesCount) + "\n")
					previousTime = beginning
				
				# Call the method to change the time for the beginning and end times
				beginning = modifyTime(beginning, offset, startTime)
				end = modifyTime(end, offset, startTime)
				
				beginning = convertToSRTTimeCode(beginning)
				end = convertToSRTTimeCode(end)
				
				modifiedLine = beginning + " --> " + end + "\n"
				
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
	print "Delayed subtitles " + inputPath + " by " + str(offset) + " milliseconds, starting at " + convertToSRTTimeCode(startTime) + " and wrote to file " + outputPath + "!"
		
if __name__ == "__main__":
	main()