import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

# Raspberry Pi pin configuration:
RST = 4

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
width = disp.width
height = disp.height


def init():
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()


def show(data):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    left = 0
    top = 0
    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    # Write two lines of text.
    for index, elem in enumerate(data):
        draw.text((left, top + index*9), elem, font=font, fill=127)

    # Display image.
    disp.image(image)
    disp.display()
