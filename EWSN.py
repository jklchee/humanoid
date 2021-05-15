import cv2

def mode_ewsn(binary):
    ewsn = 129

    # 모폴로지 연산(열림연산) 후 컨투어
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary_ero = cv2.erode(binary, kernel)
    contours, _ = cv2.findContours(binary_ero, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 컨투어된 영역중에서 제일 큰 부분만 선택 (배경 제거)
    max_contour = None
    max_area = -1

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # 각 컨투어에 근사 컨투어로 단순화
    approx = cv2.approxPolyDP(max_contour, 0.01 * cv2.arcLength(max_contour, True), True)
    # 꼭짓점의 개수
    vertices = len(approx)
    # 사각형으로 컨투어
    x, y, w, h = cv2.boundingRect(max_contour)

    if vertices >= 18:
        ewsn = 112
        print('남')
    elif vertices <= 12:
        ewsn = 111
        print('북')
    else:
        if abs(w - h) >= 60:
            ewsn = 113
            print('동')
        else:
            ewsn = 114
            print('서')

    print("방위 :", ewsn)
    return ewsn

