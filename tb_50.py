from get_all_dirs import *
import os


def get_all_videos_and_groundtruths(ROOT="./TB-50", video_name="video.avi", ground_truth_name="groundtruth_rect.txt"):

    dirs = get_all_dirs(ROOT)

    dirs.sort()

    videos = [path + video_name for path in dirs]
    ground_truth = [path + ground_truth_name for path in dirs]

    for video in videos:
        if not os.path.isfile(video):
            raise RuntimeError("file {} does not exist!".format(video))

    for gt in ground_truth:
        if not os.path.isfile(gt):
            raise RuntimeError("file {} does not exist!".format(gt))

    return list(zip(dirs, videos, ground_truth))


if __name__ == "__main__":
    for element in get_all_videos_and_groundtruths():
        print(element)

    print(len(get_all_videos_and_groundtruths()))