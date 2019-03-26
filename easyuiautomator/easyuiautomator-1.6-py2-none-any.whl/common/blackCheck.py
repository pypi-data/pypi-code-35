#coding=utf-8
try:
    import cv2
except:
    pass

#   rmBlackBorder: remove the black borders of one image
#   return: cropped image
def _rmBlackBorder(
    src,  # input image
    thres=0,  # threshold for cropping: sum([r,g,b] - [0,0,0](black))
    diff=1000,  # max tolerable difference between black borders on two side
    shrink=0,  # number of pixels to shrink after the blackBorders removed
    directionMore=0,  # 哪个方向上多出不对称的内容，0：正常，1：上，2：下,3：左，4：右
    ):
    
    #
    #   remove the black border on both right and left side
    #
    srcCol = src.shape[1]
    srcRow = src.shape[0]
    nRow = src.shape[0]
    nCol = src.shape[1]
    left = -1
    right = nCol

    for i in [0, nRow / 2, nRow - 1]:
        curLeft = -1
        curRight = nCol
        for j in range(0, nCol - 1):
            if(sum(list(src[i, j])) <= thres and curLeft == j - 1):
                curLeft += 1
        if left == -1:
            left = curLeft
        if curLeft < left:
            left = curLeft

        for j in range(nCol - 1, 0, -1):
            if(sum(list(src[i, j])) <= thres and curRight == j + 1):
                curRight -= 1
        if right == nCol:
            right = curRight
        if curRight > right:
            right = curRight
    
    if min(left, right) >= 1 and abs((left + 1) - (nCol - right)) <= diff and right - left > 0 :
        print 'left margin: %d\n' % left
        print 'right margin: %d\n' % right
        
        if directionMore == 3:
            left = srcCol - right                    
        elif directionMore == 4:
            right = srcCol - left
        
        src = src[0 : nRow - 1, left + 1 + shrink : right - 1 - shrink, :]
    else:
        src = src

    #
    #   remove the black border on both up and down side
    #
    nRow = src.shape[0]
    nCol = src.shape[1]
    up = -1
    down = nRow    
    for j in [0, nCol / 2, nCol - 1]:
        curUp = -1
        curDown = nRow
        for i in range(0, nRow - 1):
            if(sum(list(src[i, j])) <= thres and curUp == i - 1):
                curUp += 1
        if up == -1:
            up = curUp
        if curUp < up:
            up = curUp
        for i in range(nRow - 1, 0, -1):
            if(sum(list(src[i, j])) <= thres and curDown == i + 1):
                curDown -= 1
        if down == nRow:
            down = curDown
        if curDown > down:
            down = curDown    
    if min(up, down) >= 1 and abs((up + 1) - (nRow - down)) <= diff and down - up > 0:
        if directionMore == 4 or directionMore == 1:
            up = srcRow - down
        elif directionMore == 3 or directionMore == 2:
            down = srcRow - up         
        print 'up margin: %d\n' % up
        print 'down margin: %d\n' % down
        dst = src[up + 1 + shrink : down - 1 - shrink, 0 : nCol - 1, :]
    else:
        dst = src
    return dst


def blackBorderCheck(
            srcpath,  # input image
            tarpath,
            thres,  # threshold for cropping: sum([r,g,b] - [0,0,0](black))
            diff,  # max tolerable difference between black borders on two side
            shrink,  # number of pixels to shrink after the blackBorders removed
            directionMore,  # 哪个方向上多出不对称的内容，0：正常，1：上，2：下,3：左，4：右
            ):

    src = cv2.imread(srcpath)    
    res = _rmBlackBorder(src,thres, diff, shrink, directionMore)
    cv2.imwrite(tarpath, res)




if __name__ == '__main__':
    path = r"C:\Program Files\AutoRecorder\workspace\test_tool\tools\test.png"
    path2 = r"C:\Program Files\AutoRecorder\workspace\test_tool\tools\test2.png"
    print blackBorderCheck(path, path2, 50,1000,0,0)

