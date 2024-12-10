from PIL import Image


def rysuj_kwadrat_max(obraz, m, n, k):
    obraz1 = obraz.copy()
    pix1 = obraz1.load()
    d = k // 2
    temp = [0, 0, 0]
    for a in range(k):
        for b in range(k):
            x = m + a - d
            y = n + b - d
            pixel = pix1[x, y]
            temp = [max(p, t) for p, t in zip(pixel, temp)]
    for a in range(k):
        for b in range(k):
            x = m + a - d
            y = n + b - d
            pix1[x, y] = (temp[0], temp[1], temp[2])
    return obraz1


def rysuj_kwadrat_min(obraz, m, n, k):
    obraz1 = obraz.copy()
    pix1 = obraz1.load()
    d = k // 2
    temp = [255, 255, 255]
    for a in range(k):
        for b in range(k):
            x = m + a - d
            y = n + b - d
            pixel = pix1[x, y]
            temp = [min(p, t) for p, t in zip(pixel, temp)]
    for a in range(k):
        for b in range(k):
            x = m + a - d
            y = n + b - d
            pix1[x, y] = (temp[0], temp[1], temp[2])
    return obraz1


def zakres(w, h):
    return [(i, j) for i in range(w) for j in range(h)]


def wycinek_kolo(obraz, m_s, n_s, r, m_cel=None, n_cel=None):
    kolo = Image.new('RGB', (r * 2, r * 2), (0, 0, 0))
    obraz1 = obraz.copy()
    w, h = obraz1.size
    for i, j in zakres(r * 2, r * 2):
        oryg_i, oryg_j = m_s - r + i, n_s - r + j

        if 0 <= oryg_i < w and 0 <= oryg_j < h:
            if (i - r) ** 2 + (j - r) ** 2 < r ** 2:
                kolo.putpixel((i, j), obraz1.getpixel((oryg_i, oryg_j)))
    if m_cel is None or n_cel is None:  # zwróć sam wycinek, jeśli nie podano koordynatów celu
        return kolo
    for i, j in zakres(r * 2, r * 2):
        cel_i, cel_j = m_cel - r + i, n_cel - r + j

        if 0 <= cel_i < w and 0 <= cel_j < h:
            if (i - r) ** 2 + (j - r) ** 2 < r ** 2:
                obraz1.putpixel((cel_i, cel_j), kolo.getpixel((i, j)))
    return obraz1


def rysuj_kolo(obraz, m_s, n_s, x, y, r):
    obraz1 = obraz.copy()
    w, h = obraz.size
    for i, j in zakres(w, h):
        if (i - m_s) ** 2 + (j - n_s) ** 2 < r ** 2:  # wzór na koło o środku (m_s, n_s) i promieniu r
            obraz1.putpixel((i, j), obraz1.getpixel((i - m_s + x, j - n_s + y)))
    return obraz1


def odbij_w_pionie(obraz):
    img = obraz.copy()
    px0 = obraz.load()
    w, h = obraz.size
    px = img.load()
    for i in range(w):
        for j in range(h):
            px[i, j] = px0[w - 1 - i, j]
    return img


def odbij_w_pionie2(obraz):
    img = obraz.copy()
    w, h = obraz.size
    px = img.load()
    for i in range(w):
        for j in range(h):
            px[i, j] = px[w - 1 - i, j]
    return img


def odbij_w_poziomie(obraz):
    px0 = obraz.load()
    img = obraz.copy()
    w, h = obraz.size
    px = img.load()
    for i in range(w):
        for j in range(h):
            px[i, j] = px0[i, h - 1 - j]
    return img


def odbij_dol_na_gore(obraz):
    img = obraz.copy()
    w, h = obraz.size
    h_s = h // 2
    px = img.load()
    for i in range(w):
        for j in range(0, h_s):
            px[i, j] = px[i, h - 1 - j]
    return img


def odbij_gore_na_dol(obraz):
    img = obraz.copy()
    w, h = obraz.size
    h_s = h // 2
    px = img.load()
    for i in range(w):
        for j in range(h_s, h):
            px[i, j] = px[i, h - 1 - j]
    return img


im = Image.open('obraz.png')
# im2 = rysuj_kwadrat_max(im, 10, 15, 9)
# im2 = rysuj_kwadrat_max(im2, 70, 15, 11)
# im2 = rysuj_kwadrat_max(im2, 15, 70, 13)
# im2.save('obraz1.png')
# im3 = rysuj_kwadrat_min(im, 10, 15, 9)
# im3 = rysuj_kwadrat_min(im3, 70, 15, 11)
# im3 = rysuj_kwadrat_min(im3, 15, 70, 13)
# im3.save('obraz2.png')
# im4 = wycinek_kolo(im, 65, 195, 8, 83, 266)
# im4.save('obraz3.png')
# im5 = wycinek_kolo(im, 65, 195, 8, 2, 346)
# im5 = wycinek_kolo(im5, 65, 195, 8, 4, 298)
# im5 = wycinek_kolo(im5, 65, 195, 8, 33, 331)
# im5 = wycinek_kolo(im5, 65, 195, 8, 35, 365)
im5 = rysuj_kolo(im, 2, 346, 65, 195, 8)
im5 = rysuj_kolo(im5, 4, 298, 65, 195, 8)
im5 = rysuj_kolo(im5, 33, 331, 65, 195, 8)
im5 = rysuj_kolo(im5, 33, 365, 65, 195, 8)
im5.show()
# im5.save('obraz4.png')
# odbij_w_poziomie(im)
# odbij_dol_na_gore(im)
# odbij_gore_na_dol(im)
