import cv2
import numpy as np

CAM_ID = 0

#검정색 이미지를 생성
#h : 높이, w : 넓이, d : 깊이 (1 : gray, 3: bgr)

def create_image(h, w, d):
    image = np.zeros((h, w,  d), np.uint8)
    color = tuple(reversed((0, 0, 0)))
    image[:] = color
    return image

#검정색 이미지를 생성 단 배율로 더 크게
#hcout : 높이 배수(2: 세로로 2배), wcount : 넓이 배수 (2: 가로로 2배)
def create_image_multiple(h, w, d, hcout, wcount):
    image = np.zeros((h*hcout, w*wcount,  d), np.uint8)
    color = tuple(reversed((0, 0, 0)))
    image[:] = color
    return image

#통이미지 하나에 원하는 위치로 복사(표시)
#dst : create_image_multiple 함수에서 만든 통 이미지
#src : 복사할 이미지
#h : 높이, w : 넓이, d : 깊이, col : 행 위치(0부터 시작), row : 열 위치(0부터 시작)
def showMultiImage(dst, src, h, w, d, col, row):
    # 3 color
    if d == 3:
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w] = src[0:h, 0:w]
    # 1 color
    elif d == 1:
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 0] = src[0:h, 0:w]
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 1] = src[0:h, 0:w]
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 2] = src[0:h, 0:w]



##### 코드 시작 ####
cam = cv2.VideoCapture(CAM_ID) #카메라 생성

if not cam.isOpened(): #카메라 생성 확인
    print ('Can\'t open the CAM(%d)' % (CAM_ID))
    exit()

#윈도우 생성 및 사이즈 변경
cv2.namedWindow('multiView')

while True:
    #카메라에서 이미지 얻기
    #ret, frame = cam.read()
    frame = cv2.imread("/Users/leejinwoo/Desktop/color.png", cv2.IMREAD_ANYCOLOR)
    # 이미지 높이
    height = frame.shape[0]
    # 이미지 넓이
    width = frame.shape[1]
    # 이미지 색상 크기
    depth = frame.shape[2]

    #흑백으로 변경
    #grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #밝기 평균 분포
    #grayframe = cv2.equalizeHist(grayframe)

    #median 필터 적용
    #blur = cv2.medianBlur(grayframe, 5)

    #ret, th1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    #th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    #th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

    lower_red = np.array([150, 15, 60])
    upper_red = np.array([180, 255, 255])
    hsv_red_mask = cv2.inRange(hsv, lower_red, upper_red)

    lower_blue = np.array([90, 15, 40])
    upper_blue = np.array([120, 255, 255])
    hsv_blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_green = np.array([45, 15, 50])
    upper_green = np.array([80, 255, 255])
    hsv_green_mask = cv2.inRange(hsv, lower_green, upper_green)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 50])
    hsv_black_mask = cv2.inRange(hsv, lower_black, upper_black)

    lower_yellow = np.array([0, 80, 110])
    upper_yellow = np.array([50, 255, 255])
    #hsv_lw = np.array([l_h.get(), l_s.get(), l_v.get()])
    #hsv_up = np.array([u_h.get(), u_s.get(), u_v.get()])
    hsv_mask_rb = cv2.bitwise_or(hsv_red_mask, hsv_blue_mask)
    hsv_mask_rbg = cv2.bitwise_or(hsv_mask_rb, hsv_green_mask)
    hsv_mask_rbgd = cv2.bitwise_or(hsv_mask_rbg, hsv_black_mask)
    hsv_res = cv2.bitwise_and(frame, frame, mask=hsv_mask_rbgd)
    #hsv_rgb = cv2.cvtColor(hsv_res, cv2.COLOR_BGR2RGB)

    '''
    YCrCb_lw = np.array([l_h.get(), l_s.get(), l_v.get()])
    YCrCb_up = np.array([u_h.get(), u_s.get(), u_v.get()])
    YCrCb_mask = cv2.inRange(YCrCb, YCrCb_lw, YCrCb_up)
    YCrCb_res = cv2.bitwise_and(frame, frame, mask=YCrCb_mask)
    YCrCb_rgb = cv2.cvtColor(YCrCb_res, cv2.COLOR_BGR2RGB)'''

    # 화면에 표시할 이미지 만들기 ( 2 x 2 )
    dstImage = create_image_multiple(height, width, depth, 2, 2)

    # 원하는 위치에 복사
    #왼쪽 위에 표시(0,0)
    showMultiImage(dstImage, frame, height, width, depth, 0, 0)
    #오른쪽 위에 표시(0,1)
    showMultiImage(dstImage, hsv_mask_rbgd, height, width, 1, 0, 1)
    #왼쪽 아래에 표시(1,0)
    showMultiImage(dstImage, hsv_res, height, width, depth, 1, 0)
    #오른쪽 아래에 표시(1,1)
    #showMultiImage(dstImage, hsv_mask, height, width, 1, 1, 1)

    # 화면 표시
    cv2.imshow('multiView', dstImage)

    #1ms 동안 키입력 대기 ESC키 눌리면 종료
    if cv2.waitKey(1) == 27:
        break

#윈도우 종료
cam.release()
cv2.destroyWindow('multiView')