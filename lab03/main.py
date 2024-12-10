from PIL import Image
import numpy as np


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


obrazek_z_ramkami_szarymi = rysuj_ramki_szare(300, 200, 15, 50)


# obrazek_z_ramkami_szarymi.show()


def rysuj_pasy_pionowe_szare(w, h, grub, zmiana_koloru):
    t = (h, w)
    tab = np.ones(t, dtype=np.uint8)
    ile = w // grub
    for k in range(ile):
        for g in range(grub):
            j = k * grub + g
            for i in range(h):
                tab[i, j] = (k + zmiana_koloru) % 256
    return Image.fromarray(tab)


im_paski = rysuj_pasy_pionowe_szare(246, 100, 1, 10)


# im_paski.show()

def negatyw(obraz: Image) -> Image:
    tab = np.asarray(obraz)
    tab_neg = tab.copy()
    match obraz.mode:
        case 'L':
            h, w = tab.shape
            for i in range(h):
                for j in range(w):
                    tab_neg[i, j] = 255 - tab[i, j]
        case '1':
            h, w = tab.shape
            for i in range(h):
                for j in range(w):
                    tab_neg[i, j] = 1 - tab_neg[i, j]
        case 'RGB':
            h, w, b = tab.shape
            for i in range(h):
                for j in range(w):
                    for k in range(b):
                        tab_neg[i, j, k] = 255 - tab_neg[i, j, k]
        case 'RGBA':
            h, w, b = tab.shape
            for i in range(h):
                for j in range(w):
                    tab_neg[i, j] = tuple(255 - tab_neg[i, j, k] if k < 3 else tab_neg[i, j, k] for k in range(4))
        case _:
            raise TypeError("Nie obsługiwany format obrazu")
    return Image.fromarray(tab_neg)


# inicjaly = Image.open('pliki/inicjaly.bmp')
# kolorowy = Image.open('pliki/kolorowy.jpg')
# transparent = Image.open('pliki/transparent.png')
# tab_transparent = np.asarray(transparent)


# print(transparent.mode)


# obraz_neg = negatyw(im_paski)
# obraz_neg2 = negatyw(inicjaly)
# obraz_neg3 = negatyw(transparent)
# # # obraz_neg.show()
# # # obraz_neg2.show()
# obraz_neg3.show()


def koloruj_w_paski(obraz, grub, kolor, zmiana_koloru):
    t_obraz = np.asarray(obraz)
    h, w = t_obraz.shape
    t = (h, w, 3)
    tab = np.ones(t, dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            if not t_obraz[i, j]:
                tab[i, j] = tuple((kolor[k] + zmiana_koloru * (i // grub)) % 256 for k in range(3))
            else:
                tab[i, j] = [255, 255, 255]
    return Image.fromarray(tab)


# gwiazdka = Image.open("pliki/gwiazdka.bmp")
# obraz3 = koloruj_w_paski(gwiazdka, 10,[120, 240, 50],32)
# obraz3.show()

# inicjaly = Image.open('pliki/inicjaly.bmp')

# inicjaly.save("inicjaly_og.bmp")
# kolory_w_paski = koloruj_w_paski(inicjaly, 5, [42, 197, 245], -25)
# kolory_w_paski.save('inicjaly.png')
# kolory_w_paski.save('inicjaly.jpg')