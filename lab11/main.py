import numpy as np
from PIL import Image, ImageOps, ImageChops, ImageStat, ImageDraw, ImageFont
import matplotlib.pyplot as plt

im1 = Image.open('obraz1.png')
im2 = Image.open('obraz2.png')
# im_blend = Image.blend(im1, im2, 3/5)
# im_blend.save('obraz_blend.png')

# box = (98, 24, 179, 65)
# fragment = im1.crop(box)
# im2_2a = im2.copy()
# im2_2a.paste(fragment, (63, 7))
# im2_2a.save('obraz2_2a.png')

# maska = Image.new('L', im1.size, 'black')
# dctx = ImageDraw.Draw(maska)
# dctx.ellipse(box, fill='white')
# del dctx
# maska.save('maska.png')
# print(maska.mode)
# im1_maska = im1.copy()
# im1_maska.paste(im2, (0, 0), maska)
# im1_maska.save('obraz1_maska.png')
# im2_maska = im2.copy()
# im2_maska.paste(im1, (0, 0), maska)
# im2_maska.save('obraz2_maska.png')
# im1_maska_alfa = im1.copy()
# im1_maska_alfa.putalpha(maska)
# im1_maska_alfa.save('obraz1_maska_alfa.png')

# im1_tekst1 = im1.copy()
# tekst = "Jedi używa Mocy do\nzdobywania wiedzy i\nobrony, nigdy do ataku"
# fnt = ImageFont.truetype('ttf/DejaVuSans.ttf', 22)
# d = ImageDraw.Draw(im1_tekst1)
# d.text((10, 400), tekst, font=fnt, fill='chartreuse', align='left')
# del d
# im1_tekst2 = im1.copy().convert('RGBA')
# tekst = "Jedi używa Mocy do\nzdobywania wiedzy i\nobrony, nigdy do ataku"
# txt = Image.new('RGBA', im1_tekst2.size, (0,0,0,0))
# fnt = ImageFont.truetype('ttf/DejaVuSans.ttf', 22)
# d = ImageDraw.Draw(txt)
# d.text((10, 400), tekst, font=fnt, fill=(127, 255, 0, 200), align='left')
# del d
# im1_tekst2 = Image.alpha_composite(im1_tekst2, txt)
# im1_tekst2.save('obraz1_tekst2.png')
