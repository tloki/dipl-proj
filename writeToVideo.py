#!/usr/bin/env python3
import cv2
import re
import glob

# usage:
# ./writeToVideo.py folderWithSequence out.mov [fps, extension]
# fps defaults to 24
# extension defaults to png

# example run within python script:
# dump_to_video("/home/loki/Downloads/Jogging/img", "/home/loki/myVideo.avi", 30, "jpg")


def dump_to_video(folder_name, output_file_name, fps=24, extension="png"):
    if folder_name[-1] != "/":
        folder_name += "/"

    file_list = sorted(glob.glob(folder_name + "*." + extension))
    print(file_list)

    first_image_path = file_list.pop()
    first_image = cv2.imread(first_image_path)
    height, width, layers = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(output_file_name, fourcc, fps, (width, height))

    video.write(first_image)

    if not video:
        raise RuntimeError("Cound not export video")

    for image_path in file_list:
        image = cv2.imread(image_path)
        video.write(image)

    # cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("""usage:
./writeToVideo.py folderWithSequence out.mov [fps, extension]
fps defaults to 24
extension defaults to png""")
        exit(-1)

    folder_name = sys.argv[1]
    output_path = sys.argv[2]
    fps = 24
    ext = "png"

    if len(sys.argv) > 3:
        fps = int(sys.argv[3])
    if len(sys.argv) == 5:
        ext = sys.argv[4]

    dump_to_video(folder_name, output_path, fps, ext)
