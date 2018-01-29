from writeToVideo import *
import cv2

# dump_to_video("../sample_videos/Jogging1/img", "../sample_videos/Jogging1/myVideoSpori.avi", 10, "jpg")

from utils import tracking_algorithms

trackers = tracking_algorithms()

print(trackers)

video = cv2.VideoCapture("../sample_videos/myVideoSpori.avi")

ok, frame = video.read()

# bbox = (111, 98, 25, 101)
bbox = cv2.selectROI(frame, False)

tracker = trackers['TrackerTLD'][1]()



