import numpy as np
from scipy.stats import norm
import math
import random

N = 7
Y = 3

def read_data(file_name):
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

# def load_data(filename):
#     data = np.array([[float(x) for x in line.strip().split('\t')] for line in open(filename).readlines()])
#     # print('Loaded %d observations.'%len(data))
#     return data

def condprob(x, n, y, params):
    mu = params[n][y]['mean']
    sigma = params[n][y]['var']
    pdf = (1 / (sigma * math.sqrt(2 * 3.14))) * math.exp(-1 * math.pow(x - mu, 2) / (2 * math.pow(sigma, 2)))
    return pdf

def learn(data):
    params = {}
    for n in range(N):
        params[n] = {}
        for y in range(Y):
            params[n][y] = {}
            subset = []
            for obs in data:
                if obs[-1] == y:
                    subset.append(obs[n])
            params[n][y]['mean'] = np.mean(subset)
            params[n][y]['var'] = np.var(subset)
    return params

def classify(obs, params):
    ans = []
    for y in range(Y):
        prob  = 1
        for n in range(N):
            if n == 2:
                continue
            prob *= condprob(obs[n], n, y, params)
        ans.append(prob)
    # print(ans)
    return ans


def demo():
    data = read_data('seeds_dataset.txt')
    train_data = random.sample(data, k = int(0.3 * 210))
    test_data = random.sample(data, k = int(0.7 * 210))

    params = learn(train_data)

    correct = 0
    np.seterr(divide='ignore', invalid='ignore')
    for obs in test_data:
        print(obs, end='-- ')
        result = classify(obs, params)
        result = np.array(result) / np.sum(result)
        if np.argmax(result) == obs[-1]:
            correct += 1
        print(result, end=' -- ')
        print(np.argmax(result))
    print('accuracy:', correct / len(test_data))

if __name__ == '__main__':
    demo()