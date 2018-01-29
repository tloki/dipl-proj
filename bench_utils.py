def bb_rel_to_abs(bb):
    return bb[0], bb[1], bb[0] + bb[2], bb[1] + bb[3]


def bb_abs_to_rel(bb):
    return bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]

# def bb_intersection_over_union2(box1, box2):
#
#     # make box1 the leftmost box
#     if box1[0] > box2[0]:
#         box1, box2 = box2, box1
#
#
#     x1_min, y1_min, w1, h1 = box1
#     x2_min, y2_min, w2, h2 = box2
#
#     # area1 = w1 * h1
#     # area2 = w2 * h2
#
#     x1_max = x1_min + w1
#     y1_max = y1_min + h1
#
#     x2_max = x2_min + w2
#     y2_max = y2_min + h2
#
#     x5 = max(x1_min, x2_min)
#     y5 = max(y1_min, y2_min)
#     x6 = min(x1_max, x2_max)
#     y6 = min(y1_max, y2_max)


def bb_intersection_over_union(boxA, boxB, relative=True):

    if relative: # conversion if needed
        boxA = bb_rel_to_abs(boxA)
        boxB = bb_rel_to_abs(boxB)

    # print(boxA, boxB)

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = (xB - xA) * (yB - yA)

    # print(interArea)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # if no intersection exists
    if iou < 0:
        return 0

    # return the intersection over union value
    return iou

def fixbboxdims(bbox, w, h):
    bbox_abs = bb_rel_to_abs(bbox)

    x1, y1, x2, y2 = bbox_abs

    if x1 < 0:
        x1 = 0
    if x1 > w:
        x1 = w
    if x2 < 0:
        x2 = 0
    if x2 > w:
        x2 = w

    if y1 < 0:
        y1 = 0
    if y1 > h:
        y1 = h
    if y2 < 0:
        y2 = 0
    if y2 > h:
        y2 = h

    bbox_abs = (x1, y1, x2, y2)
    return bb_abs_to_rel(bbox_abs)




def fixbbox(bbox):
    tofix = False

    for i in range(len(bbox)):
        if bbox[i] < 0:
            tofix = True

    if not tofix:
        return bbox
    bbox = list(bbox)

    for i in range(len(bbox)):
        if bbox[i] < 0:
            bbox[i] = 0

    return tuple(bbox)

if __name__ == "__main__":
    box_a = (0, 0, 10, 10)
    box_b = (100, 100, 5, 5)

    print(bb_intersection_over_union(box_a, box_b))

    print(bb_abs_to_rel(bb_rel_to_abs((1, 2, 3, 4))) == (1, 2, 3, 4))
