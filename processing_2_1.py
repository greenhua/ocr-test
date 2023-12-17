import cv2, os
import numpy as np
import time
import imutils
import math


def processing(frame, clahe=False, i=0):
    cv2.waitKey(10)
    cv2.imshow('frame', frame)

# Adjust image
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    adjusted = cv2.filter2D(frame, -1, kernel)


    image_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# CLAHE!!!!
    # clipLimit -> Threshold for contrast limiting
    if clahe:
        clahe = cv2.createCLAHE(clipLimit = 4)
        final_img = clahe.apply(image_bw)
    else:
        final_img = image_bw

#looking for the center circle
    clone = cv2.cvtColor(final_img,cv2.COLOR_GRAY2RGB)
    gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)

#         Threshold grayscaled image to get binary image
    ret,gray_threshed = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)

    # Smooth an image
    bilateral_filtered_image = cv2.bilateralFilter(gray_threshed, 5, 175, 175)

    # Find edges
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 250)

    # Find contours of center circle
    contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for contour in contours:
       approx = cv2.approxPolyDP(contour, 0.1*cv2.arcLength(contour,True), True)
       area = cv2.contourArea(contour)
#        print(area)
       if (  ( area < 10000) and (area > 1000) ):
           contour_list.append(contour)
#     cv2.drawContours(clone, contour_list, -1, (255,0,0), 2)



    roi = ""
    result_status = 0
    #ищем центр центральногоь круга
#     print(len(contour_list))
    if (5>len(contour_list)>1):
        result_status+=1
        print("center found!!")
        contour = contour_list[0]
        moments = cv2.moments(contour)
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])





#рисуем центр
        color = (0,  255, 0)
        radius = 2  # Радиус точки
        thickness = -1  # Заполнение точки, если thickness = -1
        cv2.circle(clone, (center_x, center_y), radius, color, thickness)

        radius = 230
        cv2.circle(clone, (center_x, center_y), radius, (0,  0, 255), 7)

        gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)

        # Применение порогового преобразования для получения бинарного изображения
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Нахождение контуров в бинарном изображении
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Поиск наибольшего контура
        largest_contour = max(contours, key=cv2.contourArea)

        # Создание маски из контура
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

        # Вырезание области изображения по маске
        result = cv2.bitwise_and(clone, clone, mask=mask)

#         cv2.imshow('Result', result)






# вырезаем квадрат

        left_x = int(center_x-radius)
        if (left_x<0):
            left_x = 0

        left_y = int(center_y-radius)

        if (left_y<0):
            left_y = 0


        height, width = clone.shape[:2]

        right_x = center_x + radius
        if right_x > width:
            right_x = width

        right_y = center_y + radius
        if right_y > height:
            right_y = width

        print("src", height, width)

        print("center: ", center_y, center_x )
        print("l", left_y, left_x)
        print("r", right_y, right_x)

        cropped_image  = result[left_y:right_y, left_x:right_x]
#         cv2.imshow('Cropped Image', cropped_image)
#         cv2.imwrite(f"cropped_image.jpg", cropped_image)



# ищем остальное
        image_bw = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        edge_detected_image = cv2.Canny(image_bw, 10, 100)
        kernel = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(edge_detected_image, kernel, iterations=1)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
#         dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
        contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        c_dilated_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2RGB)

        for c in contours:
            cv2.drawContours(c_dilated_image, [c], 0, (250, 90, 0), thickness=-0)
            cv2.imshow('c_dilated_image', c_dilated_image)
#             cv2.waitKey(20000)
            area = cv2.contourArea(c)
            print(area)

        cv2.imshow('eroded_image', eroded_image)
        key = cv2.waitKey(10)
        if (key==115):
            cv2.imwrite(f"frame-{i}.jpg", frame)
            print("saved")


        return 1

#         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#
#
#         ret,gray_threshed = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
#         cv2.imshow('gray_threshed', bilateral_filtered_image)
#
#         # Smooth an image
#         bilateral_filtered_image = cv2.bilateralFilter(gray_threshed, 2, 20, 20)
#         cv2.imshow('bilateral_filtered_image', bilateral_filtered_image)
#
#         # Find edges
#         edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 250)
#
#
#         # Нахождение контуров в бинарном изображении
#         contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# #         contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#         # Поиск наибольшего контура
#         largest_contour = max(contours, key=cv2.contourArea)
#         print("c:", len(contours))
#         cv2.drawContours(thresh, contours, 0, (250, 90, 0), thickness=0)
#         cv2.imshow('bilateral_filtered_image', bilateral_filtered_image)
#         for contour in contours:
#             cv2.drawContours(cropped_image, [contour], 0, (250, 90, 0), thickness=0)
#             cv2.imshow('Cropped Image', cropped_image)
#             print(len(contour))
#             cv2.waitKey(200000)
#
#
#
#
#         # Применение маски к исходному изображению
# #             final_img = cv2.cvtColor(final_img,cv2.COLOR_GRAY2RGB)
#
# #         result = cv2.bitwise_and(final_img,final_img,mask=mask)
# #         cv2.imshow('result', result)

    cv2.waitKey(20)




def calculate_angle(line1, line2):
    # Рассчитываем угловой коэффициент для каждой линии
    slope1 = math.atan2(line1[3] - line1[1], line1[2] - line1[0])
    slope2 = math.atan2(line2[3] - line2[1], line2[2] - line2[0])

    # Рассчитываем угол между линиями в радианах
    angle_rad = math.atan2(math.sin(slope1 - slope2), math.cos(slope1 - slope2))

    # Преобразуем угол в градусы
    angle_deg = math.degrees(angle_rad)

    # Убеждаемся, что угол положителен (в диапазоне от 0 до 180 градусов)
    if angle_deg < 0:
        angle_deg += 180

    return angle_deg