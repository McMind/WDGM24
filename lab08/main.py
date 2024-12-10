from PIL import Image, ImageFilter, ImageChops, ImageStat
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

im = Image.open('obraz.png')


def konwolucja(obraz: np.array, kernel: np.array, scale: int):
    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2
    pad_img = np.pad(obraz, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    obraz_wyjsciowy = obraz.copy()
    w, h = obraz.shape
    for m in range(pad_w, w - pad_w):
        for n in range(pad_h, h - pad_h):
            region = pad_img[m:m + k_h, n:n + k_w]
            obraz_wyjsciowy[m, n] = round((np.sum(region * kernel) / scale))
    return obraz_wyjsciowy


def filtruj(obraz: Image, kernel: tuple, scale: int = 0):
    im_copy = obraz.copy()
    kernel = np.array(kernel)
    if scale == 0:
        scale = np.sum(kernel)
    kernel_size = sqrt(kernel.size)
    if kernel_size != int(kernel_size):
        raise ValueError('Ilość elementów w jądrze po spierwiastkowaniu musi być liczbą całkowitą')
    kernel_size = int(kernel_size)
    kernel_2d = kernel.reshape(kernel_size, kernel_size)
    img_arr = np.array(im_copy, dtype=np.int32)
    if len(img_arr.shape) == 3:
        channels = []
        for c in range(3):
            channel = konwolucja(img_arr[:, :, c], kernel_2d, scale)
            channels.append(channel)
        tab_wyjsciowy = np.stack(channels, axis=2)
    else:
        tab_wyjsciowy = konwolucja(img_arr, kernel_2d, scale)

    tab_wyjsciowy = np.clip(tab_wyjsciowy, 0, 255).astype(np.uint8)
    obraz_wyjsciowy = Image.fromarray(tab_wyjsciowy)
    return obraz_wyjsciowy


def takie_same(obraz1, obraz2):  # zwraca True gdy obrazy są takie same lub False w przeciwnym wypadku
    diff = ImageChops.difference(obraz1, obraz2)
    tab = np.asarray(diff, np.bool)
    if obraz1.mode != obraz2.mode or obraz1.size != obraz2.size:
        return False
    return not np.any(tab)


def pokaz_roznice(obraz1, obraz2):  # wyrzuca obraz z ImageChops tylko używa do tego czarno białego obrazu,
    # tam gdzie jest różnica pixel będzie biały, w przeciwnym wypadku czarny
    if takie_same(obraz1, obraz2):
        return Image.fromarray(np.zeros(obraz1.size, dtype=np.bool))
    diff = ImageChops.difference(obraz1, obraz2)
    tab = np.asarray(diff, np.bool)
    tab2d = np.all(tab, axis=2)
    return Image.fromarray(tab2d)


def statystyki(obraz):
    s = ImageStat.Stat(obraz)
    print("extrema ", s.extrema)  # max i min
    print("count ", s.count)  # zlicza
    print("mean ", s.mean)  # srednia
    print("median ", s.median)  # mediana
    print("stddev ", s.stddev)  # odchylenie standardowe
    return


# im1_BLUR = im.filter(ImageFilter.BLUR)
# print(ImageFilter.BLUR.filterargs)
# im2_BLUR = filtruj(im, (1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1), 16)
# diff_BLUR = ImageChops.difference(im1_BLUR, im2_BLUR)
# plt.figure(figsize=(16, 8))
# plt.subplot(1, 4, 1)
# plt.title("oryginalny")
# plt.imshow(im)
# plt.axis('off')
# plt.subplot(1, 4, 2)
# plt.title("im.filter(ImageFilter.BLUR)")
# plt.imshow(im1_BLUR)
# plt.axis('off')
# plt.subplot(1, 4, 3)
# plt.title("funkcja filtruj()")
# plt.imshow(im2_BLUR)
# plt.axis('off')
# plt.subplot(1, 4, 4)
# plt.title("różnica")
# plt.imshow(diff_BLUR)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig1.png')
# plt.show()
# statystyki(diff_BLUR)

# im_L = im.convert('L')
# im_EMBOSS = im_L.filter(ImageFilter.EMBOSS)
# print(ImageFilter.EMBOSS.filterargs)
# im_SOBEL1 = im_L.filter(ImageFilter.Kernel((3, 3), (-1, 0, 1, -2, 0, 2, -1, 0, 1), 1, 128))
# im_SOBEL2 = im_L.filter(ImageFilter.Kernel((3, 3), (-1, -2, -1, 0, 0, 0, 1, 2, 1), 1, 128))

# plt.figure(figsize=(16, 8))
# plt.subplot(1, 4, 1)
# plt.title("po konwersji na L")
# plt.imshow(im_L, cmap='gray', vmin=0, vmax=255)
# plt.axis('off')
# plt.subplot(1, 4, 2)
# plt.title("EMBOSS")
# plt.imshow(im_EMBOSS, cmap='gray', vmin=0, vmax=255)
# plt.axis('off')
# plt.subplot(1, 4, 3)
# plt.title("SOBEL1")
# plt.imshow(im_SOBEL1, cmap='gray', vmin=0, vmax=255)
# plt.axis('off')
# plt.subplot(1, 4, 4)
# plt.title("SOBEL2")
# plt.imshow(im_SOBEL2, cmap='gray', vmin=0, vmax=255)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig2.png')
# plt.show()

# im_DETAIL = im.filter(ImageFilter.DETAIL)
# im_EDGE_ENHANCE_MORE = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
# im_SHARPEN = im.filter(ImageFilter.SHARPEN)
# im_SMOOTH_MORE = im.filter(ImageFilter.SMOOTH_MORE)
# diff_DETAIL = ImageChops.difference(im, im_DETAIL)
# diff_EDGE_ENHANCE_MORE = ImageChops.difference(im, im_EDGE_ENHANCE_MORE)
# diff_SHARPEN = ImageChops.difference(im, im_SHARPEN)
# diff_SMOOTH_MORE = ImageChops.difference(im, im_SMOOTH_MORE)

# plt.figure(figsize=(16, 40))
# plt.subplot(4, 2, 1)
# plt.title("DETAIL")
# plt.imshow(im_DETAIL)
# plt.axis('off')
# plt.subplot(4, 2, 2)
# plt.title("różnica")
# plt.imshow(diff_DETAIL)
# plt.axis('off')
# plt.subplot(4, 2, 3)
# plt.title("EDGE_ENHANCE_MORE")
# plt.imshow(im_EDGE_ENHANCE_MORE)
# plt.axis('off')
# plt.subplot(4, 2, 4)
# plt.title("różnica")
# plt.imshow(diff_EDGE_ENHANCE_MORE)
# plt.axis('off')
# plt.subplot(4, 2, 5)
# plt.title("SHARPEN")
# plt.imshow(im_SHARPEN)
# plt.axis('off')
# plt.subplot(4, 2, 6)
# plt.title("różnica")
# plt.imshow(diff_SHARPEN)
# plt.axis('off')
# plt.subplot(4, 2, 7)
# plt.title("SMOOTH_MORE")
# plt.imshow(im_SMOOTH_MORE)
# plt.axis('off')
# plt.subplot(4, 2, 8)
# plt.title("różnica")
# plt.imshow(diff_SMOOTH_MORE)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig3.png')
# plt.show()

# im_BoxBlur = im.filter(ImageFilter.BoxBlur((3, 1)))
# diff_BoxBlur = ImageChops.difference(im, im_BoxBlur)
# im_GaussianBlur = im.filter(ImageFilter.GaussianBlur((1, 3)))
# diff_GaussianBlur = ImageChops.difference(im, im_GaussianBlur)
# im_UnsharpMask = im.filter(ImageFilter.UnsharpMask(3, 200, 6))
# diff_UnsharpMask = ImageChops.difference(im, im_UnsharpMask)
# im_Kernel = im.filter(ImageFilter.Kernel((3, 3), (0, -2, 0, -2, 24, -2, 0, -2, 0), -16, 192))
# diff_Kernel = ImageChops.difference(im, im_Kernel)
# im_RankFilter = im.filter(ImageFilter.RankFilter(5, 20))
# diff_RankFilter = ImageChops.difference(im, im_RankFilter)
# im_MedianFilter = im.filter(ImageFilter.MedianFilter(5))
# diff_MedianFilter = ImageChops.difference(im, im_MedianFilter)
# im_MinFilter = im.filter(ImageFilter.MinFilter(3))
# diff_MinFilter = ImageChops.difference(im, im_MinFilter)
# im_MaxFilter = im.filter(ImageFilter.MaxFilter(9))
# diff_MaxFilter = ImageChops.difference(im, im_MaxFilter)

# plt.figure(figsize=(16, 48))
# plt.subplot(5, 2, 1)
# plt.title("GaussianBlur(1, 3)")
# plt.imshow(im_GaussianBlur)
# plt.axis('off')
# plt.subplot(5, 2, 2)
# plt.title("różnica")
# plt.imshow(diff_GaussianBlur)
# plt.axis('off')
# plt.subplot(5, 2, 3)
# plt.title("UnsharpMask(3, 200, 6)")
# plt.imshow(im_UnsharpMask)
# plt.axis('off')
# plt.subplot(5, 2, 4)
# plt.title("różnica")
# plt.imshow(diff_UnsharpMask)
# plt.axis('off')
# plt.subplot(5, 2, 5)
# plt.title("MedianFilter(5)")
# plt.imshow(im_MedianFilter)
# plt.axis('off')
# plt.subplot(5, 2, 6)
# plt.title("różnica")
# plt.imshow(diff_MedianFilter)
# plt.axis('off')
# plt.subplot(5, 2, 7)
# plt.title("MinFilter(3)")
# plt.imshow(im_MinFilter)
# plt.axis('off')
# plt.subplot(5, 2, 8)
# plt.title("różnica")
# plt.imshow(diff_MinFilter)
# plt.axis('off')
# plt.subplot(5, 2, 9)
# plt.title("MaxFilter(9)")
# plt.imshow(im_MaxFilter)
# plt.axis('off')
# plt.subplot(5, 2, 10)
# plt.title("różnica")
# plt.imshow(diff_MaxFilter)
# plt.axis('off')
# plt.subplots_adjust(wspace=0.05, hspace=0.05)
# plt.savefig('fig4.png')
# plt.show()
