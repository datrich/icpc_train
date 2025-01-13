import math
import numpy as np
import cv2 as cv

drawing = False # true if mouse is pressed
img = np.ones((800,1200,3), np.uint8)*255
start_point = (-1,-1)
end_point = (-1,-1)
mode = 'draw'
input_text = ''
input_para = {'trans':[0,0],'scale':[1.0,1.0],'rotate':0}

def legend():
    global img
    cv.rectangle(img, (900,20), (950,40), (0,0,0), 1)
    cv.putText(img, ": original rectangle",
                (970,35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv.rectangle(img, (900,60), (950,80), (192,192,192), -1)
    cv.rectangle(img, (900,60), (950,80), (0,0,0), 1)
    cv.putText(img, ": transformated rectangle",
                (970,75), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
def text():
    global img, mode, input_text

    # Clear the top area
    cv.rectangle(img, (0,0), (1200,100), (255,255,255), -1)
    cv.rectangle(img, (1,2), (1198,100), (0,0,0), 2)

    # Draw mode and instructions
    cv.putText(img, f"Current Mode: {mode.upper()}", (10,20),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 1)
    if mode == 'draw':
        cv.putText(img, "Click and drag to draw rectangle | Press: T-Translate, R-Rotate, S-Scale, Q-Quit",
                    (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    elif mode == 'trans':
        cv.putText(img, "Type numbers for dx,dy (e.g: 100,50) | Press Enter to apply | D to return | Q to quit",
                    (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        cv.putText(img, f"Input: {input_text}", (10,60),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        cv.putText(img, f"Current translation: dx={input_para['trans'][0]}, dy={input_para['trans'][1]}",
                    (10,80), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        if input_para['trans'] != [0,0]:
            legend()
    elif mode == 'rotate':
        cv.putText(img, "Type angle in degrees (e.g: 45) | Press Enter to apply | D to return | Q to quit",
                    (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        cv.putText(img, f"Input: {input_text}", (10,60),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        cv.putText(img, f"Current angle: {input_para['rotate']}",
                    (10,80), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        if input_para['rotate'] != 0:
            legend()
    elif mode == 'scale':
        cv.putText(img, "Type scale factors sx,sy (e.g: 1.5,1.5) | Press Enter to apply | D to return | Q to quit",
                    (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        cv.putText(img, f"Input: {input_text}", (10,60),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        cv.putText(img, f"Current scale: sx={input_para['scale'][0]}, sy={input_para['scale'][1]}",
                    (10,80), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        if input_para['scale'] != [1.0,1.0]:
            legend()

def draw_rectangle(event,x,y,flags,param):
    global drawing,img,start_point,end_point,mode
    if mode == 'draw':
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = x,y
            img = np.ones((800,1200,3), np.uint8)*255
            text()
        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                img = np.ones((800,1200,3), np.uint8)*255
                text()
                cv.rectangle(img,start_point,(x,y),(192,192,192),-1)
                cv.rectangle(img,start_point,(x,y),(0,0,0),1)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x,y)
            img = np.ones((800,1200,3), np.uint8)*255
            text()
            cv.rectangle(img,start_point,end_point,(192,192,192),-1)
            cv.rectangle(img,start_point,end_point,(0,0,0),1)
    else:
        if event == cv.EVENT_LBUTTONDOWN:
            cv.rectangle(img,(380,370),(820,420),(0,0,0),-1)
            cv.putText(img, "PRESS D IF YOU WANT RETURN TO DRAWING MODE!",
                    (400,400), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        elif event == cv.EVENT_LBUTTONUP:
            img = np.ones((800,1200,3), np.uint8)*255
            cv.rectangle(img,start_point,end_point,(192,192,192),-1)
            cv.rectangle(img,start_point,end_point,(0,0,0),1)
            if mode == 'trans':
                transfomation()
            elif mode == 'rotate':
                rotate()
            elif mode == 'scale':
                scale()
    cv.imshow('LAB1_by_Tuan_Dat',img)

def transfomation():
    global start_point,end_point,img,input_para,mode
    img = np.ones((800,1200,3), np.uint8)*255
    temp1 = (start_point[0]+input_para['trans'][0],start_point[1]+input_para['trans'][1])
    temp2 = (end_point[0]+input_para['trans'][0],end_point[1]+input_para['trans'][1])
    cv.rectangle(img,start_point,end_point,(0,0,0),1)
    cv.rectangle(img,temp1,temp2,(192,192,192),-1)
    cv.rectangle(img,temp1,temp2,(0,0,0),1)
    text()
    cv.imshow('LAB1_by_Tuan_Dat',img)

def rotate():
    global start_point,end_point,img,input_para,mode
    img = np.ones((800,1200,3), np.uint8)*255
    dx = abs(end_point[0]-start_point[0])
    dy = abs(end_point[1]-start_point[1])
    corners = np.array([[start_point[0], start_point[1]],[start_point[0] + dx, start_point[1]],
        [start_point[0] + dx, start_point[1] + dy],[start_point[0], start_point[1] + dy]], dtype=np.float32)
    image_center = ((start_point[0]+end_point[0])/2,(start_point[1]+end_point[1])/2)
    rot_mat = cv.getRotationMatrix2D(image_center, float(input_para['rotate']), 1.0)
    ones = np.ones(shape=(len(corners), 1))
    points_ones = np.hstack([corners, ones])
    transformed_points = rot_mat.dot(points_ones.T).T.astype(np.int32)
    cv.rectangle(img,start_point,end_point,(0,0,0),1)
    cv.fillPoly(img, [transformed_points], (192,192,192))
    cv.polylines(img, [transformed_points], True, (0,0,0), 1)
    text()
    cv.imshow('LAB1_by_Tuan_Dat', img)

def scale():
    global start_point,end_point,img,input_para,mode
    img = np.ones((800,1200,3), np.uint8)*255
    image_center = ((start_point[0]+end_point[0])/2,(start_point[1]+end_point[1])/2)
    dx = abs(end_point[0]-start_point[0])
    dy = abs(end_point[1]-start_point[1])


    new_dx = int(dx * input_para['scale'][0])
    new_dy = int(dy * input_para['scale'][1])

    new_start = (
        int(image_center[0] - new_dx//2),
        int(image_center[1] - new_dy//2)
    )
    new_end = (
        int(image_center[0] + new_dx//2),
        int(image_center[1] + new_dy//2)
    )
    cv.rectangle(img,start_point,end_point,(0,0,0),1)
    cv.rectangle(img,new_start,new_end,(192,192,192),-1)
    cv.rectangle(img,new_start,new_end,(0,0,0),1)
    text()
    cv.imshow('LAB1_by_Tuan_Dat',img)

def process_input():
    global input_text, input_para, mode

    try:
        if mode == 'trans':
            dx, dy = map(int, input_text.split(','))
            input_para['trans'] = [dx, dy]
            transfomation()
        elif mode == 'rotate':
            angle = float(input_text)
            input_para['rotate'] = angle
            rotate()
        elif mode == 'scale':
            sx, sy = map(float, input_text.split(','))
            input_para['scale'] = [sx, sy]
            scale()
    except ValueError:
        print("Invalid input format!")
    input_text = ''

cv.namedWindow('LAB1_by_Tuan_Dat')
cv.setMouseCallback('LAB1_by_Tuan_Dat',draw_rectangle)

while(True):
    text()
    cv.imshow('LAB1_by_Tuan_Dat',img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('d'):
        mode = 'draw'
        input_text = ''
    elif k == ord('t'):
        if start_point != (-1,-1):
            mode = 'trans'
            input_text = ''
        else:
            cv.putText(img, "DRAW RECTANGLE FIRST!",
                        (400,400), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
            mode = 'draw'
    elif k == ord('r'):
        if start_point != (-1,-1):
            mode = 'rotate'
            input_text = ''
        else:
            cv.putText(img, "DRAW RECTANGLE FIRST!",
                        (400,400), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
            mode = 'draw'
    elif k == ord('s'):
        if start_point != (-1,-1):
            mode = 'scale'
            input_text = ''
        else:
            cv.putText(img, "DRAW RECTANGLE FIRST!",
                        (400,400), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
            mode = 'draw'
    elif k == 13:  # Enter key
        process_input()
    elif k == 127:  # Backspace value (127 for MacOS/ 8 for Windows)
        input_text = input_text[:-1]
    elif k != 255:
        if mode != 'draw':
            input_text += chr(k)

cv.destroyAllWindows()
