from PIL import Image
import PIL.ImageOps    

image = Image.open('send.png')
if image.mode == 'RGBA':
    r,g,b,a = image.split()
    rgb_image = Image.merge('RGB', (r,g,b))

    inverted_image = PIL.ImageOps.invert(rgb_image)

    r2,g2,b2 = inverted_image.split()

    final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

    final_transparent_image.save('send1.png')

else:
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save('send1.png')

from PIL import Image

img = Image.open('./send1.png')

img_resize = img.resize((512, 512), Image.LANCZOS)
img_resize.save('./send2.png')

