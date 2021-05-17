import cv2
import numpy as np

def onChange(x):
    pass

def setting_bar():
    cv2.namedWindow('YCrCb')

    cv2.createTrackbar('Y_MAX', 'YCrCb', 0, 255, onChange)
    cv2.createTrackbar('Y_MIN', 'YCrCb', 0, 255, onChange)
    cv2.createTrackbar('Cr_MAX', 'YCrCb', 0, 255, onChange)
    cv2.createTrackbar('Cr_MIN', 'YCrCb', 0, 255, onChange)
    cv2.createTrackbar('Cb_MAX', 'YCrCb', 0, 255, onChange)
    cv2.createTrackbar('Cb_MIN', 'YCrCb', 0, 255, onChange)
    cv2.setTrackbarPos('Y_MAX', 'YCrCb', 255)
    cv2.setTrackbarPos('Y_MIN', 'YCrCb', 0)
    cv2.setTrackbarPos('Cr_MAX', 'YCrCb', 255)
    cv2.setTrackbarPos('Cr_MIN', 'YCrCb', 0)
    cv2.setTrackbarPos('Cb_MAX', 'YCrCb', 255)
    cv2.setTrackbarPos('Cb_MIN', 'YCrCb', 0)

def showcam():
    try:
        print('open cam')
        cap = cv2.VideoCapture(0)
    except:
        print('Not working')
        return
    cap.set(3, 480)
    cap.set(4, 320)

    while True:
        ret, frame = cap.read()
        Y_MAX = cv2.getTrackbarPos('Y_MAX', 'YCrCb')
        Y_MIN = cv2.getTrackbarPos('Y_MIN', 'YCrCb')
        Cr_MAX = cv2.getTrackbarPos('Cr_MAX', 'YCrCb')
        Cr_MIN = cv2.getTrackbarPos('Cr_MIN', 'YCrCb')
        Cb_MAX = cv2.getTrackbarPos('Cb_MAX', 'YCrCb')
        Cb_MIN = cv2.getTrackbarPos('Cb_MIN', 'YCrCb')

        lower = np.array([Y_MIN, Cr_MIN, Cb_MIN])
        higher = np.array([Y_MAX, Cr_MAX, Cb_MAX])
        YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
        Gmask = cv2.inRange(YCrCb, lower, higher)
        G = cv2.bitwise_and(frame, frame, mask=Gmask)
        if not ret:
            print('error')
            break
        #cv2.imshow('cam_load', frame)
        cv2.imshow('YCrCb', G)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

setting_bar()
showcam()