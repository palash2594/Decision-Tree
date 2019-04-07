import numpy as np
from scipy.stats import norm


N = 7
Y = 3

def load_data(filename):
    data = np.array([[float(x) for x in line.strip().split('\t')] for line in open(filename).readlines()])
    print('Loaded %d observations.'%len(data))
    return data

def condprob(x, n, y, params):
    return norm.pdf(x, params[n][y]['mean'], params[n][y]['var'])

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
            prob *= condprob(obs[n], n, y, params)
        ans.append(prob)
    return ans


def demo():
    train_data = load_data('seeds_dataset.txt')
    params = learn(train_data)

    test_data = load_data('seeds_dataset.txt')

    correct = 0
    for obs in test_data:
        print(obs, end='-- ')
        result = classify(obs, params)
        print(np.array(result))
        print(np.sum(result))
        result = np.array(result) / np.sum(result)
        if np.argmax(result) == obs[-1]:
            correct += 1
        print(result, end=' -- ')
        print(np.argmax(result))
    print('accuracy:', correct / len(test_data))

if __name__ == '__main__':
    demo()