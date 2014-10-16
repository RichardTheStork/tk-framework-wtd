import os, subprocess

CREATE_NO_WINDOW  = 0x00000008

def test():
	print "Succesfull test!"

# ffmpegPath = r"W:/WG/WTD_Code/trunk/wtd/pipeline/resources/ffmpeg/bin/ffmpeg.exe" 
def ffmpegMakingSlates(inputFilePath, outputFilePath, audioPath = "", topleft = "", topmiddle = "", topright = "", bottomleft = "", bottommiddle = "", bottomright = "", ffmpegPath = "ffmpeg.exe", font = "arial.ttf", font_size = 16, font_color = "white", slate_height = 21, slate_color = "black@1.0", overwrite = True, logLevel = "quiet"):
	
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
	
def ffmpegMakingMovie(inputFilePath, outputFilePath, audioPath = "",start_frame = 0, framerate = 24, encodeOptions = None, ffmpegPath = "ffmpeg.exe"):
	codec = ""
	if encodeOptions != None:
		codec = " -vcodec %s" %(encodeOptions)	
	elif outputFilePath.endswith(".mov"):
		codec = " -vcodec %s" %("mjpeg")
	elif outputFilePath.endswith(".mp4"):
		codec = " -vcodec %s" %("libx264")
		
	audio = ""
	if audioPath != "":
		audio = " -i %s" %audioPath
		
	value = subprocess.call('{ffmpeg} -start_number "{start_frame}" -i "{input}"{audio}{codec} -r {framerate} "{output}" -y'.format(ffmpeg=ffmpegPath, input=inputFilePath, output=outputFilePath, codec=codec, audio=audio, start_frame=start_frame, framerate=framerate), creationflags=CREATE_NO_WINDOW, shell=False)
	return value
	
def ffmpegConcatFiles(inputDict, outputFilePath, audioDict, ffmpegPath = "ffmpeg.exe"):
	print '! TODO !'
	concatString = ""
	concatAudioString = ""
	
	for i in inputDict:
		concatString += "%s|" %(i)
	for a in audioDict:
		concatAudioString += "%s|" %(a)
	
	value = subprocess.call('{ffmpeg} -start_number "{start_frame}" -i "{input}"{audio} "{output}" -y'.format(ffmpeg=ffmpegPath, input=concatString, output=outputFilePath, audio=concatAudioString))
	return value
