import argparse
import matplotlib.pyplot as plt
import numpy as np

with open("data.arff", "r") as file:
    data = file.read().splitlines()

data = data[9:]

hours = set(data[1])

data_hours = []

def main():

    for i in range(len(data)):
        for j in range(len(hours)):
            if data[i][1] == hours[j]:
                pass
                


