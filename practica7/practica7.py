import numpy as np
import statistics
from pyparsing import line
from scipy import stats
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--group", help="Select group or ungrouped data",
                    default=1, type=int)
args = parser.parse_args()

group = args.group

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[8:]

hours = sorted(list({x.split(',')[1] for x in data}))

print(hours)


def size():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    if group == 0:
        x, y = get_axes(0)
        plt.scatter(x, y, s = 3)
        
    else:
        for hour in hours:
            y = get_axes_mean(hour, 0)
            plt.scatter(hour, y, s = 8)
        
        lineal_regression(y, "size")

    # Plot data of size
    plt.title("Size")
    plt.xlabel('Time (h)')
    plt.ylabel('Size (MB)')
    plt.savefig(f"size_{group}.png")


def velocity():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    if group == 0:
        x, y = get_axes(2)
        plt.scatter(x, y, s = 3)
    else:
        for hour in hours:
            y = get_axes_mean(hour, 2)
            plt.scatter(hour, y, s = 8)

        lineal_regression(y, "velocity")

    # Plot data of velocity
    plt.title("Velocity")
    plt.xlabel('Time (h)')
    plt.ylabel('Velocity (MB/s)')
    plt.savefig(f"velocity_{group}.png")

def format(x):
    return float(('%.4f' % x).rstrip('0').rstrip('.'))

def get_axes(value):
    x = []
    y = []

    for line in data:
        line = line.split(',')
    
        x.append(int(line[1]))
        y.append(float(line[value]))

    return x, y


def get_axes_mean(hour, value):
    x = []

    for line in data:
        line = line.split(',')
        if line[1] == hour:
            x.append(float(line[value]))

    if value == 0:
        return format(np.mean(x))
    else:
        return format(statistics.harmonic_mean(x))


def lineal_regression(y, type):
    plt.figure()
    plt.scatter(hours, y)

    m, b = np.polyfit(hours, y, 1)
    plt.plot(hours, m*np.array(hours)+b)

    plt.savefig(f"lineal_regression_{type}.png")

def moving_averages():
    pass

def exponential_smoothing():
    pass

if __name__ == "__main__":
    size()
    velocity()
