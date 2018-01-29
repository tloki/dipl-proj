from cv_utils import tracking_algorithms
from tb_50 import *
import cv2
from bench_utils import *
import time
from parse_rectangle_data import *
import os
import sys


def bench(tracker_create, video_path, gt_path, reset_iou=0.5, name='Tracking', dbg_dir='/tmp'):
    # init a tracker
    tracker = tracker_create()

    # load a video
    video = cv2.VideoCapture(video_path)

    # check if video is opened
    if not video.isOpened():
        raise RuntimeError("Cannot open video {}".format(video_path))

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        raise RuntimeError("Cannot read video {}".format(video_path))

    # read current ground truth file
    ground_truth_boxes = parse(gt_path)
    n_frames = len(ground_truth_boxes)

    # fetch first bbox
    bbox = ground_truth_boxes.pop(0)

    # initialize tracker
    tracker.init(frame, bbox)

    # initialize output values
    gt_reinit_count = 0
    curr_time = time.time()
    iou = 0
    ious = []
    tracked_bboxes = [bbox]

    # for all other frames
    while True:

        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break  # end of video

        # Update tracker
        ok, bbox = tracker.update(frame)
        tracked_bboxes.append(bbox)

        # fetch current ground truth bbox
        bbox_gt = ground_truth_boxes.pop(0)

        current_iou = bb_intersection_over_union(bbox, bbox_gt)
        iou += current_iou
        ious.append(current_iou)

        # compare ground truth and current tracking
        # if tracker is not relevant any more, reset it to ground truth value:
        if bb_intersection_over_union(bbox, bbox_gt) <= reset_iou:
            ok = False

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracker Reset", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            #             2)
            gt_reinit_count += 1
            tracked_bboxes.pop(0)
            tracker = tracker_create()
            tracked_bboxes.append(bbox)
            bbox = bbox_gt
            bbox = fixbboxdims(bbox, video.get(3), video.get(4))
            ok = tracker.init(frame, bbox)
            iou -= current_iou
            iou += 1.0
            ious[-1] = 1.0

        # Display tracker type on frame
        cv2.putText(frame, name, (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    cv2.destroyAllWindows()

    end_time = time.time()
    duration = end_time - curr_time

    # dump result to file
    dbg = "tracker: {}\nvideo: {}\navg FPS:{}\navg iou: {}\nreset count: {}\ncutoff iou: {}\noius:\n{}\nbboxes:\n{}".format(
        name, video_path, n_frames/duration, iou / n_frames,
        gt_reinit_count, reset_iou, ious, tracked_bboxes
    )

    if not dbg_dir.endswith('/'):
        dbg_dir += '/'

    with open(dbg_dir + name, "w+") as out:
        out.write(dbg)

    result = dict()
    result['tracker'] = name
    result['video'] = video_path
    result['fps'] = n_frames / duration
    result['avg_iou'] = sum(ious) / len(ious)
    result['iou_reset'] = reset_iou
    result['ious'] = ious
    result['bboxes'] = tracked_bboxes
    result['reset_count'] = gt_reinit_count
    result['duration'] = duration
    result['n_frames'] = n_frames

    return result


if __name__ == '__main__':

    done = [('TrackerBoosting', './TB-50/Basketball/')]
    noimpl = ('TrackerGOTURN')
    videoDone = ['./TB-50/Bird1/', './TB-50/Biker/', './TB-50/BlurBody/', './TB-50/BlurCar2/',
                 './TB-50/BlurFace/', './TB-50/BlurOwl/', './TB-50/Box/', './TB-50/Car1/', './TB-50/Car4/',
                 './TB-50/CarDark/', './TB-50/CarScale/', './TB-50/ClifBar/', './TB-50/Couple/', './TB-50/Crowds/',
                 './TB-50/Deer/', ]

    CUTOFF_IOU = 0.5
    SLOW = True

    algorithms = tracking_algorithms()
    benchmark_sequences = get_all_videos_and_groundtruths()

    print("trackers: ({} implemented)".format(len(algorithms)))
    print("#"*20)
    for algorithm_name in algorithms:

        print("tracker: ", algorithm_name)
        # tracker, tracker_create = algorithms[algorithm_name]

    print()
    print("TB-50: ({} files)".format(len(benchmark_sequences)))
    print("#"*20)

    for directory, video_path, ground_truth_file in benchmark_sequences:
        print(directory, video_path, ground_truth_file)

    print()
    print("benchmark:")
    print("#"*20)

    for directory, video_path, ground_truth_file in benchmark_sequences:
        if directory in videoDone:
            print("preskacem odradeni video: {}".format(directory))
            continue

        print("video: {}".format(video_path))

        for algorithm_name in sorted(algorithms.keys()):

            # preskociti:
            if (algorithm_name, directory) in done:
                print("preskacem {}".format((algorithm_name, directory)))
                continue

            if algorithm_name in noimpl:
                print("preskacem", algorithm_name)
                continue

            Tracker, tracker_create = algorithms[algorithm_name]

            print("\ttracker: {}".format(algorithm_name))

            # init a tracker
            tracker = tracker_create()

            # load a video
            video = cv2.VideoCapture(video_path)

            # check if video is opened
            if not video.isOpened():
                raise RuntimeError("Cannot open video {}".format(video_path))

            # Read first frame.
            ok, frame = video.read()
            if not ok:
                raise RuntimeError("Cannot read video {}".format(video_path))

            # read current ground truth file
            ground_truth_boxes = parse(ground_truth_file)
            n_frames = len(ground_truth_boxes)

            # fetch first bbox
            bbox = ground_truth_boxes.pop(0)

            # initialize tracker
            tracker.init(frame, bbox)

            # initialize output values
            gt_reinit_count = 0
            curr_time = time.time()
            iou = 0
            ious = []
            tracked_bboxes = [bbox]

            # for all other frames
            while True:

                # Read a new frame
                ok, frame = video.read()
                if not ok:
                    break  # end of video

                # Update tracker
                ok, bbox = tracker.update(frame)
                tracked_bboxes.append(bbox)

                # fetch current ground truth bbox
                bbox_gt = ground_truth_boxes.pop(0)

                current_iou = bb_intersection_over_union(bbox, bbox_gt)
                iou += current_iou
                ious.append(current_iou)


                # compare ground truth and current tracking
                # if tracker is not relevant any more, reset it to ground truth value:
                if bb_intersection_over_union(bbox, bbox_gt) <= CUTOFF_IOU:
                    ok = False

                # Draw bounding box
                if ok:
                    # Tracking success
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                else:
                    # Tracking failure
                    cv2.putText(frame, "Tracker Reset", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    #             2)
                    gt_reinit_count += 1
                    # print("\t\t{}.reset to ground truth!".format(gt_reinit_count))
                    tracked_bboxes.pop(0)
                    tracker = tracker_create()
                    bbox = bbox_gt
                    # print(bbox)
                    # bbox = fixbbox(bbox)
                    bbox = fixbboxdims(bbox, video.get(3), video.get(4))
                    ok = tracker.init(frame, bbox)
                    tracked_bboxes.append(bbox)
                    iou -= current_iou
                    iou += 1.0
                    ious[-1] = 1.0


                # Display tracker type on frame
                cv2.putText(frame, algorithm_name, (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

                # Display result
                cv2.imshow("Tracking", frame)

                # Exit if ESC pressed
                k = cv2.waitKey(1) & 0xff
                if k == 27:
                    break

            dbg = "tracker: {}\nvideo: {}\navg FPS:{}\navg iou: {}\nreset count: {}\ncutoff iou: {}\noius:\n{}\nbboxes:\n{}".format(
                algorithm_name, video_path,  (time.time() - curr_time)/n_frames, iou / n_frames,
                gt_reinit_count, CUTOFF_IOU, ious, tracked_bboxes
            )

            with open(directory + algorithm_name, "w+") as out:
                out.write(dbg)

            dbg2 = "tracker: {}\nvideo: {}\navg FPS:{}\navg iou: {}\nreset count: {}\ncutoff iou: {}\n".format(
                algorithm_name, video_path, (time.time() - curr_time) / n_frames, iou / n_frames,
                gt_reinit_count, CUTOFF_IOU, ious, tracked_bboxes
            )

            print(dbg2)

if __name__ == '__main__2':
    algorithms = tracking_algorithms()
    print(algorithms['TrackerMedianFlow'][1])
    res = bench(algorithms['TrackerMedianFlow'][1],
                        'TB-50/Basketball/video.avi',
                        'TB-50/Basketball/groundtruth_rect.txt',
                        reset_iou=0.5,
                        name='MedianFlow primjer')

    print(res)
















