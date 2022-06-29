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
                    im_np[i][k][1] = im_np[i - 1][k][1]
                    im_np[i][k][2] = im_np[i - 1][k][2]
                    k = k + 1


def blocking(im_np, w, h):
    not_real_w = w // 8
    not_real_h = h // 8
    real_w = 0
    real_h = 0
    im_np_full = im_np
    # finding the metrics for how much unrealistic data is given to block.
    if w % 8 == 0:
        real_w = not_real_w
    if h % 8 == 0:
        real_h = not_real_h
    elif w % 8 != 0:
        real_w = not_real_w + 1

    elif h % 8 != 0:
        real_h = not_real_h + 1
        print(real_h)
        print(not_real_h)
        difference = 8 - (h % 8)  # making the difference to append the black cells to full the array.
        print(difference) # it has to make three row with 0 0 0 in each channel.
        k = 0
        #an_array2 = [[0 for i in range(difference)] for j in range(w)]
        an_array2 = np.full((difference,w,3), 0)
        im_np_full = np.append(im_np_full, an_array2, 0)
        """""
        print("before:")
        print(im_np_full[h-1])
        im_np_full = np.append(im_np_full,an_array2,0)
        print("after")

        print(im_np_full[not_real_h*8 - 1 ][not_real_w-1])
        print("a whole section after update>>>>>")
        print(real_h * 8-4)
        print(im_np_full[real_h * 8-4])
        """

    # making array map for feeding the blocks with unrealistic data added.

    block_y = [[0 for i in range(8)] for j in range(8)]
    print(block_y)
    blocks_yy = np.full((real_h,real_w,8,8), 0)
    block_cb = [[0 for i in range(8)] for j in range(8)]
    block_cr = [[0 for i in range(8)] for j in range(8)]
    blocks_cb = np.full((real_h, real_w, 8, 8), 0)
    blocks_cr = np.full((real_h, real_w, 8, 8), 0)

    for i in range(0,real_h):
        for j in range(0,real_w):
            for k in range(0, 8):
                for f in range(0, 8):
                    # print(type(im_np[k + i * 8 ][f + j * 8][0]))
                    # print(block_y)
                    # print(type(block_y[0][0]))
                    block_y[k][f] = im_np_full[k + i * 8][f + j * 8][0]
                    block_cb[k][f] = im_np_full[k + i * 8][f + j * 8][1]
                    block_cr[k][f] = im_np_full[k + i * 8][f + j * 8][2]
                    # print("index i and j for block_y ----->  ",k,f,)
                    # print("index in actual array --------> ",k + (i * 8),f + (j * 8))
                    # print("data that has been added",im_np[k + i * 8 ][f + j * 8][0])
            blocks_yy[i][j] = block_y
            blocks_cb[i][j] = block_cb
            blocks_cr[i][j] = block_cr

            """""
            print("one block has been created")
            print(block_y)
            print("the block is above")
            print("index i and j for blockssssss_y ----->  ", i, j, )
           
            print(blocks_yy[i][j - 1])
            print("before blockssss||||")
            print(blocks_yy[i][j])
            print("now blockssssss ||||")

    print("now block checker in luminance:>>>>")
    print(blocks_yy[0][0][0][0])
    print(blocks_yy[1][1][7][7])
    print("start and end to check:>>>>>>>>")
    print(im_np[0][0][0],im_np[15][15][0])
    print("last block check :>>>")
    print(blocks_yy[real_h-1][real_w-1])
    # print(real_h,real_w)
    """""
    print("luminance maintenance blocks>>>>")
    print(blocks_yy[real_h-1][real_w-1])
    print("chrominance blue section maintenance blocks>>>>")
    print(blocks_cb[real_h - 1][real_w - 1])
    print("chrominance red section maintenance blocks>>>>")
    print(blocks_cr[real_h - 1][real_w - 1])


if __name__ == '__main__':
    # x = input('directory :')
    x = "photo1.png"
    im = Image.open(x)
    w, h = im.size
    # w ------> j for pixel array , h -------> i for pixel array.
    im_np = np.asarray(im)
    im_ycbcr = rgb2ycbcr(im_np)
    chromaSubFourTwo(im_ycbcr, w, h)
    print(im_ycbcr[0][0][1],im_ycbcr[0][1][1])
    im_ycbcr_copy = im_ycbcr
    print("top after  ", im_ycbcr[240][4])
    print("bottom after ", im_ycbcr[241][4])
    print(blocking(im_ycbcr, w, h))
