#!/usr/bin/env python3
import sys, os
import csv
import subprocess
try:
    import cv2
except ModuleNotFoundError:
    # check if pip installed
    if 0 == subprocess.run([sys.executable, "-m", "pip"], stdout=subprocess.DEVNULL).returncode:
        print("Starting pip...")
        if 0 == subprocess.run(["sudo", sys.executable, "-m", "pip", "install", "opencv-python"]).returncode:
            import cv2
        else:
            print("Failed to get opencv")
            exit(1)
    else:
        print("Install opencv!")
        exit(1)
import numpy as np

TITLE = "r/place"
PIXELS_FILE = "pixels.csv"
SORTED_FILE = "sorted_pixels.csv"
DIR = os.path.dirname(os.path.realpath(__file__))

COLOR= [(1.0000, 1.0000, 1.0000),
        (0.8941, 0.8941, 0.8941),
        (0.5333, 0.5333, 0.5333),
        (0.1333, 0.1333, 0.1333),
        (0.8196, 0.6549, 1.0000),
        (0.0000, 0.0000, 0.8980),
        (0.0000, 0.5843, 0.8980),
        (0.2588, 0.4157, 0.6275),
        (0.0000, 0.8510, 0.8980),
        (0.2667, 0.8784, 0.5804),
        (0.0039, 0.7451, 0.0078),
        (0.9412, 0.8980, 0.0000),
        (0.7804, 0.5137, 0.0000),
        (0.9176, 0.0000, 0.0000),
        (1.0000, 0.2902, 0.8784),
        (0.5020, 0.0000, 0.5098)]

def main():
    curl_val = subprocess.run([DIR + "/get_and_sort_pixels_file.sh",
                                DIR + "/" + PIXELS_FILE,
                                DIR + "/" + SORTED_FILE]).returncode
    if curl_val != 0 and curl_val != 254:
        exit(curl_val)
    
    total = int(subprocess.run(["wc", "-l", SORTED_FILE], stdout=subprocess.PIPE).stdout.decode("UTF-8").split(" ")[0]) - 1
    count = 0

    cv2.namedWindow(TITLE, cv2.WINDOW_NORMAL)
    img = np.full(shape=[1000, 1000, 3], fill_value=1.0, dtype=np.float)

    file = open(SORTED_FILE, "r")
    csv_reader = csv.reader(file)
    break_flag = False
    for row in csv_reader:
        count += 1
        try:
            x = int(row[2]) - 1
        except:
            continue
        y = int(row[3]) - 1
        color = COLOR[int(row[4])]
        img[y][x] = color
        if count % 1000 == 0:
            print("\r{:.3f}%".format(100 * count / total), end='')
            cv2.imshow(TITLE, img)
            char = cv2.waitKey(1) & 0xFF
            if char == ord('q') or char == 27:
                break_flag = True
                break
    
    if not break_flag:
        print("Press any key on the window to exit...")
        cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
