from matplotlib import pyplot as plt
import numpy as np
from sys import argv
from sys import exit as sysexit
import csv


if len(argv) == 1:
    print("Usage: python statistics_analysis.py <source path>")
    sysexit()
else:
    source_dir = argv[1]

dataset = np.genfromtxt(source_dir, delimiter=",", skip_header=1, usecols=[2,3])
reflections = dataset[:,0]
edges = dataset[:,1]

print("Dataset: " + str(dataset))
#print("Maximum reflection: " + str(np.amax(reflections)))

def show_edge_histogram():
    fig = plt.figure(figsize =(10, 7))
    plt.hist(edges, bins = 70)
    plt.title("Edge histogram")
    plt.show()

def show_reflection_histogram():
    fig = plt.figure(figsize =(10, 7))
    plt.hist(reflections, bins = 50, range=(0,10), log=True)
    plt.title("Reflection histogram")
    plt.show()

def determine_if_glasses():
    with open (source_dir, 'r') as file:
        with open('output.csv', 'w', newline="\n") as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow(["last_dir", "filename", "percentage", "line_amount", "determined_glasses", "is_correct"])
            csvreader = csv.reader(file)
            row0 = next(csvreader)
            row0.append("determined_glasses")
            row0.append("is_correct")
        
            for line in csvreader:
                if line[0] == "last_dir":
                    continue
                else:
                    if float(line[2]) > 0 or float(line[3]) > 20:
                        line.append(1)
                        if(line[0] == "glasses"):
                            line.append(1)
                        else:
                            line.append(0)
                        
                        #print(line[1] + " has glasses")
                    else:
                        line.append(0)
                        if(line[0] == "no_glasses"):
                            line.append(1)
                        else:
                            line.append(0)
                        
                        #print(line[1] + " has no glasses")

                    csvwriter.writerow(line)
                    
def determine_error_rate():
    far = 0
    frr = 0
    total_counted = 0
    is_correct = np.genfromtxt("output.csv", delimiter=",", skip_header=1, usecols=[4,5])
    for value in is_correct:
        if value[0] == 1 and value[1] == 0:
            far += 1
        elif value[0] == 0 and value[1] == 0:
            frr += 1
        total_counted += 1
    print("Total images: " + str(total_counted))
    print("Errors: " + str(frr + far))
    print("False Acceptance Rate (glasses present, not detected): " + str(100*far/total_counted) + "%")
    print("False Rejection Rate (glasses not present, but detected): " + str(100*frr/total_counted) + "%")
    print("Total error rate: " + str(100*(far+frr)/total_counted) + "%")
    print("Total correct: " + str(100*(total_counted - (far+frr))/total_counted) + "%")

determine_if_glasses()
determine_error_rate()