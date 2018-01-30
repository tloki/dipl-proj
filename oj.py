def calculate_iou(bbox1, bbox2, pr = False):

    # let leftmost box be A
    bboxA = min(tuple(bbox1), tuple(bbox2))
    bboxB = max(tuple(bbox1), tuple(bbox2))
    
    x_left_A, y_left_A, x_right_A, y_right_A = bboxA
    x_left_B, y_left_B, x_right_B, y_right_B = bboxB

    if(x_left_A > x_right_A) or (y_left_A > y_right_A) or (x_left_B > x_right_B) or (y_left_B > y_right_B):
        raise ValueError("format error")

    A_width = x_right_A - x_left_A
    if(A_width == 0):
        return 0.0
    
    B_width = x_right_B - x_left_B
    if(B_width == 0):
        return 0.0

    A_height = y_right_A - y_left_A
    if(A_height == 0):
        return 0.0
    
    B_height = y_right_B - y_left_B
    if(B_height == 0):
        return 0.0
    

    if pr:
        print("A:", bboxA)
        print("B:", bboxB)

    if x_right_A <= x_left_B:
        return 0.0

    # if A is lower
    if (y_left_A <= y_left_B) and (y_right_A <= y_left_B):
        return 0.0

    # if B is lower
    if (y_left_B <= y_left_A) and (y_right_B <= y_left_A):
        return 0.0

    x_overlap = abs(x_left_B - min(x_right_A, x_right_B))

    y_overlap = "err"
    # A is lower
    if (y_left_A <= y_left_B):
        if pr: print("A lower")
        y_overlap = abs(y_left_B - min(y_right_A, y_right_B))

    # B is lower
    elif (y_left_B <= y_left_A):
        if pr: print("B lower")
        y_overlap = abs(y_left_A - min(y_right_B, y_right_A))

    interception = x_overlap * y_overlap
    
    union = A_width * A_height +\
            B_width * B_height - interception

    if pr:
        print("A width   :", A_width)
        print("A height  :", A_height)
        print("B width   :", B_width)
        print("B height  :", B_height)
        print("x overlap :", x_overlap)
        print("y overlap :", y_overlap)
        print("intercept :", interception)
        print("A size    :", (x_right_A - x_left_A) * (y_right_A - y_left_A))
        print("B size    :", (x_right_B - x_left_B) * (y_right_B - y_left_B))
        print("Union size:", union)

    return interception / union

import random

i = 0
while True:
    i += 1
    bbox1 = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
    bbox2 = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]

    bbox1[2], bbox1[3] = bbox1[0] + bbox1[2], bbox1[1] + bbox1[3]
    bbox2[2], bbox2[3] = bbox2[0] + bbox2[2], bbox2[1] + bbox2[3]
    if i%100000 == 0:
        print(i)
    try:
        iou = calculate_iou(bbox1, bbox2)
    except ZeroDivisionError:
        print(bbox1, bbox2)
        raise ValueError("err")
    if iou > 1.0 or iou < 0.0:
        
        raise ValueError("A, B: {}, {}    , iou: {}".format(bbox1, bbox2, iou))
    
        

    

    
