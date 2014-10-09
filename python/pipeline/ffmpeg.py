import os

def test():
	print "Succesfull test!"

# ffmpegPath = r"W:/WG/WTD_Code/trunk/wtd/pipeline/resources/ffmpeg/bin/ffmpeg.exe" 
def ffmpegMakingSlates(inputFilePath, outputFilePath, audioPath = "", topleft = "", topmiddle = "", topright = "", bottomleft = "", bottommiddle = "", bottomright = "", ffmpegPath = "ffmpeg.exe", font = "arial.ttf", font_size = 10, font_color = "gray", slate_height = 13, slate_color = "black@0.8", overwrite = True):
	
	top = "%s/5.0" %slate_height
	bottom = "h-(%s-%s/5.0-1)" %(slate_height, slate_height)
	if overwrite:
		overwrite = "-y"
	else:
		overwrite = ""
	
	command_line_arguments = '{ffmpeg} -f image2 -i "{input}" -vf "drawbox=x=-{slate_height}:y=0:w=20000:h=0:color={slate_color}:t={slate_height},\
	drawtext=fontsize={font_size}:fontfile={font}: text={topleft}: x={left}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={topmiddle}: x={middle}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={topright}: x={right}: y={top}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottomleft}: x={left}: y={bottom}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottommiddle}: x={middle}: y={bottom}: fontcolor={font_color},\
	drawtext=fontsize={font_size}:fontfile={font}:text={bottomright}: x={right}: y={bottom}: fontcolor={font_color}"\
	"{output}" {overwrite}'.format(
		ffmpeg=ffmpegPath, input=inputFilePath, output=outputFilePath, 
		topleft=topleft, topmiddle=topmiddle, topright=topright ,bottomleft=bottomleft, bottommiddle=bottommiddle, bottomright=bottomright, 
		left= "5",middle= "(w-tw)/2", right= "(w-tw)-5", top="13/5.0" , bottom="h-(13-13/5.0-1)", 
		font=font, font_size=font_size, font_color=font_color, 
		slate_height=slate_height, slate_color=slate_color, overwrite = overwrite
		)
	os.system(command_line_arguments)

# ffmpegMakingSlates(r"W:\RTS\People\Mclaeys\fun\StorkLegacy.png", r"W:\RTS\People\Mclaeys\fun\StorkLegacy.png", topleft= "Mathias 10", topmiddle= "Mathias 20", topright= "Mathias 30", bottomleft= "Mathias 40", bottommiddle= "Mathias 50", bottomright= "Mathias 60")