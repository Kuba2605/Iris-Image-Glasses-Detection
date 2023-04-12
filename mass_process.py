import os, csv, cv2, time

import reflection_detection as rd
import edge_detection as ed

from sys import argv
from sys import exit as sysexit
from fnmatch import fnmatch

dir = ""
pattern_jpg = "*.jpg"
pattern_png = "*.png"

if len(argv) != 3:
    print("Usage: python mass_process.py <target path> <output path>")
    sysexit()
else:
    dir = argv[1]
    outputdir = argv[2]


fields = ['last_dir', 'filename', 'percentage', 'line_amount']
rows = []


for path, subdirs, files in os.walk(dir):
    for name in files:
        if fnmatch(name, pattern_jpg) or fnmatch(name, pattern_png):
            print("Processing " + os.path.join(path, name))
            img = cv2.imread(os.path.join(path, name))
            resized_img = cv2.resize(img, (320, 240))
            reflections_img, reflections_perc = rd.process_image(resized_img, 180)
            edges_image, line_amount = ed.detect_glasses(resized_img)
            last_dir = os.path.basename(os.path.normpath(path))

            rows.append([last_dir, name, reflections_perc, line_amount])
            continue

if not os.path.isdir(outputdir):
    os.makedirs(outputdir)

if rows:    #Make sure we have some data to write
    try:
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        csv_path = outputdir + "\\results_" + timestr + ".csv"
        with open(csv_path, 'w', newline="\n") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)
        print("Results written to: " + csv_path)
    except:
        print("Unable to write to file: " + csv_path)