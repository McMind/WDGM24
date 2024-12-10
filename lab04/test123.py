from PIL import Image
import numpy as np
from PIL import ImageChops as chops
from PIL import ImageStat as stat
import matplotlib.pyplot as plt

im = Image.open('og.png')

T = np.array(im)
t_r = T[:, :, 0]
t_g = T[:, :, 1]
t_b = T[:, :, 2]
im_r = Image.fromarray(t_r)
im_g = Image.fromarray(t_g)
im_b = Image.fromarray(t_b)

im1 = Image.merge('RGB', (im_r, im_g, im_b))
im1.save('im1.png')
diff1 = chops.difference(im, im1)

plt.figure(figsize=(12,3))
plt.subplot(1,3,1)
plt.imshow(im)
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(im1)
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(diff1)
plt.axis('off')
plt.subplots_adjust(wspace=0.05, hspace=0.05)
plt.savefig('fig1.png')
