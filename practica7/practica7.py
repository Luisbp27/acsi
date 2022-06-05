import numpy as np
import statistics
import matplotlib.pyplot as plt

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[8:]

hours_label = ["22", "23", "01", "02", "03", "04", "05"]
pred_hours_label = ["22", "23", "01", "02", "03", "04", "05", "06"]
hours = np.arange(len(hours_label))


def size():
    # Plot initialization
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    y_values = []

    # Get data for especific hour
    for hour in hours_label:
        y = get_axes_mean(hour, 0)
        plt.scatter(hour, y, s=10, c="blue")
        plt.xticks(hours, hours_label)

        # Data for post-processing
        y_values.append(y)

    # Save plot
    plt.title("Media de los Tamaños (MB) frente al Tiempo (h)")
    plt.xlabel('Tiempo (h)')
    plt.ylabel('Tamaño (MB)')
    plt.savefig(f"size.png")

    # Post-processing
    linear_regression(y_values, "Tamaño (MB)")
    moving_means(y_values, "Tamaño (MB)")
    exponential_smoothing(y_values, "Tamaño (MB)")


def velocity():
    # Plot initialization
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    y_values = []

    # Get data for especific hour
    for hour in hours_label:
        y = get_axes_mean(hour, 2)
        plt.scatter(hour, y, s=10, c="blue")
        plt.xticks(hours, hours_label)

        # Data for post-processing
        y_values.append(y)

    # Save plot
    plt.title("Media de las Velocidades (MBps) frente al Tiempo (h)")
    plt.xlabel('Tiempo (h)')
    plt.ylabel('Velocidad (MBps)')
    plt.savefig(f"velocity.png")

    # Post-processing
    linear_regression(y_values, "Velocidad (MBps)")
    moving_means(y_values, "Velocidad (MBps)")
    exponential_smoothing(y_values, "Velocidad (MBps)")


def format(x):
    return float(('%.4f' % x).rstrip('0').rstrip('.'))


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
    
    # Calculate means
    x_mean = np.mean(x)
    if type == "Velocidad (MBps)":
        y_mean = statistics.harmonic_mean(y)
    else:
        y_mean = np.mean(y)

    # Calculate b
    b = (np.sum(y * x) - len(y) * x_mean * y_mean) / (np.sum(x * x) - len(x) * x_mean * x_mean)

    # Calculate a
    a = y_mean - b * x_mean

    # Plot data
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(x, y, s=10, c="blue")

    # Plot linear regression
    x_plot = np.arange(len(pred_hours_label))
    plt.plot(x_plot, a + b * x_plot, color='red')

    # Save plot
    plt.xticks(x_plot, pred_hours_label)
    plt.title(f"Regresión Lineal de {type}")
    plt.xlabel('Tiempo (h)')
    plt.ylabel(f"{type}")
    plt.savefig(f"linear_regression_{type}.png")


def moving_means(y, type):
    i = 1
    moving_averages = []
    cum_sum = np.cumsum(y)
    x = np.arange(len(y))

    # Calculate moving averages
    i = 4
    while i <= (len(y)):
        window_average = round(cum_sum[i-1] / i, 2)
        moving_averages.append(window_average)
        i += 1

    # Calulate moving averages for next hour
    moving_averages.append(np.sum(y[-4:])/4)

    # Plot data
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})
    plt.scatter(x, y, s=10, c="blue")

    # Plot moving averages
    x_plot = np.arange(3, 8)
    plt.plot(x_plot, moving_averages, color="red")

    # Save plot
    x = np.arange(len(pred_hours_label))
    plt.xticks(x, pred_hours_label)
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

    # Calculate moving averages for next hour
    smoothed.append(smoothed[-1])

    # Plot exponential smoothing
    x_plot = np.arange(8)
    plt.plot(x_plot, smoothed, color="red")

    # Save plot
    plt.xticks(x_plot, pred_hours_label)
    plt.title(f"Suavizado Exponencial de {type}")
    plt.xlabel('Tiempo (h)')
    plt.ylabel(f"{type}")
    plt.savefig(f"exponential_smoothing_{type}.png")


if __name__ == "__main__":
    size()
    velocity()
