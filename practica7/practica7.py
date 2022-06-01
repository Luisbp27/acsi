import numpy as np
import statistics
from scipy import stats
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--group", help="Select group or ungrouped data",
                    default=0, type=int)
args = parser.parse_args()

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[8:]

hours = sorted(list({x.split(',')[1] for x in data}))


def size():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    ax_size = plt.axes()

    x_size = []

    if args.group == 0:
        for hour in hours:
            x, y = get_axes_ungrouped(0)
            ax_size.scatter(x, y)
    else:
        for hour in hours:
            x = get_axes_mean(hour, 0)
            ax_size.scatter(x, hour)
            x_size.append(x)

        lineal_regression(x_size)
        moving_averages(x_size)
        exponential_smoothing(x_size)

    # Plot data of size
    ax_size.set_title("Size")
    ax_size.set_xlabel('Time (h)')
    ax_size.set_ylabel('Size (MB)')
    plt.savefig("size.png")


def velocity():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    ax_velocity = plt.axes()

    x_velocity = []

    if args.group == 0:
        for hour in hours:
            x, y = get_axes_ungrouped(2)
            ax_velocity.scatter(x, y)
    else:
        for hour in hours:
            x, y = get_axes_mean(hour, 2)
            ax_velocity.scatter(x, hour)
            x_velocity.append(x)

        lineal_regression(x_velocity)
        moving_averages(x_velocity)
        exponential_smoothing(x_velocity)

    # Plot data of velocity
    ax_velocity.set_title("Velocity")
    ax_velocity.set_xlabel('Time (h)')
    ax_velocity.set_ylabel('Velocity (MB/s)')
    plt.savefig("velocity.png")


def get_axes_mean(hour, value):
    x = []

    for line in data:
        line = line.split(',')
        if line[1] == hour:
            x.append(float(line[value]))

    if value == 0:
        return np.mean(x)
    else:
        return statistics.harmonic_mean(x)


def get_axes_ungrouped(value):
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
