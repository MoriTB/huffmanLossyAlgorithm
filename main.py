import numpy as np
from PIL import Image


def rgb2ycbcr(im):
    xform = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
    ycbcr = im.dot(xform.T)
    ycbcr[:, :, [1, 2]] += 128
    return np.uint8(ycbcr)


def chromaSubFourTwo(im_np, w, h):
    for i in range(0, h - 1, 1):
        for j in range(0, w - 1, 4):
            if i % 2 == 0:
                im_np[i][j + 1][1] = im_np[i][j][1]  # matching color on cy section ( row - equalization )
                im_np[i][j + 1][2] = im_np[i][j][2]  # matching color on cr section ( row - equalization )
                im_np[i][j + 3][1] = im_np[i][j + 2][1]  # matching color on cy section ( row - equalization )
                im_np[i][j + 3][2] = im_np[i][j + 2][2]  # matching color on cr section ( row - equalization )
            else:
                k = j
                while k < j + 4:  # matching the down rows to upper rows.
                    im_np[i][k][1] = im_np[i-1][k][1]
                    im_np[i][k][2] = im_np[i - 1][k][2]
                    k = k + 1



if __name__ == '__main__':
    # x = input('directory :')
    x = "photo1.png"
    im = Image.open(x)
    w, h = im.size
    # w ------> j for pixel array , h -------> i for pixel array.
    im_np = np.asarray(im)
    im_ycbcr = rgb2ycbcr(im_np)
    print("top before  ",im_ycbcr[240][4])
    print("bottom before ",im_ycbcr[241][4])
    chromaSubFourTwo(im_ycbcr,w,h)
    print("top after  ", im_ycbcr[240][4])
    print("bottom after ", im_ycbcr[241][4])
