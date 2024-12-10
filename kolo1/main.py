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
    if obraz1.mode != obraz2.mode or obraz1.size != obraz2.size:
        return False
    diff = chops.difference(obraz1, obraz2)
    tab = np.asarray(diff, np.bool)
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


def statystyki(im):
    s = stat.Stat(im)
    print("extrema ", s.extrema)  # max i min
    print("count ", s.count)  # zlicza
    print("mean ", s.mean)  # srednia
    print("median ", s.median)  # mediana
    print("stddev ", s.stddev)  # odchylenie standardowe


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


def rysuj_ramke_kolor(w, h, grub, kolor):
    t = (h, w, 3)
    tab = np.ones(t, dtype=np.uint8)
    tab[:] = kolor
    z1 = h - grub
    z2 = w - grub
    tab[grub:z1, grub:z2] = 100, 200, 30
    return tab


def odkoduj(obraz1, obraz2):
    t_obraz1 = np.asarray(obraz1, np.int16)
    t_obraz2 = np.asarray(obraz2, np.int16)
    if t_obraz1.shape != t_obraz2.shape:
        raise TypeError("różne wymiary obrazów")
    h, w, d = t_obraz1.shape
    wynik = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            for k in range(d):
                a = t_obraz1[i, j, k]
                b = t_obraz2[i, j, k]
                if abs(a - b) in (1, 255):
                    wynik[i, j] = 255
                    break

    return Image.fromarray(wynik.astype(np.uint8))


def plot_color_histogram(image, channel):
    image_data = np.array(image)
    if channel == 'r':
        channel_data = image_data[:, :, 0]
    elif channel == 'g':
        channel_data = image_data[:, :, 1]
    elif channel == 'b':
        channel_data = image_data[:, :, 2]
    else:
        return

    plt.figure(figsize=(10, 3))
    plt.hist(channel_data.flatten(), bins=256, color=channel, alpha=0.7)
    plt.title(f'histogram kanału {channel}')
    plt.xlabel('Wartość')
    plt.ylabel('Ilość')
    plt.grid(True)
    plt.show()


def rysuj_histogram(obraz):
    hist = obraz.histogram()
    plt.title("histogram  ")
    plt.figure(figsize=(6, 2))
    plt.bar(range(256), hist[:])
    plt.show()


bek1 = Image.open('pliki/obrazki/bek1.png')
bek2 = Image.open('pliki/obrazki/bek2.png')
bek3 = Image.open('pliki/obrazki/bek3.png')
bek1_r, bek1_g, bek1_b = bek1.split()
bek2_r, bek2_g, bek2_b = bek2.split()
bek3_r, bek3_g, bek3_b = bek3.split()
rysuj_histogram(bek3_b)
# rysuj_histogram(bek1_g)
# rysuj_histogram(bek2_b)
# rysuj_histogram(bek2_r)

#plot_color_histogram(bek2, 'b')

t1 = np.loadtxt('pliki/tablice/tab1.txt', dtype=np.bool)
im = Image.fromarray(t1)
bat = Image.open('pliki/obrazki/batman2.png')
w1, h1 = bat.size
w2, h2 = im.size


# im.show()

def wstaw_obraz_w_obraz(obraz_bazowy, obraz_wstawiany, m, n):
    tab_obraz = np.asarray(obraz_wstawiany).astype(np.bool)
    (h0, w0) = tab_obraz.shape
    tab_wyjscie = np.asarray(obraz_bazowy).astype(np.uint8)
    (h, w, c) = tab_wyjscie.shape
    n_k = min(h, n + h0)
    m_k = min(w, m + w0)
    n_p = max(0, n)
    m_p = max(0, m)
    for i in range(n_p, n_k):
        for j in range(m_p, m_k):
            if not tab_obraz[i - n][j - m]:
                tab_wyjscie[i][j] = (0, 0, 0)
            else:
                tab_wyjscie[i][j] = (255, 255, 0)
    return Image.fromarray(tab_wyjscie)


wyjscie = wstaw_obraz_w_obraz(bat, im, 0, h1 - h2)
# wyjscie.save('wyjscie.png')
