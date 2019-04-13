
__author__ = "Palash Jain"

"""
This is an implementation of decision tree.
"""

import numpy as np
import collections
import math
import random

class Node:

    """
    class to store every node in the tree
    """

    __slots__ = "name", "split_point", "left", "right", "data"

    def __init__(self, name, split_point, data):
        """
        initiallization of the node
        :param name: the name of the attribute
        :param split_point: the point on which spliting took place
        :param data: the data set corresponding to that node
        """
        self.name = name
        self.split_point = split_point
        self.data = data

def read_data(file_name):
    """
    to read the data from input file
    :param file_name: the name of the file
    :return: data read in list of list
    """
    data = []

    file_data = open(file_name, "r")

    for line in file_data:
        line = line.strip().split("\t")
        temp = []
        for item in line[0:len(line)]:
            temp.append(float(item))
        data.append(temp)

    file_data.close()

    return data

def get_greater_counts(data, column, split_point):
    """
    to count the class labels in the right portion of splited data
    :param data: the data set
    :param column: the attribute in focus
    :param split_point: the splitting point on which the data set is divided
    :return: the count of every class label the current portion of data
    """
    counts = [0, 0, 0, 0]

    for i in range(len(data)):
        if data[i][column] > split_point:
            counts[int(data[i][7])] += 1

    return counts

def get_smaller_counts(data, column, split_point):
    """
    to count the class labels in the right portion of splited data
    :param data: the data set
    :param column: the attribute in focus
    :param split_point: the splitting point on which the data set is divided
    :return: the count of every class label the current portion of data
    """
    counts = [0, 0, 0, 0]

    for i in range(len(data)):
        if data[i][column] <= split_point:
            counts[int(data[i][7])] += 1

    return counts

def find_best_entropy(data):
    """
    to calculate the best entropy
    :param data: the data set
    :param removed_attribute:
    :return:
    """
    a = np.array(data)
    means = a.mean(axis=0)

    freq_class = dict(collections.Counter(a[:,7]))
    sum_class = 0

    for key in freq_class:
        sum_class += freq_class[key]

    class_entropy = 0
    for key in freq_class:
        class_entropy += (freq_class[key] / sum_class * math.log(freq_class[key] / sum_class, 2))

    class_entropy *= -1
    # print("class entropy: ", class_entropy)

    means = []
    for i in range(7):
        means.append(np.mean(a[:,i]))

    gains = []

    for attribute in range(7):
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

    return gains.index(max(gains)), max(gains), means[gains.index(max(gains))]


def get_data(data, attribute, split_point):
    """
    to the data with respect to the split point
    :param data: the dataset
    :param attribute: the attribute by which the splitting occurs
    :param split_point: the split point
    :return: the splited data in two separate list
    """
    data_low = []
    data_high = []

    for row in data:
        if row[attribute] <= split_point:
            data_low.append(row)
        else:
            data_high.append(row)

    return data_low, data_high

def get_best_attribute(data):
    """
    to choose the best attribute by calculating the highest occurence of that attribute
    in the given data set
    :param data: the dataset
    :return: the best attribute
    """
    class_type = {}
    for item in data:
        if item[7] not in class_type:
            class_type[item[7]] = 1
        else:
            class_type[item[7]] += 1

    max = -1
    max_att = -1

    for key, value in class_type.items():
        if value > max:
            max = value
            max_att = key

    return max_att


def find_entropy(data, current, depth, split_point):
    """
    this is a recursive function which builds the decision tree
    :param data: the dataset
    :param current: the current attribute in focus
    :param depth: the current depth of the decision tree
    :param split_point:
    :return:
    """

    root = None
    if depth < 5:
        attribute, gain, split_point = find_best_entropy(data)

        root = Node(attribute, split_point, data)
        data_low, data_high = get_data(data, attribute, split_point)

        remove_attribute = attribute

        root.left = find_entropy(data_low, root, depth + 1, split_point)
        root.right = find_entropy(data_high, root, depth + 1, split_point)
    else:
        root = Node(get_best_attribute(data), None, data)
        root.left = None
        root.right = None

    return root

def traverse(root):
    """
    to print the decision tree
    :param root: the root of the tree
    :return:
    """
    while root is not None:
        print(root.name)

def test_decision_tree(root, input):
    """
    to test the decision tree's accuracy
    :param root: the root of the decision tree
    :param input: the input observation
    :return: the class label
    """
    attributes = ["Kama", "Rosa", "Canadian"]
    while root.split_point is not None:
        if root.split_point > input[root.name]:
            root = root.left
        else:
            root = root.right

    return int(root.name)

if __name__ == '__main__':

    data = read_data("seeds_dataset.txt")
    attributes = [0, 1, 2, 3]

    # train_data = random.sample(data, k = int(0.6 * 210))
    # test_data = random.sample(data, k = int(0.4 * 210))
    random.shuffle(data)
    train_data = [data[0:len(data) // 3], data[len(data) // 3 + 1 : 2 * len(data) // 3 + 1], data[2 * len(data) // 3 : ]]

    test_data = [data[len(data) // 3 : ], data[0 : len(data) // 3 + 1] + data[2 * len(data) // 3 + 1 : ], data[0 : 2 * len(data) // 3]]

    print("Total inputs: ", len(data))
    print()
    for i in range(3):
        print("Inputs used for Training: ", len(train_data[i]))
        print("Inputs used for Testing: ", len(test_data[i]))

        root = find_entropy(train_data[i], None, 0, 0)

        count = 0
        for input in test_data[i]:
            if input[7] == test_decision_tree(root, input):
                count += 1

        print("Accuracy: ", count / len(test_data[i]))

        print()