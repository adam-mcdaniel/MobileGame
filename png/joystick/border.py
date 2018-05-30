import glob, sys, os
from PIL import Image, ImageOps
for name in glob.glob(os.path.dirname(sys.argv[0])+"*.png"):
    print(name)
    img = Image.open(name)
    img_with_border = ImageOps.expand(img,border=160,fill='black')
    img_with_border.save(name.replace(".png", "border.png"))

    img = Image.open(name.replace(".png", "border.png"))
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(name, "PNG")