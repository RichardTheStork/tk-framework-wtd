import os, subprocess

CREATE_NO_WINDOW  = 0x00000008

def test():
	print "Succesfull test!"

ffmpegPath = ""
try:
	ffmpegPath = r'%s/ffmpeg.exe' %os.environ["FFMPEG_PATH"] 
except:
	ffmpegPath = r'ffmpeg.exe'
	
def ffmpegMakingSlates(inputFilePath, outputFilePath, audioPath = "", topleft = "", topmiddle = "", topright = "", bottomleft = "", bottommiddle = "", bottomright = "", ffmpegPath = ffmpegPath, font = "arial.ttf", font_size = 16, font_color = "white", slate_height = 21, slate_color = "black@1.0", overwrite = True, logLevel = "quiet"):
	
	top = "%s/5.0" %slate_height
	bottom = "h-(%s-%s/5.0-1)" %(slate_height, slate_height)
	if overwrite:
		overwrite = "-y"
	else:
		overwrite = ""
	
	logLevel = "-loglevel %s " %logLevel
	
	command_line_arguments = '{ffmpeg} {logLevel}-f image2 -i "{input}" -vf "drawbox=x=-{slate_height}:y=0:w=20000:h=0:color={slate_color}:t={slate_height},\
	drawtext=fontsize={font_size}:fontfile={font}: text={topleft}: x={left}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={topmiddle}: x={middle}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={topright}: x={right}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottomleft}: x={left}: y={bottom}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottommiddle}: x={middle}: y={bottom}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottomright}: x={right}: y={bottom}: fontcolor={font_color}"\
	"{output}" {overwrite}'.format(
		ffmpeg=ffmpegPath, input=inputFilePath, output=outputFilePath, 
		topleft=topleft, topmiddle=topmiddle, topright=topright ,bottomleft=bottomleft, bottommiddle=bottommiddle, bottomright=bottomright, 
		left= "5",middle= "(w-tw)/2", right= "(w-tw)-5", top="%s/5.0" %slate_height, bottom="h-(%s-%s/5.0-1)" %(slate_height, slate_height), 
		font=font, font_size=font_size, font_color=font_color, 
		slate_height=slate_height, slate_color=slate_color, overwrite = overwrite, logLevel = logLevel
		)
	value = subprocess.call(command_line_arguments, creationflags=CREATE_NO_WINDOW, shell=False)
	return value
	
def ffmpegMakingMovie(inputFilePath, outputFilePath, audioPath = "",start_frame = -1, end_frame = -1, frame_duration = -1, framerate = 24, encodeOptions = None, ffmpegPath = ffmpegPath):
	codec = ""
	if outputFilePath.endswith(".mov") or encodeOptions == "mjpeg":
		codec = " -vcodec %s -qscale 1" %("mjpeg")
	elif outputFilePath.endswith(".mp4"):
		codec = " -vcodec %s" %("libx264")
	elif encodeOptions != None:
		codec = " -vcodec %s" %(encodeOptions)	
		
	start = ""
	duration = ""
	numberOfFrames = -1
	if start_frame > -1:
		start = ' -start_number "%s"' %start_frame
	if end_frame > -1:
		numberOfFrames = end_frame - start_frame +1
		duration = ' -vframes "%s"' %numberOfFrames
	if frame_duration > -1:
		numberOfFrames = frame_duration
		duration = ' -vframes "%s"' %frame_duration
		
	if "\\" in ffmpegPath:
		ffmpegPath = ffmpegPath.replace("\\","/")
		
	audio = ""
	if audioPath != "":
		audio = " -i %s" %audioPath
	
	"""
		-rc_override[:stream_specifier] override (output,per-stream)
		Rate control override for specific intervals, formatted as "int,int,int" list separated with slashes. Two first values are the beginning and end frame numbers, last one is quantizer to use if positive, or quality factor if negative.
	"""	
	ffmpeg_command = '{ffmpeg}{start_frame} -r {framerate} -i "{input}"{audio}{codec} -r {framerate}{duration} "{output}" -y'.format(ffmpeg=ffmpegPath, input=inputFilePath, output=outputFilePath, codec=codec, audio=audio, start_frame=start, duration=duration,framerate=framerate)
	print ffmpeg_command
	value = subprocess.call(ffmpeg_command, creationflags=CREATE_NO_WINDOW, shell=False)
	return value
	
def combineMediaFiles(fileList, output, ffmpegPath = ffmpegPath):
	results = []
	rootPath = str.split(str(fileList[0]),"/q")[0]
	mediaType = str.rsplit(str(fileList[0]),".",1)[1]
	mediaFilePresent = False
	mediaListFile = rootPath+'/tmp_'+mediaType+'List.txt'
	with open(mediaListFile, 'w') as mediaTxtFile:
		for mediaFile in fileList:
			if os.path.exists(mediaFile):
				mediaFilePresent = True
				shotPath = str.split(str(mediaFile),"Sequences")[1][1:]
				mediaTxtFile.write("file '" +shotPath+"'")
				mediaTxtFile.write('\r\n')
			else:
				print("MEDIA FILE NOT FOUND :  " + str(mediaFile))
				results.append({"task":"audio stuff", "errors":("AUDIO FILE NOT FOUND :  " + str(mediaFile))})
	returnValue = ffmpegConcatFiles(mediaListFile, output, ffmpegPath = ffmpegPath)
	if returnValue == None:
		results.append({"task":"concat file", "errors":("Error while making total file %s" %output)})
	
	return results
	
def ffmpegConcatFiles(listfile, output, ffmpegPath = ffmpegPath):
	if os.path.exists(listfile):
		command = '{ffmpeg} -f concat -i {mediaListFile} -c copy {output}'.format(ffmpeg=ffmpegPath, mediaListFile=listfile, output=output)
		command = str.replace(str(command), "\\" , "/")
		print command
		value = subprocess.call(command, creationflags=CREATE_NO_WINDOW, shell=False)
		return output
	else:
		return None

	
def main():
	ffmpegPath =r'%s/ffmpeg.exe' %os.environ["FFMPEG_PATH"]
	input = r'W:\RTS\Renders\Sequences\lay\q350\publish\maya\v002\playblast\1724x936\q350_lay.%04d.png'
	output = r'C:\Users\mclaeys\Desktop\Test_q350.mov'
	start = 1032
	end = 1080
	duration = 27
	encoder = "libx264"
	
	# value = subprocess.call(ffmpegPath)
	value = ffmpegMakingMovie(inputFilePath = input, outputFilePath = output, start_frame = start, end_frame = end, framerate = 24)
	return value
	
	
# if __name__ == '__main__':
    # main()