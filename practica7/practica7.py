import numpy as np
import statistics
import matplotlib.pyplot as plt
import argparse
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--group", help="Select group or ungrouped data",
                    default=1, type=int)
args = parser.parse_args()

group = args.group

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[8:]

hours_label = ["22", "23", "01", "02", "03", "04", "05"]
hours = np.arange(7)


def size():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    y_values = []

    if group == 0:
        x, y = get_axes(0)
        plt.scatter(x, y, s=3)

        plt.title("Tamaño")
        plt.xlabel('Tiempo (h)')
        plt.ylabel('Tamaño (MB)')
        plt.savefig(f"size_{group}.png")

    else:
        for hour in hours_label:
            y = get_axes_mean(hour, 0)
            plt.scatter(hour, y, s=10, c="blue")
            plt.xticks(hours, hours_label)

            # Data for post-processing
            y_values.append(y)

        plt.title("Tamaño")
        plt.xlabel('Tiempo (h)')
        plt.ylabel('Tamaño (MB)')
        plt.savefig(f"size_{group}.png")

        # Post-processing
        linear_regression(y_values, "Tamaño (MB)")
        moving_means(y_values, "Tamaño (MB)")
        exponential_smoothing(y_values, "Tamaño (MB)")


def velocity():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    y_values = []

    if group == 0:
        x, y = get_axes(2)
        plt.scatter(x, y, s=3)

        plt.title("Velocidad")
        plt.xlabel('Tiempo (h)')
        plt.ylabel('Velocidad (MBps)')
        plt.savefig(f"velocity_{group}.png")

    else:
        for hour in hours_label:
            y = get_axes_mean(hour, 2)
            plt.scatter(hour, y, s=10, c="blue")
            plt.xticks(hours, hours_label)

            # Data for post-processing
            y_values.append(y)

        plt.title("Velocidad")
        plt.xlabel('Tiempo (h)')
        plt.ylabel('Velocidad (MBps)')
        plt.savefig(f"velocity_{group}.png")

        # Post-processing
        linear_regression(y_values, "Velocidad (MBps)")
        moving_means(y_values, "Velocidad (MBps)")
        exponential_smoothing(y_values, "Velocidad (MBps)")


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
    y = []

    # Get data for especific hour
    for line in data:
        line = line.split(',')
        if line[1] == hour:
            y.append(float(line[value]))

    # Calculate mean
    if value == 0:
        return format(np.mean(y))
    else:
        return format(statistics.harmonic_mean(y))


def linear_regression(y, type):
    x = np.arange(len(y))

    # Plot data
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(x, y, s=10, c="blue")

    # Linear regression
    regr = LinearRegression().fit(x.reshape(-1, 1), y)
    plt.plot(x, regr.predict(x.reshape(-1, 1)), color='red')

    # Save plot
    plt.xticks(x, hours_label)
    plt.title(f"Regresión Lineal de {type}")
    plt.xlabel('Tiempo (h)')
    plt.ylabel(f"{type}")
    plt.savefig(f"linear_regression_{type}.png")


def moving_means(y, type):
    i = 1
    moving_averages = []
    cum_sum = np.cumsum(y)
    x = np.arange(len(y))

    while i <= len(y):
        window_average = round(cum_sum[i-1] / i, 2)
        moving_averages.append(window_average)
        i += 1

    # Plot data
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(x, y, s=10, c="blue")

    # Plot moving averages
    plt.plot(x, moving_averages, color="red")

    # Save plot
    plt.xticks(x, hours_label)
    plt.title(f"Media Móvil de {type}")
    plt.xlabel('Tiempo (h)')
    plt.ylabel(f"{type}")
    plt.savefig(f"moving_means_{type}.png")


def exponential_smoothing(y, type):
    x = np.arange(len(y))

    # Plot data
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(x, y, s=10, c="blue")

    # Exponential smoothing
    alpha = 0.6
    smoothed = [y[0]]
    for i in range(1, len(y)):
        smoothed.append(alpha * y[i] + (1 - alpha) * smoothed[i-1])

    # Plot exponential smoothing
    plt.plot(x, smoothed, color="red")

    # Save plot
    plt.xticks(x, hours_label)
    plt.title(f"Suavizado Exponencial de {type}")
    plt.xlabel('Tiempo (h)')
    plt.ylabel(f"{type}")
    plt.savefig(f"exponential_smoothing_{type}.png")


if __name__ == "__main__":
    size()
    velocity()
