#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import struct
import sys

from utility import load_mnist_images, load_mnist_labels, sigmoid, \
init_parameters, create_batch


def extract_target_data(X, Y, target):
    p = (Y == target)
    return X[p], Y[p]

def extract_target_label(Y, target):
    Y_t = (Y == target)
    return np.expand_dims(Y_t, axis=0)

def logistic_propagate(X, Y, w, b, lambd):
    m = Y.shape[-1]
    Z = np.dot(w, X) + b
    A = sigmoid(Z)

    cost = - np.sum(Y * np.log(A) + (1-Y) * np.log(1-A)) / m

    cost += lambd * np.linalg.norm(w) / m  # L2 Regularization
    #cost += lambd * np.linalg.norm(w, 1)    # L1 Regularization

    dw = np.dot((A - Y), X.T) / m + 2 * lambd * w / m
    db = np.sum((A - Y), axis=1, keepdims=True) / m

    grad = {'dw':dw, 'db':db}

    return grad, cost


def optimize(X, Y, w, b, learning_rate, lambd):
    grad, cost = logistic_propagate(X, Y, w, b, lambd)

    dw = grad['dw']
    db = grad['db']

    w -= learning_rate * dw
    b -= learning_rate * db

    return w, b, cost


class LogisticRegression(object):

    def __init__(self, n_feature, n_epoch, batch_size=32, learning_rate=0.001, lambd=0.01):
        self.n_epoch = n_epoch
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.lambd = lambd
        self.w, self.b = init_parameters(n_feature, 1)
        self.cost = -1.

    def fit(self, X, Y):
        for i in range(self.n_epoch):
            X_batches, Y_batches, n_batch = create_batch(X, Y, self.batch_size)

            for j in range(n_batch):
                self.w, self.b, self.cost = optimize(X_batches[j], Y_batches[j], self.w, self.b, self.learning_rate, self.lambd)

            if i % 20 == 0: print('%d epoches cost: %f' % (i, self.cost))

    def predict(self, X, Y):
        m = X.shape[-1]

        Z = np.dot(self.w, X) + self.b
        A = sigmoid(Z)

        self.Y_p = (A > 0.5)
        correct = (self.Y_p == Y)
        self.accuracy = np.sum(correct) / m

def __main__():
    train_images = load_mnist_images('train-images.idx3-ubyte', 2000)
    train_labels = load_mnist_labels('train-labels.idx1-ubyte', 2000)
    test_images = load_mnist_images('t10k-images.idx3-ubyte', 200)
    test_labels = load_mnist_labels('t10k-labels.idx1-ubyte', 200)

    '''
    # Show A Image
    plt.gray()
    plt.imshow(train_images[50])
    plt.show()
    '''

    m_train = train_images.shape[0]
    m_test = test_images.shape[0]
    train_X = train_images.reshape(m_train, -1).T / 255.
    test_X = test_images.reshape(m_test, -1).T / 255.

    train_X_2 = train_X
    train_Y_2 = extract_target_label(train_labels, 2)
    test_X_2 = test_X
    test_Y_2 = extract_target_label(test_labels, 2)

    n_feature = train_X.shape[0]

    sigmoid_2_model = LogisticRegression(n_feature, n_epoch=400)
    sigmoid_2_model.fit(train_X_2, train_Y_2)
    sigmoid_2_model.predict(test_X_2, test_Y_2)
    print('Softmax Regression on Category 2 Accuracy: %f %%' % (sigmoid_2_model.accuracy * 100))

__main__()