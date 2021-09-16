# RENDER THIS DOCUMENT WITH DRAWBOT: http://www.drawbot.com
# COMPRESSED WITH: https://github.com/kornelski/pngquant
# $ brew install pngquant
# $ pngquant image.png
from drawBot import *
from datetime import date
from fontTools.ttLib import TTFont
from fontTools.misc.fixedTools import floatToFixedToStr
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', metavar="PNG", help='where to write the PNG file')
args = parser.parse_args()

# Constants
WIDTH, HEIGHT, MARGIN, FRAMES = 792, 612, 36, 1
FONT_PATH = "sources/variable_ttf/Mekorot-VF.ttf"
AUXILIARY_FONT = "Helvetica Neue"
AUXILIARY_FONT_SIZE = 12
BIG_TEXT = FormattedString()
BIG_TEXT.append("Aa", font=FONT_PATH, fontSize=MARGIN*8, fill=(1))
BIG_TEXT_WIDTH = BIG_TEXT.size().width
BIG_TEXT_HEIGHT = BIG_TEXT.size().height
BIG_TEXT_X_POS = (WIDTH - BIG_TEXT_WIDTH) / 2 # Adjust this number to change x-axis of main text
BIG_TEXT_Y_POS = (HEIGHT - BIG_TEXT_HEIGHT - (MARGIN * 2))

ttFont = TTFont(FONT_PATH)

# Constants we will work out dynamically
MY_URL = subprocess.check_output("git remote get-url origin", shell=True).decode()
MY_HASH = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode()
MY_FONT_NAME = ttFont["name"].getDebugName(4)
FONT_VERSION = "v%s" % floatToFixedToStr(ttFont["head"].fontRevision, 16)

# Draws a grid
def grid():
    stroke(1,0,0,0.1)
    fill(None)
    strokeWidth(1)
    STEP_X, STEP_Y = 0, 0
    INCREMENT_X, INCREMENT_Y = MARGIN / 2, MARGIN / 2
    rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 2))
    for x in range(30):
        polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN))
        STEP_X += INCREMENT_X
    for y in range(50):
        polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
        STEP_Y += INCREMENT_Y
    polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))

# Remap input range to VF axis range
# (E.G. sinewave(-1,1) to wght(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
    outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)

# Draw page
newPage(WIDTH, HEIGHT)
#grid() # uncomment to view a grid over the background

# Main text
fill(0)
stroke(None)
font(FONT_PATH)
# Text waterfall
fontSize(MARGIN*0.8)
tracking(None)

# list all axis from the current font
for axis, data in listFontVariations().items():
    print((axis, data))

# Main text
fontVariations(wght=400)


language("en")
step = 12
var = 400
for i in range(9):
    fontVariations(wght=var)
    text("Typography on the UNIX System",(MARGIN,MARGIN*step))
    step -= 1
    var += 50

fontSize(MARGIN / 2)

# Divider lines
stroke(0)
strokeWidth(1)
lineCap("round")
line((MARGIN, HEIGHT - MARGIN), (WIDTH - MARGIN, HEIGHT - MARGIN))
line((MARGIN, MARGIN + (MARGIN / 2)), (WIDTH - MARGIN, MARGIN + (MARGIN / 2)))
stroke(None)

# Auxiliary text
font(AUXILIARY_FONT)
fontSize(AUXILIARY_FONT_SIZE)
POS_TOP_LEFT = (MARGIN, HEIGHT - MARGIN * 1.5)
POS_TOP_RIGHT = (WIDTH - MARGIN * 0.9, HEIGHT - MARGIN * 1.5)
POS_BOTTOM_LEFT = (MARGIN, MARGIN)
POS_BOTTOM_RIGHT = (WIDTH - MARGIN * 0.85, MARGIN)
URL_AND_HASH = MY_URL + "at commit " + MY_HASH
URL_AND_HASH = URL_AND_HASH.replace('\n', ' ')

text(MY_FONT_NAME+": Weight Axis Range", POS_TOP_LEFT, align="left")
text(FONT_VERSION, POS_TOP_RIGHT, align="right")
text(URL_AND_HASH+str(date.today()), POS_BOTTOM_LEFT, align="left")
text("OFL v1.1", POS_BOTTOM_RIGHT, align="right")

# Save output
saveImage(args.output)
print("DrawBot: Done")
