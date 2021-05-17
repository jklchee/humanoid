import cv2
def mode_abcd(binary_mask):
    abcd = 129

    contours, hierarchy = cv2.findContours(binary_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 컨투어

    if len(contours) == 0:
        print("물체를 감지할 수 없습니다")
    else:
        contr = contours[0]
        x, y, w, h = cv2.boundingRect(contr)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        frame2 = frame[y:y + h, x:x + w]

        cv2.drawContours(frame, contours, -1, (0, 255, 0), 4)

        blue_area = cv2.contourArea(contr, False)
        total_size = frame2.size
        per = blue_area / total_size

        if per < 0.145:
            abcd = 112
            print('c')
        elif per > 0.15 and per < 0.2:
            abcd = 113
            print('a')
        else:
            if len(contours) == 2:
                abcd = 111
                print('d')
            else:
                abcd = 114
                print('b')

    return abcd


def mode_area_color(mask_green):
    areaColor = 129

    pixels = cv2.countNonZero(mask_green)

    if pixels > 10000:
        areaColor = 130  # 초록
        print('green')
    else:
        areaColor = 128  # 검정
        print('black')

    print("영역색상 :", areaColor)
    return areaColor

def mode_milk_save(binary_area):
    save = 129

    pixels_area = cv2.countNonZero(binary_area)

    if pixels_area > 1000:
        test_frame = binary_area[241:480, :]
        pixels = cv2.countNonZero(test_frame)
        cv2.imshow("milk", test_frame)

        if pixels > 69120:  # =240*640*0.45
            save = 130
            print('성공')

        else:
            save = 128
            print('실패')

    print("안전구역우유결과 :", save)
    return save


# ---------------------------------------

def mode_milk_escape(binary_area):
    escape = 129

    pixels_area = cv2.countNonZero(binary_area)

    if pixels_area > 1000:
        test_frame = binary_area[0:240, :]
        pixels = cv2.countNonZero(test_frame)
        cv2.imshow("milk", test_frame)

        if pixels <= 9216:  # =240*640*0.08
            escape = 130
            print('성공')

        else:
            escape = 128
            print('실패')

    print("확진구역우유결과 :", escape)
    return escape


