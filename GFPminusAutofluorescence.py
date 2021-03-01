from collections import Counter
from ij import IJ
from ij import process
from ij.measure import ResultsTable

# get the current image as an ImagePlus
imp = IJ.getImage()

# convert ImagePlus to ColorProcessor
color_processor = process.ColorProcessor(imp.getBufferedImage())

# respect ROI
roi = imp.getRoi()
if roi: color_processor.setRoi(roi)

# get green values as bytes from channel
green_pixels = color_processor.crop().getChannel(2)
green_pixels = map(lambda p: p & 0xff, green_pixels)

red_pixels   = color_processor.crop().getChannel(1)
red_pixels = map(lambda p: p & 0xff, red_pixels)

# to avoid yellow (which shows up in red and green pixels)
# count only green pixels if equal to or more intense than red
minus_yellow = [x if x>=y else 0 for x,y in zip(green_pixels, red_pixels)]

green_pixels = minus_yellow
#print(green_pixels[:100])

### VISUAL TEST ###
#theight = 1200
#twidth = 1920
#mij = IJ.createImage("Worm", "8-bit black", twidth, theight, 1)
#mip = mij.getProcessor()
#a = []
# convert flat list to square (list of lists)
#for i in range(theight):
#    a.append(green_pixels[twidth*i:twidth*(i+1)])

# set each pixel individually in the new image
#for i in range(twidth):
#   for j in range(theight):
#       mip.putPixel(i, j, a[j][i])
       
#mij.show()

# for some reason imageJ bytes range -128 to 127

# convert signed java ints to unsigned ints by bitwise &, 0xff => 8bit, 0xff => 16bit ... so on
# wikipedia two's complement for more info
#gp = Counter(map(lambda p: p & 0xff, green_pixels))
# maybe clearer in binary, signed numbers use the first bit:
# -4 is 100, and 100 & 111 = 100, but in unsigned convention 4 is 100
# -3 is 101, becomes 5
# -2 is 110, becomes 6
# -1 is 111, becomes 7
#green_pixels = map(lambda p: p & 0b11111111, green_pixels)

# now use a python collection counter to get the number of times each pixel is observed
# counts = Counter(green_pixels)

# print if curious
# print(counts)

# but what we really want is:
# total intensity or pixel intensity * number of pixels
total = 0.0
ic = {x:0.0 for x in range(256)}
N = 0.0 # number of non-zero pixels
for pixel in green_pixels:
	# ignore 6> pixels
	if pixel < 6:
		continue
	# sum green intensity (i.e. value * number of pixels)
	total += pixel
	ic[pixel] += 1
	# sum number of pixels
	N += 1
#print(ic)
# report to a results table
#rt = ResultsTable()
rt = ResultsTable.getResultsTable()
# first set column headers
rt.setHeading(0, "Intensity")
rt.setHeading(1, "# Green")
rt.setHeading(2, "I/N")
rt.setHeading(3, "Name")
# then add values
rt.incrementCounter()
rt.addValue(0, total)
rt.addValue(1, N)
rt.addValue(2, total/float(N))
rt.addValue("Name", imp.getTitle())
rt.show("Green Intensity Scaled by the Number of Green Pixels")

# be careful with selections, they might drop out lots of pixels at 1 
# and result in seemingly higher values...
