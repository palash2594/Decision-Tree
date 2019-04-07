import numpy as np
import collections
import math

class Node:

    __slots__ = "name", "split_point", "left", "right"

    def __init__(self, name, split_point):
        self.name = name
        self.split_point = split_point

def read_data(file_name):
    data = []

    file_data = open("iris.data.txt", "r")

    for line in file_data:
        line = line.strip().split(",")
        temp = []
        for item in line[0:len(line)]:
            temp.append(float(item))
        data.append(temp)

    file_data.close()

    return data

def get_greater_counts(data, column, split_point):
    counts = [0, 0, 0, 0]

    for i in range(len(data)):
        if data[i][column] > split_point:
            counts[int(data[i][4])] += 1

    return counts

def get_smaller_counts(data, column, split_point):
    counts = [0, 0, 0, 0]

    for i in range(len(data)):
        if data[i][column] <= split_point:
            counts[int(data[i][4])] += 1

    return counts

def find_initial_entropy(data, removed_attribute):
    a = np.array(data)
    means = a.mean(axis=0)

    freq_class = dict(collections.Counter(a[:,4]))
    sum_class = 0

    for key in freq_class:
        sum_class += freq_class[key]

    class_entropy = 0
    for key in freq_class:
        class_entropy += (freq_class[key] / sum_class * math.log(freq_class[key] / sum_class, 2))

    class_entropy *= -1
    print("class entropy: ", class_entropy)

    means = []
    for i in range(4):
        means.append(np.mean(a[:,i]))

    # g_counts = get_greater_counts(a, 0, means[0])
    # s_counts = get_smaller_counts(a, 0, means[0])

    gains = []

    for attribute in range(4):
        if attribute == removed_attribute:
            gains.append(0)
            continue
        g_att_entropy = 0
        s_att_entropy = 0
        g_counts = get_greater_counts(a, attribute, means[attribute])
        s_counts = get_smaller_counts(a, attribute, means[attribute])
        for i in range(0, len(g_counts)):
            if g_counts[i] <= 0:
                continue
            g_att_entropy += (g_counts[i]/sum(g_counts) * math.log(g_counts[i]/sum(g_counts), 2))

        for i in range(0, len(s_counts)):
            if s_counts[i] <= 0:
                continue
            s_att_entropy += (s_counts[i]/sum(s_counts) * math.log(s_counts[i]/sum(s_counts), 2))

        count = sum(g_counts) + sum(s_counts)
        att_entropy = -1 * (sum(g_counts) / count * g_att_entropy + sum(s_counts) / count * s_att_entropy)
        gain = class_entropy - att_entropy
        gains.append(gain)

        # print(g_att_entropy, s_att_entropy)
        # print(att_entropy)

    return gains.index(max(gains)), max(gains), means[gains.index(max(gains))]


def get_data(data, attribute, split_point):
    data_low = []
    data_high = []

    for row in data:
        if row[attribute] <= split_point:
            data_low.append(row)
        else:
            data_high.append(row)

    return data_low, data_high


def find_entropy(data, current, depth, remove_attribute):

    root = None
    if depth < 5:
        attribute, gain, split_point = find_initial_entropy(data, remove_attribute)

    # if current == None:
    #     attribute, gain, split_point = find_initial_entropy(data, attributes)
    #     root = Node(attribute, split_point)
    # else:
    #     attribute, gain, split_point = find_initial_entropy(data, attributes)

        root = Node(attribute, split_point)
        data_low, data_high = get_data(data, attribute, split_point)

        remove_attribute = attribute

        root.left = find_entropy(data_low, root, depth + 1, remove_attribute)
        root.right = find_entropy(data_high, root, depth + 1, remove_attribute)

    return root

    a = np.array(data)
    print(type(a))
    # print(a)
    means = a.mean(axis=0)

if __name__ == '__main__':

    data = read_data("iris.data.txt")
    attributes = [0, 1, 2, 3]
    attribute, gain, split_point = find_initial_entropy(data, -1)
    print(attribute, gain, split_point)
    root = Node(attribute, split_point)

    # find_entropy(data, root, 0)

    # print(data)