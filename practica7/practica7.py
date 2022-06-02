import numpy as np
import statistics
from scipy import stats
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--group", help="Select group or ungrouped data",
                    default=0, type=int)
args = parser.parse_args()

group = args.group

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[8:]

hours = sorted(list({x.split(',')[1] for x in data}))


def size():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    x_arr = []
    y_arr = []

    if group == 0:
        x, y = get_axes(0)
        plt.scatter(x, y)
        x_arr.append(x)
        y_arr.append(y)
        
    else:
        x_size = []

        for hour in hours:
            x = get_axes_mean(hour, 0)
            plt.scatter(x, hour)
            x_size.append(x)

    print(y_arr)

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
        plt.scatter(x, y)
    else:
        x_velocity = []

        for hour in hours:
            x, y = get_axes_mean(hour, 2)
            plt.scatter(x, hour)
            x_velocity.append(x)

    # Plot data of velocity
    plt.title("Velocity")
    plt.xlabel('Time (h)')
    plt.ylabel('Velocity (MB/s)')
    plt.savefig(f"velocity_{group}.png")

def format(x):
    return float(('%.4f' % x).rstrip('0').rstrip('.'))

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


def get_axes(value):
    x = []
    y = []

    for line in data:
        line = line.split(',')
        x.append(float(line[value]))
        y.append(int(line[1]))

    return x, y

def lineal_regression(values):
    model = list(map(regression(values), values))

    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(values, hours)
    plt.plot(values, model)
    plt.savefig("lineal_regression.png")


def regression(values):
    slope, intercept, r_value, p_value, std_err = stats.linregress(values, hours)

    return slope * values + intercept

def moving_averages():
    pass

def exponential_smoothing():
    pass

if __name__ == "__main__":
    size()
    velocity()
