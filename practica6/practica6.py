import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file",
                    default="data.in", type=str)
parser.add_argument('-c', "--csv",   help="csv format?",
                    action=argparse.BooleanOptionalAction)
args = parser.parse_args()

def main():
    with open(args.input) as file:
        data = file.read().splitlines()

    # Remove header
    data.pop(0)
    with open(f"data.{'csv' if args.csv else 'arff'}", "x") as output:
        if args.csv:
            output.write("size,hour,MB/s\n")
        else:
            output.write("@relation data-server\n\n")
            output.write("@attribute SIZE numeric\n")
            output.write("@attribute HOUR numeric\n")
            output.write("@attribute MBS numeric \n")
            output.write("\n@data\n\n")

        for line in data:
            line = line.split(",")

            # Remove first -1
            if line[0] == "-1":
                continue

            # Remove last part
            try:
                line.pop(2)
            except:
                pass

            # Split values
            try:
                temp = line[1].split("\t")
            except:
                print(line)
            
            line[1] = temp[0]

            # Refractor numbers
            line.append(fractor_number(temp[1]))

            output.write(f"{line[0]},{line[1]},{line[2]}\n")

def fractor_number(number):
    temp = number.split(".")

    if len(temp) == 3:
        return f"{temp[0]}{temp[1]}.{temp[2]}"
    else:
        return number

if __name__ == "__main__":
    main()
