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

hours = [ "22", "23", "01", "02", "03", "04", "05" ]

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
        moving_averages(y, "size")

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
        moving_averages(y, "velocity")

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

def moving_averages(values, type):
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    prediction = sum(values) / len(values)
    hours.append("06")
    values.append(prediction)

    plt.plot(hours, values)

    plt.savefig(f"moving_averages_{type}.png")

def exponential_smoothing(values, type):
    alpha = 0.5
    values_hat = []

    for hour in hours:
        values.append(get_axes_mean(hour, 0))
        values_hat.append(alpha * y[-1] + (1 - alpha) * y[-2])

    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(hours, values)
    plt.plot(hours, values_hat)
    plt.savefig(f"exponential_smoothing_{type}.png")
    

if __name__ == "__main__":
    size()
    velocity()
