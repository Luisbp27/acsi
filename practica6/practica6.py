import csv

reader = []

with open("data.csv", "r") as csvfile:
    reader = csv.reader(csvfile)

salida = []

for row in reader:
    print(reader)
    
csvfile.close()