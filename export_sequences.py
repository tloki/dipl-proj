from writeToVideo import *
import os

ROOT_DIR = "./"
SEQUENCES_DIR = "TB-50/"


sequences_common_path = ROOT_DIR + SEQUENCES_DIR
files = os.listdir(sequences_common_path)

files_full_path = [sequences_common_path + path + "/" for path in files]
directories = []

for f in files_full_path:
    if os.path.isdir(f):
        directories.append(f)

print(directories)
print(len(directories))

for i, dir in enumerate(directories):
    video_path = dir + "video.avi"
    images_path = dir + "img/"

    print("{}. video: {}".format(i + 1, images_path), end="")

    dump_to_video(images_path, video_path, fps=24, extension="jpg")

    print(" done!")

