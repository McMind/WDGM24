from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

obraz = Image.open('pliki/obraz.png')
inicjaly = Image.open('pliki/inicjaly.bmp')


def negatyw_pixel(pixel):
    return tuple(255 - subpixel for subpixel in pixel)


def zakres(w, h):
    return [(i, j) for i in range(w) for j in range(h)]


def wstaw_inicjaly(obraz, inicjaly, m, n, kolor):
    obraz_wyjsciowy = obraz.copy()
    (w, h) = inicjaly.size
    (w0, h0) = obraz_wyjsciowy.size
    for (i, j) in zakres(w, h):
        if i + m < w0 and j + n < h0:
            if not inicjaly.getpixel((i, j)):
                obraz_wyjsciowy.putpixel((i + m, j + n), kolor)
    return obraz_wyjsciowy


def wstaw_inicjaly_maska(obraz, inicjaly, m, n):
    obraz_wyjsciowy = obraz.copy()
    (w, h) = inicjaly.size
    (w0, h0) = obraz_wyjsciowy.size
    for (i, j) in zakres(w, h):
        if i + m < w0 and j + n < h0:
            if not inicjaly.getpixel((i, j)):
                negatyw_pixela = negatyw_pixel(obraz_wyjsciowy.getpixel((i + m, j + n)))
                obraz_wyjsciowy.putpixel((i + m, j + n), negatyw_pixela)
    return obraz_wyjsciowy


def wstaw_inicjaly_load(obraz, inicjaly, m, n, kolor):
    obraz_wyjsciowy = obraz.copy()
    (w, h) = inicjaly.size
    (w0, h0) = obraz_wyjsciowy.size
    pix_obraz = obraz_wyjsciowy.load()
    pix_inicjaly = inicjaly.load()
    for (i, j) in zakres(w, h):
        if i + m < w0 and j + n < h0:
            if not pix_inicjaly[i, j]:
                pix_obraz[i + m, j + n] = kolor
    return obraz_wyjsciowy


def wstaw_inicjaly_maska_load(obraz, inicjaly, m, n):
    obraz_wyjsciowy = obraz.copy()
    (w, h) = inicjaly.size
    (w0, h0) = obraz_wyjsciowy.size
    pix_obraz = obraz_wyjsciowy.load()
    pix_inicjaly = inicjaly.load()
    for (i, j) in zakres(w, h):
        if i + m < w0 and j + n < h0:
            if not pix_inicjaly[i, j]:
                negatyw_pixela = negatyw_pixel(pix_obraz[i + m, j + n])
                pix_obraz[i + m, j + n] = negatyw_pixela
    return obraz_wyjsciowy


def kontrast(obraz, wsp_kontrastu):
    mn = ((255 + wsp_kontrastu) / 255) ** 2
    obraz_wyjsciowy = obraz.point(lambda i: 128 + (i - 128) * mn)
    return obraz_wyjsciowy


def transformacja_logarytmiczna(obraz):
    obraz_wyjsciowy = obraz.point(lambda i: 255 * np.log(1 + i / 255))
    return obraz_wyjsciowy


def filtr_liniowy(image, a, b):
    image2 = image.copy()
    w, h = image2.size
    pixele = image2.load()
    for i, j in zakres(w, h):
        pixele[i, j] = (pixele[i, j][0] * a + b, pixele[i, j][1] * a + b, pixele[i, j][2] * a + b)
    return image2


def transformacja_gamma(obraz, gamma):
    obraz_wyjsciowy = obraz.point(lambda i: (i / 255) ** (1 / gamma) * 255)
    return obraz_wyjsciowy


# obraz1 = wstaw_inicjaly(obraz, inicjaly, obraz.size[0] - inicjaly.size[0], obraz.size[1] - inicjaly.size[1], (255, 0, 0))
# obraz1.save('obraz1.png')
#
# obraz2 = wstaw_inicjaly_maska(obraz, inicjaly, obraz.size[0] // 2, obraz.size[1] // 2)
# obraz2.save('obraz2.png')
#
# obraz1a = wstaw_inicjaly_load(obraz, inicjaly, obraz.size[0] - inicjaly.size[0], obraz.size[1] - inicjaly.size[1], (255, 0, 0))
# obraz1a.save('obraz1a.png')
#
# obraz2a = wstaw_inicjaly_maska_load(obraz, inicjaly, obraz.size[0] // 2, obraz.size[1] // 2)
# obraz2a.save('obraz2a.png')

# plt.figure(figsize=(12, 12))
# plt.subplot(2, 2, 1)
# plt.imshow(obraz1)
# plt.axis('off')
# plt.subplot(2, 2, 2)
# plt.imshow(obraz2)
# plt.axis('off')
# plt.subplot(2, 2, 3)
# plt.imshow(obraz1a)
# plt.axis('off')
# plt.subplot(2, 2, 4)
# plt.imshow(obraz2a)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig1.png')
# plt.show()

# obraz4a1 = kontrast(obraz, 25)
# obraz4a2 = kontrast(obraz, 50)
# obraz4a3 = kontrast(obraz, 100)
#
# plt.figure(figsize=(12, 3))
# plt.subplot(1, 4, 1)
# plt.imshow(obraz)
# plt.axis('off')
# plt.subplot(1, 4, 2)
# plt.imshow(obraz4a1)
# plt.axis('off')
# plt.subplot(1, 4, 3)
# plt.imshow(obraz4a2)
# plt.axis('off')
# plt.subplot(1, 4, 4)
# plt.imshow(obraz4a3)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig2.png')
# plt.show()

# obraz4b1 = transformacja_logarytmiczna(obraz)
# obraz4b2 = filtr_liniowy(obraz, 2, 100)
#
# plt.figure(figsize=(9, 3))
# plt.subplot(1, 3, 1)
# plt.imshow(obraz)
# plt.axis('off')
# plt.subplot(1, 3, 2)
# plt.imshow(obraz4b1)
# plt.axis('off')
# plt.subplot(1, 3, 3)
# plt.imshow(obraz4b2)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig3.png')
# plt.show()


# obraz4c1 = transformacja_gamma(obraz, 0.01)
# obraz4c2 = transformacja_gamma(obraz, 0.5)
# obraz4c3 = transformacja_gamma(obraz, 4)
#
# plt.figure(figsize=(12, 3))
# plt.subplot(1, 4, 1)
# plt.imshow(obraz)
# plt.axis('off')
# plt.subplot(1, 4, 2)
# plt.imshow(obraz4c1)
# plt.axis('off')
# plt.subplot(1, 4, 3)
# plt.imshow(obraz4c2)
# plt.axis('off')
# plt.subplot(1, 4, 4)
# plt.imshow(obraz4c3)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig4.png')
# plt.show()

# T = np.array(obraz, dtype='uint16')  # ustawiamy większy zakres inta
# T += 100
# T = np.clip(T, 0, 255).astype('uint8') # ustawiam zakres od 0 do 255 i przywracam do uint8
# obraz_wynik = Image.fromarray(T, "RGB")
# obraz_wynik.show()
