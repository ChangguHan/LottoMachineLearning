# -*- coding:utf-8 -*-

import tensorflow.compat.v1 as tf
import numpy as np
import datetime, ssl
from items import GlobalMethod
from scripts import helpers

tf.disable_v2_behavior()

today = GlobalMethod.getToday()
dDay = GlobalMethod.getDDay()
thisTime = GlobalMethod.getthisTime()
learning_rate = 0.05
steps = 10

# nums받으면 회차 구해주기
def numsToTimeAndDays(nums):

    # 원하는 숫자만큼 회차로
    if nums == 1000: nums = thisTime - 1
    timeResult = []
    daysResult = []
    for i in range(nums):
        timeResult.append(thisTime - (i + 1))
        daysResult.append((dDay - datetime.timedelta(weeks=i + 1)).isoformat())

    return [timeResult, daysResult]

#  X,Y raw Data 구하기
def getXInputData(nums):
    [timeResult, daysResult] = numsToTimeAndDays(nums)

    result = []
    for j in range(len(timeResult)):
        sub_result = setXInputType(timeResult[j], daysResult[j])
        result.append(sub_result)

    return result

# time, day넣으면 X input 으로 바꾸기
def setXInputType(time , day) :
    print(time, day)

    result = []
    if (len(str(time))==1) :
        result.append(0)
        result.append(0)
        result.append(time)
    elif (len(str(time))==2) :
        result.append(0)
        result.append(int(str(time)[0]))
        result.append(int(str(time)[1]))
    elif (len(str(time))==3) :
        result.append(int(str(time)[0]))
        result.append(int(str(time)[1]))
        result.append(int(str(time)[2]))

    result.append(int(day[0:2]))
    result.append(int(day[2:4]))
    result.append(int(day[5:7]))
    result.append(int(day[8:10]))
    print(result)

    return result

def getYInputData(nums):
    result = []
    context = ssl._create_unverified_context()

    # nums to 회차
    timeResult = numsToTimeAndDays(nums)[0]


    for i_nums in timeResult:
        result.append(helpers.dbGetOriginData(i_nums))
    return result

def minmax(array):
    result_sub = []
    for i_col in range(len(array[0])):
        col = array[:, i_col]
        result_sub.append([min(col), max(col)])
    return result_sub

def normal(array):
    result = np.zeros((len(array), len(array[0])))
    for i_col in range(len(array[0])):
        col = array[:, i_col]
        for i_line in range(len(array)):
            if (max(col) - min(col) == 0):
                result[i_line, i_col] = 1
            else:
                result[i_line, i_col] = (array[i_line][i_col] - min(col)) / (max(col) - min(col))
    return result

def normal_new(array, base_array):

    base_array = minmax(base_array)
    result = []
    for i in range(len(array)):
        if (base_array[i][0] - base_array[i][1] == 0):
            result.append(1)
        else:
            result.append((array[i] - base_array[i][0]) / (base_array[i][1] - base_array[i][0]))
    return result

def getPredict(nums):

    x_raw = np.array(
        getXInputData(nums)
        , dtype=np.float32)
    y_raw = np.array(
        getYInputData(nums))

    x_data = normal(x_raw)
    print("x_data")
    print(x_data)

    y_data = []
    for i in y_raw:
        result = np.zeros(45)
        for j in i:
            result[int(j) - 1] = 1
        y_data.append(result)

    print("y_data")
    print(y_data)
    X = tf.placeholder("float", [None, 7])
    Y = tf.placeholder("float", [None, 45])
    nb_classes = 45

    W1 = tf.Variable(tf.random_normal([7, nb_classes]), name='weight1')
    b1 = tf.Variable(tf.random_normal([nb_classes]), name='bias1')
    layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

    W2 = tf.Variable(tf.random_normal([nb_classes, nb_classes]), name='weight2')
    b2 = tf.Variable(tf.random_normal([nb_classes]), name='bias2')

    matmul = tf.matmul(layer1, W2) + b2
    hypothesis = tf.nn.softmax(matmul)

    yAndhyp = -Y * tf.log(hypothesis)
    reduceSum = tf.reduce_sum(yAndhyp, axis=1)
    cost = tf.reduce_mean(reduceSum)

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        text = []

        for step in range(steps):

            _, val_W, val_b, val_layer, val_W2, val_b2, val_matmul, val_hyp, val_yAndhyp, val_redu, val_cost = sess.run(
                [optimizer, W1, b1, layer1, W2, b2, matmul, hypothesis, yAndhyp, reduceSum, cost],
                feed_dict={X: x_data, Y: y_data})

            if step == 5000 or step == 9999:
                text.append([step, val_cost])
            print(step, val_cost)

        # print("5000,", text[0][1])
        # print("9999,", text[1][1])

        x_new_data = [normal_new(
            setXInputType(thisTime, str(dDay))
            , x_raw)]

        expectation = sess.run(hypothesis, feed_dict={X: x_new_data})
        print(expectation * 100)
        map_expect = {}
        for i in range(len(expectation[0])):
            # map_expect[str(i+1)] = str(expectation[0][i])
            map_expect[int(i + 1)] = float(expectation[0][i])
        # print(map_expect)
        # map_expect_sorted = sorted(map_expect.items(), key=(lambda x:x[1]),reverse=True)
        # print(map_expect_sorted)

    return map_expect

    '''
    Test 7
    Input : 5개 데이터셋, 총 7개 인풋값
    회차 3개(각각), 년도 2개 (각각), 당첨 월 1개, 일 1개
    - normalize 방법 고침
    - deep2층, 45개 node
    - 확률뽑기 Logistic 추가


    0.05
    5000, 13.708403
    9999, 13.653595

    0.1
    5000, 13.65699
    9999, 13.635595

    0.3
    5000, 13.633786
    9999, 13.6266985

    0.5
    5000, 13.629497
    9999, 13.626805
    '''
