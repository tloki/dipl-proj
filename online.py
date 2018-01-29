import cv2
import sys


def bb_rel_to_abs(bb):
    return bb[0], bb[1], bb[0] + bb[2], bb[0] + bb[3]


def bb_intersection_over_union(boxA, boxB, relative=True):

    if relative:
        boxA = bb_rel_to_abs(boxA)
        boxB = bb_rel_to_abs(boxB)  # if needed...

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = (xB - xA + 1) * (yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use

    from cv_utils import tracking_algorithms

    chosen = 'TrackerGOTURN'

    tracker = tracking_algorithms()[chosen][1]()
    #tracker = cv2.Tracker_create("TLD")

    # Read video
    video = cv2.VideoCapture("/home/loki/PycharmProjects/dipl-proj/TB-50/Basketball/video.avi")
    # video = cv2.VideoCapture("sample_videos/ParkingDriver.mp4")

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    bbox = (111, 98, 25, 101)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    print(bbox)
    # input()

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    gt_reinit_count = 0
    precision = 0.6

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        relevant = True

        # if tracker is not relevant any more, reset it to ground truth value:
        if not relevant:
            tracker.release()
            tracker = tracking_algorithms()[chosen][1]()
            bbox = 0  # ucitaj iz ground truth
            ok = tracker.init(frame, bbox)
            gt_reinit_count += 1
            ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
