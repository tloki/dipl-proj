def parse_single_rectangle(rectangle_string):

    if "," not in rectangle_string:
        rectangle_string = rectangle_string.replace("\t", ",")

    rectangle_string = rectangle_string.replace(" ", "")
    rectangle_string = rectangle_string.replace("\n", "")
    rectangle_string = rectangle_string.replace("\r", "")
    rectangle_string = rectangle_string.replace("\t", "")

    data = rectangle_string.split(",")
    result = []

    for record in data[0:4]:
        result.append(int(record))

    if len(result) != 4:
        raise ValueError("invalid rectangle {}".format(rectangle_string))

    return tuple(result)


def parse(file_path):
    with open(file_path, "r+") as rect_file:

        rects = rect_file.readlines()

    result = [parse_single_rectangle(p) for p in rects]
    return result


if __name__ == "__main__":
    path = "./TB-50/Basketball/groundtruth_rect.txt"
    print(parse(path))
