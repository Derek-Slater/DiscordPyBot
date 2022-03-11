from PIL import Image, ImageDraw, ImageFont
import textwrap
from string import ascii_letters
import requests
import os

# attempts to download file from given URL
# returns the name it downloaded it as, "" if it failed to download
def downloadImgFromURL(imageURL):
    try:
        filename = imageURL.split('/')[-1]
        r = requests.get(imageURL, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        return filename
    except:
        return None

def addTextToImage(imageName, text):
    # open image and get size
    try:
        img = Image.open(imageName)
    except: #non-image
        return None
    width, height = img.size
    
    # set font size, and then get total length of string/font in pixels to wrap the text
    fontSize = int(height * 0.06)
    if fontSize < 20:
        fontSize = 20
    font = ImageFont.truetype("fonts/MICROSS.ttf",size=fontSize)
    avgCharWidth = sum(font.getsize(char)[0] for char in text) / len(text)
    maxCharsInLine = int(width / avgCharWidth) - 1 # -1 to account for horizontal padding
    wrappedText = textwrap.fill(text=text, width=maxCharsInLine)
    lines = wrappedText.count("\n") + 1
    lineSpacing = fontSize / 10

    # get height of entire text entry in order to have an appropriately sized background
    textImage = Image.new('RGBA', (width, height), color=(255, 255, 255))
    drawnImg = ImageDraw.Draw(textImage)
    textX, textY = width * 0.05, height * 0.025
    bb = drawnImg.textbbox((textX, textY), text=wrappedText, font=font, spacing=lineSpacing,
                            stroke_width=int(fontSize/12))
    x1, y1, x2, y2 = bb
    totalTextHeight = y2 - y1

    # create background that can encompass both the text and image,
    # and then actually put in the text/image
    newHeight = int(height + totalTextHeight + (2 * y1))
    imageList = list()
    imageFrames = 1
    if img.format == "GIF":
        imageFrames = img.n_frames

    for frame in range(imageFrames):
        canvasImage = Image.new('RGBA', (width, newHeight), color=(255, 255, 255))
        img.seek(frame)
        canvasImage.paste(img, (0, int((newHeight - height))))
        drawnImg = ImageDraw.Draw(canvasImage)
        drawnImg.text((textX, textY), text=wrappedText, font=font, spacing=lineSpacing, fill=(0, 0, 0))
        imageList.append(canvasImage)
    # for drawing with an outline, but can make it harder to read for smaller pictures
    # drawnImg.text((textX, textY), text=wrappedText, font=font, spacing=lineSpacing,
    #                         stroke_width=round(fontSize/12), stroke_fill=(0, 0, 0), 
    #                         fill=(255, 255, 255))
    try:
        duration = img.info["duration"]
        return imageList, duration
    except:
        return imageList, 0