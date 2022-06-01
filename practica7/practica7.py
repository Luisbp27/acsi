import numpy as np
import statistics
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


def velocity():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    ax_velocity = plt.axes()

    if args.group == 0:
        for hour in hours:
            x, y = get_axes_ungrouped(2)
            ax_velocity.scatter(x, y)
    else:
        for hour in hours:
            x, y = get_axes_mean(hour, 2)
            ax_velocity.scatter(x, hour)

    # Plot data of velocity
    ax_velocity.set_title("Velocity")
    ax_velocity.set_xlabel('Time (h)')
    ax_velocity.set_ylabel('Velocity (MB/s)')
    plt.savefig("velocity.png")


def size():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    ax_size = plt.axes()

    if args.group == 0:
        for hour in hours:
            x, y = get_axes_ungrouped(0)
            ax_size.scatter(x, y)
    else:
        for hour in hours:
            x = get_axes_mean(hour, 0)
            ax_size.scatter(x, hour)

    # Plot data of size
    ax_size.set_title("Size")
    ax_size.set_xlabel('Time (h)')
    ax_size.set_ylabel('Size (MB)')
    plt.savefig("size.png")


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


if __name__ == "__main__":
    size()
    velocity()
