import argparse
import matplotlib.pyplot as plt
import numpy as np

colors = ("red", "green", "blue", "yellow", "purple")

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cluster", help="Select cluster number",
                    default=0, type=int)
args = parser.parse_args()

# Get number of clusters from keyboard input
num_clusters = args.cluster


def main():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    # Get cluster data and make a scatter plot
    for i in range(num_clusters):
        x_norm, y_norm = get_cluster_norm_values(i)
        plt.plot(x_norm, y_norm, 'o', color=colors[i], markersize=3, label=f"Cluster {i}")

    # Plot data
    plt.xlabel("Tamaño (MB)")
    plt.ylabel("Velocidad (MB/s)")
    plt.title(
        f"K-Means Algorithm with Euclidean Distance of {num_clusters} clusters")
    plt.legend(loc="upper right")
    plt.savefig(f"cluster_{num_clusters}.png")


def get_cluster_norm_values(value):
    with open(f"cluster{num_clusters}.arff", "r") as file:
        data = file.read().splitlines()

    # Remove header
    data = data[9:]

    # Create an array with the cluster data
    cluster_value = []
    for line in data:
        line = line.split(',')
        if line[4] == f"cluster{value}":
            cluster_value.append([line[1], line[3]])

    # Create diferent arrays for each axis
    cluster_x = [float(x[0]) for x in cluster_value]
    cluster_y = [float(x[1]) for x in cluster_value]

    # Return a tuple
    return cluster_x, cluster_y


def normalize(value, min, max):
    return (value - min) / (max - min)


if __name__ == "__main__":
    main()
