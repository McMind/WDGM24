from PIL import Image  # Python Imaging Library
import numpy as np

inicjaly = Image.open("pliki/bs.bmp")  # wczytywanie obrazu


def rysuj_ramke_w_obrazie(obraz, grub):
    tab_obraz = np.asarray(obraz).astype(np.uint8)
    h, w = tab_obraz.shape
    for i in range(h):
        for j in range(grub):
            tab_obraz[i][j] = 0
        for j in range(w - grub, w):
            tab_obraz[i][j] = 0
    for j in range(w):
        for i in range(grub):
            tab_obraz[i][j] = 0
        for i in range(h - grub, h):
            tab_obraz[i][j] = 0

    tab = tab_obraz.astype(bool)
    return Image.fromarray(tab)


def rysuj_ramki(w, h, grub):
    t = (h, w)
    tab = np.ones(t, dtype=np.uint8)
    min_dimension = min(w, h)
    liczba_paskow = min_dimension // (2 * grub) + 1
    for i in range(liczba_paskow):
        start = i * grub
        end_w = w - start
        end_h = h - start
        tab[start:end_h, start:end_w] = i % 2
    tab = tab.astype(np.bool)
    return Image.fromarray(tab)


def rysuj_pasy_pionowe(w, h, grub):
    t = (h, w)
    tab = np.ones(t, dtype=np.uint8)
    liczba_paskow = w // grub
    for i in range(liczba_paskow + 1):
        start = i * grub
        end = (i + 1) * grub
        tab[:, start:end] = i % 2
    tab = tab.astype(np.bool)
    return Image.fromarray(tab)


def rysuj_wlasne(w, h, grub):  # rysuje szlaczek od góry do dołu + łączy co pierwszy raz dół, a drugi górę (taki wąż)
    t = (h, w)
    tab = np.ones(t, dtype=np.uint8)
    liczba_paskow = w // grub
    for i in range(0, liczba_paskow + 1, 2):
        start = i * grub
        end = (i + 1) * grub
        tab[:, start:end] = 0
        if i % 4 == 0:
            tab[h - grub:h, start + grub:end + grub] = 0
        else:
            tab[0:grub, start + grub:end + grub] = 0
    tab = tab.astype(np.bool)
    return Image.fromarray(tab)


def wstaw_obraz_w_obraz(obraz_bazowy, obraz_wstawiany, m, n):
    tab_obraz = np.asarray(obraz_wstawiany).astype(np.uint8)
    (h0, w0) = tab_obraz.shape
    tab_wyjscie = np.asarray(obraz_bazowy).astype(np.uint8)
    (h, w) = tab_wyjscie.shape
    t = (h, w)
    n_k = min(h, n + h0)
    m_k = min(w, m + w0)
    n_p = max(0, n)
    m_p = max(0, m)
    for i in range(n_p, n_k):
        for j in range(m_p, m_k):
            tab_wyjscie[i][j] = tab_obraz[i - n][j - m]
    tab_wyjscie = tab_wyjscie.astype(bool)
    return Image.fromarray(tab_wyjscie)


inicjaly = rysuj_ramke_w_obrazie(inicjaly, 5)
# inicjaly.show()

rysunek1 = rysuj_ramki(50, 40, 4)
# rysunek1.show()
#
rysunek2 = rysuj_pasy_pionowe(300, 200, 15)
rysunek2.show()

rysunek3 = rysuj_wlasne(200, 100, 4)
# rysunek3.show()

rysunek4 = wstaw_obraz_w_obraz(rysunek3, rysunek1, 100, 50)
# rysunek4.show()

# im = Image.open("rysuj_ramki.bmp")
# im_arr = np.array(im).astype(np.uint8)
# print(f"{im.mode}; {im.size}; {im_arr.ndim}; {im_arr.size}")

# t1 = np.loadtxt('pliki/tablica.txt', dtype=np.bool)
# im = Image.fromarray(t1)
# im2 = rysuj_ramke_w_obrazie(im, 40)
# im2.save('im2.png')

a = Image.open('a.png')
a_tab = np.asarray(a)
print(f"{a.mode}; {a.size}; {a_tab.ndim}; {a_tab.size}")