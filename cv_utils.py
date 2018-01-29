import cv2
import sys
import re


def tracking_algorithms():
    # returns dictionary with methods that initialize trackers

    # dict[TrackerName] -> (TrackerConstructor, TrackerCreateMethod)

    r = re.compile("Tracker.*_create")
    available = filter(r.match, dir(cv2))
    tracker_names = list(available)

    # print(tracker_names)

    tracker_create_methods = [getattr(cv2, tracker) for tracker in tracker_names]
    tracker_names = [name[0:-7] for name in tracker_names]
    tracker_constructors = [getattr(cv2, tracker) for tracker in tracker_names]

    # check if really a tracking algorithm
    instance_check = [isinstance(method(), cv2.Tracker) for method in tracker_create_methods]

    if False in instance_check:
        raise RuntimeError("Unable to list OpenCV implemented tracking algorithms")

    # pack values into dictionary
    result_dict = dict()
    for i, name in enumerate(tracker_names):
        result_dict[name] = (tracker_constructors[i], tracker_create_methods[i])

    return result_dict


if __name__ == '__main__':

    print("Python version: {}.{}.{}\nOpenCV version: {}".format(sys.version_info[0],
                                                                sys.version_info[1],
                                                                sys.version_info[2],
                                                                cv2.__version__))

    print("Available tracking algorithms: {}".format(", ".join(list(tracking_algorithms().keys()))))