
__author__ = "Palash Jain"

"""
This is an implementation of the bayesian network.
"""

import numpy as np
import math
import random

N = 0
Y = 0

def read_data(file_name):
    """
    to read the input data file
    :param file_name: name of the file
    :return: read data in list of list
    """
    data = []

    file_data = open("seeds_dataset.txt", "r")

    for line in file_data:
        line = line.strip().split("\t")
        temp = []
        for item in line[0:len(line)]:
            temp.append(float(item))
        data.append(temp)
    file_data.close()

    return data

def condprob(x, n, y, mean, var):
    """
    to find the conditional probability
    :param x: Values at which to evaluate pdf
    :param n: the nth attribute
    :param y: the yth class
    :param mean: the mean for every attribute and class
    :param var: the variance for every attribute and class
    :return: the conditional probability
    """
    mu = mean[n][y]
    sigma = var[n][y]
    pdf = (1 / (sigma * math.sqrt(2 * 3.14))) * math.exp(-1 * math.pow(x - mu, 2) / (2 * math.pow(sigma, 2)))
    return pdf

def learn_data(data):
    """
    this function calculates the mean and variance for attribute corresponding to a class
    :param data: data set
    :return: calculated mean and variance
    """
    mean = {}
    var = {}
    for n in range(N):
        mean[n] ={}
        var[n] = {}
        for y in range(Y):
            subset = []
            for obs in data:
                if obs[-1] == y:
                    subset.append(obs[n])
            mean[n][y] = np.mean(subset)
            var[n][y] = np.var(subset)
    return mean, var

def classify(obs, mean, var):
    """
    to classify data inputs in a class
    :param obs: one of the observation
    :param mean: the mean of attributes corresponding to a class
    :param var: the variance of attributes corresponding to a class
    :return: the probability of the observation to be in any particular class
    """
    ans = []
    for y in range(Y):
        prob  = 1
        for n in range(N):
            if n == 2:
                continue
            prob *= condprob(obs[n], n, y, mean, var)
        ans.append(prob)
    # print(ans)
    return ans

def bayes_classifier():
    """
    this function manages the flow of the program
    :return:
    """
    data = read_data('seeds_dataset.txt')

    data_column = list(zip(*data))
    global N
    global Y
    Y = len(set(data_column[7]))
    N = len(data[0]) - 1

    random.shuffle(data)
    train_data = [data[0:len(data) // 3], data[len(data) // 3 + 1 : 2 * len(data) // 3 + 1], data[2 * len(data) // 3 : ]]

    test_data = [data[len(data) // 3 : ], data[0 : len(data) // 3 + 1] + data[2 * len(data) // 3 + 1 : ], data[0 : 2 * len(data) // 3]]

    print("Total inputs: " , len(data))
    print()

    for i in range(3):
        print("Inputs used for training: ", len(train_data[i]))
        print("Inputs used for testing:", len(test_data[i]))
        mean, var = learn_data(train_data[i])

        correct = 0
        np.seterr(divide='ignore', invalid='ignore')
        for obs in test_data[i]:
            # print(obs, end='-- ')
            result = classify(obs, mean, var)
            result = np.array(result) / np.sum(result)
            if np.argmax(result) == obs[-1]:
                correct += 1
            # print(result, end=' -- ')
            # print(np.argmax(result))
        print('Accuracy:', correct / len(test_data[i]))
        print()

if __name__ == '__main__':
    bayes_classifier()