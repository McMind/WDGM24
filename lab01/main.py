from PIL import Image
import numpy as np

im = Image.open("pliki/inicjaly.bmp")
print(f"Tryb: {im.mode}")
print(f"Format: {im.format}")
print(f"Rozmiar: {im.size}")
im_arr = np.array(im).astype(np.uint8)
f = open("pliki/inicjaly.txt", "w")
for rows in im_arr:
    for item in rows:
        f.write(str(item) + ' ')
    f.write("\n")
f.close()
print(f"Wartość pixela (50,30): {im_arr[30][50]}")
print(f"Wartość pixela (90,40): {im_arr[40][90]}")
print(f"Wartość pixela (99,0): {im_arr[0][99]}")
print(f"Wartość pixela (20,7): {im_arr[7][20]}")

t1 = np.loadtxt("pliki/inicjaly.txt", dtype=np.bool)
print(f"Sprawdź bool: {np.array_equal(t1, im_arr)}")
t2 = np.loadtxt("pliki/inicjaly.txt", dtype=np.uint8)
im_arr = np.array(im)
print(f"Uint8 z pliku txt: {t2.dtype}")
print(f"Z pliku bmp: {im_arr.dtype}")
print(f"Sprawdź uint8: {np.array_equal(t2, im_arr)}")
Image.fromarray(t2).save("pliki/t2.png")


