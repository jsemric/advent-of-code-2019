import numpy as np
import matplotlib.pyplot as plt
from utils import lmap


def main():
    img = lmap(int, input())
    img = np.array(img)
    img.shape = (-1, 6, 25)

    nz = np.sum(img == 0, axis=1).sum(axis=1)
    a = img[np.argmin(nz)]
    print('1.)', np.equal(a, 1).sum() * np.equal(a, 2).sum())

    a = np.ones(img.shape[1:])*2
    mask = np.zeros(img.shape[1:]).astype(bool)
    for i in img:
        a[mask] = i[mask]
        mask = a == 2
    plt.imshow(a)
    plt.show()

if __name__ == '__main__':
    main()
