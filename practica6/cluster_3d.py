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
    ax = plt.axes(projection='3d')

    # Get cluster data and make a scatter plot
    for i in range(num_clusters):
        x_norm, y_norm, z_norm = get_cluster_norm_values(i)
        ax.scatter3D(x_norm, y_norm, z_norm,
                     label=f"Cluster {i}", c=colors[i], marker="o", s=5.0)

    # Plot data
    ax.set_title(
        f"K-Means Algorithm with Euclidean Distance of {num_clusters} clusters")
    ax.set_xlabel('Size (MB)')
    ax.set_ylabel('Time (h)')
    ax.set_zlabel('Speed (MB/s)')
    ax.legend(loc="upper right")
    plt.savefig(f"cube_{num_clusters}.png")


def get_cluster_norm_values(value):
    with open(f"cluster{num_clusters}.arff", "r") as file:
        data = file.read().splitlines()

    # Remove header
    data = data[8:]

    # Create an array with the cluster data
    cluster_value = []
    for line in data:
        line = line.split(',')
        if line[4] == f"cluster{value}":
            cluster_value.append([line[1], line[2], line[3]])

    # Create diferent arrays for each axis
    cluster_x = [float(x[0]) for x in cluster_value]
    cluster_y = [float(x[1]) for x in cluster_value]
    cluster_z = [float(x[2]) for x in cluster_value]

    # Get min and max values
    x_mn = [np.min(cluster_x), np.max(cluster_x)]
    y_mn = [np.min(cluster_y), np.max(cluster_y)]
    z_mn = [np.min(cluster_z), np.max(cluster_z)]

    # Normalize data
    x_norm = [normalize(data, x_mn[0], x_mn[1]) for data in cluster_x]
    y_norm = [normalize(data, y_mn[0], y_mn[1]) for data in cluster_y]
    z_norm = [normalize(data, z_mn[0], z_mn[1]) for data in cluster_z]

    # Return a tuple
    return x_norm, y_norm, z_norm


def normalize(value, min, max):
    return (value - min) / (max - min)


if __name__ == "__main__":
    main()
