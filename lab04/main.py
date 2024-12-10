from PIL import Image
import numpy as np
from PIL import ImageChops as chops
from PIL import ImageStat as stat
import matplotlib.pyplot as plt
from itertools import permutations


def negatyw(obraz):
    tab = np.asarray(obraz)
    tab_neg = tab.copy()
    h, w, b = tab.shape
    for i in range(h):
        for j in range(w):
            for k in range(b):
                tab_neg[i, j, k] = 255 - tab_neg[i, j, k]
    return Image.fromarray(tab_neg)


def takie_same(obraz1, obraz2):  # zwraca True gdy obrazy są takie same lub False w przeciwnym wypadku
    diff = chops.difference(obraz1, obraz2)
    tab = np.asarray(diff, np.bool)
    if obraz1.mode != obraz2.mode or obraz1.size != obraz2.size:
        return False
    return not np.any(tab)


def pokaz_roznice(obraz1, obraz2):  # wyrzuca obraz z ImageChops tylko używa do tego czarno białego obrazu,
    # tam gdzie jest różnica pixel będzie biały, w przeciwnym wypadku czarny
    if takie_same(obraz1, obraz2):
        return Image.fromarray(np.zeros(obraz1.size, dtype=np.bool))
    diff = chops.difference(obraz1, obraz2)
    tab = np.asarray(diff, np.bool)
    tab2d = np.all(tab, axis=2)
    return Image.fromarray(tab2d)


def sprawdz(obraz, mix):
    if takie_same(obraz, mix):
        return "Obraz i mix są takie same"
    if takie_same(negatyw(obraz), mix):
        return "Mix jest w negatywie"
    r, g, b = obraz.split()
    for perm in permutations((r, g, b)):
        test = Image.merge('RGB', perm)
        if takie_same(test, mix):
            perm_text = ', '.join(['r', 'g', 'b'][(r, g, b).index(c)] for c in perm)
            return f"Mix jest przestawieniem kanałów ({perm_text}) oryginału"

    return "Mix nie jest permutacją kanałów oryginału, ani nie jest jego negatywem"


def rysuj_ramki_szare(w, h, grub, zmiana_koloru):
    t = (h, w)
    tab = np.ones(t, dtype=np.uint8)
    min_dimension = min(w, h)
    liczba_paskow = min_dimension // (2 * grub) + 1
    for i in range(liczba_paskow):
        start = i * grub
        end_w = w - start
        end_h = h - start
        tab[start:end_h, start:end_w] = (i * zmiana_koloru) % 256
    return Image.fromarray(tab)


# im = Image.open('og.png')
# (im_width, im_height) = im.size
# T = np.array(im)
# t_r = T[:, :, 0]
# t_g = T[:, :, 1]
# t_b = T[:, :, 2]
# im_r = Image.fromarray(t_r)
# im_g = Image.fromarray(t_g)
# im_b = Image.fromarray(t_b)
# im1 = Image.merge('RGB', (im_r, im_g, im_b))
# diff1 = chops.difference(im, im1)
#
# plt.figure(figsize=(12,3))
# plt.subplot(1,3,1)
# plt.imshow(im)
# plt.axis('off')
# plt.subplot(1,3,2)
# plt.imshow(im1)
# plt.axis('off')
# plt.subplot(1,3,3)
# plt.imshow(diff1)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig1.png')
# plt.show()
# r, g, b = im.split()
# # im.show()
# im2 = Image.merge('RGB', (r, b, g))
# im2.save('im2.jpg')
# im2.save('im2.png')
# im2_png = Image.open('im2.png')
# im2_jpg = Image.open('im2.jpg')
# diff2 = chops.difference(im2_png, im2_jpg)


# im.show()
# im2_png.show()
# pokaz_roznice(im2_jpg, im2_png).show()
# # test1 = Image.open('pliki/beksinski.png')
# # test2 = Image.open('pliki/output.png')
# plt.figure(figsize=(12,3))
# plt.subplot(1,3,1)
# plt.imshow(im2_png)
# plt.axis('off')
# plt.subplot(1,3,2)
# plt.imshow(im2_png)
# plt.axis('off')
# plt.subplot(1,3,3)
# plt.imshow(diff2)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig2.png')
# plt.show()
# im3 = rysuj_ramki_szare(im_width, im_height, 16, 15)
# im3_r = Image.merge('RGB', (im3, im_g, im_b))
# im3_g = Image.merge('RGB', (im_r, im3, im_b))
# im3_b = Image.merge('RGB', (im_r, im_g, im3))
# plt.figure(figsize=(12,3))
# plt.subplot(1,3,1)
# plt.imshow(im3_r)
# plt.axis('off')
# plt.subplot(1,3,2)
# plt.imshow(im3_g)
# plt.axis('off')
# plt.subplot(1,3,3)
# plt.imshow(im3_b)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig4.png')
# plt.show()
# kolejnytest1 = Image.open('pliki/beksinski.png')
# kolejnytest2 = Image.open('pliki/beksinskitest.png')
# pokaz_roznice(kolejnytest1, kolejnytest2).show()

def statystyki(im):
    s = stat.Stat(im)
    print("extrema ", s.extrema)  # max i min
    print("count ", s.count)  # zlicza
    print("mean ", s.mean)  # srednia
    print("median ", s.median)  # mediana
    print("stddev ", s.stddev)  # odchylenie standardowe

obraz11 = Image.open('test/obraz11.jpg')
statystyki(obraz11)

def rysuj_histogram_RGB(obraz):
    hist = obraz.histogram()
    plt.title("histogram  ")
    # plt.bar(range(768), hist)
    plt.bar(range(256), hist[:256], color='r', alpha=0.5)
    plt.bar(range(256), hist[256:2 * 256], color='g', alpha=0.4)
    plt.bar(range(256), hist[2 * 256:], color='b', alpha=0.3)
    plt.show()


def rysuj_histogram(obraz):
    hist = obraz.histogram()
    plt.title("histogram dla koloru zielonego ")
    plt.bar(range(256), hist[:], color='g')
    plt.savefig('hist.png')
    plt.show()


# statystyki(im)

# rysuj_histogram_RGB(im1)

# hist_r = im_r.histogram()
# hist_g = im_g.histogram()
# hist_b = im_b.histogram()
# print(f"jest {hist_g[1]} pikseli koloru 1 na kanale g")

mix110 = Image.open("test/mix212.png")
obraz10 = Image.open("test/obraz12.jpg")
print(sprawdz(obraz10, mix110))

# obraz11 = Image.open('test/obraz11.jpg')
# T_1 = np.array(obraz11)
# T_gr = T_1[:, :, 1]
# obraz11_g = Image.fromarray(T_gr)


# hist_gr = obraz11_g.histogram()
# print(hist_gr[50])
# pokaz_roznice(obraz11, obraz11).show()

# rysuj_histogram(obraz11_g)
# rysuj_histogram(im_r)
# rysuj_histogram(im_g)
# rysuj_histogram(im_b)

# beksinski1 = Image.open('pliki/beksinski1.png')
# r, g, b = beksinski1.split() są 4 kanały w pliki beksinski1.png

# def szary(w, h):
#     t = (h, w)
#     tab = np.zeros(t, dtype=np.uint8)
#     for i in range(h):
#         for j in range(w):
#             tab[i][j] = (i + 3 * j) % 256
#     return Image.fromarray(tab)
#
#
# obraz9 = Image.open('test/obraz9.jpg')
# w1, h1 = obraz9.size
# obraz_szary = szary(w1, h1)
# obR, obG, obB = obraz9.split()
# mix9 = Image.merge('RGB', (obraz_szary, obG, obB))
# mix9.save('mix.png')
