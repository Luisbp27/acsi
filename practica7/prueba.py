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


def main():
    plt.figure()
    plt.rcParams.update({"font.family": "serif"})

    x, y = get_axes(0)
    plt.plot(x, y, 'o', color='red', markersize=3)
            
    # Plot data of size
    plt.title("Size")
    plt.xlabel('Time (h)')
    plt.ylabel('Size (MB)')
    plt.savefig(f"size_{group}.png")


def get_axes(value):

    axes = []
    for line in data:
        line = line.split(',')
        axes.append([line[value], line[1]])

    x = [float(x[0]) for x in axes]
    y = [int(x[1]) for x in axes]

    return x, y

if __name__ == "__main__":
    main()