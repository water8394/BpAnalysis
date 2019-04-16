import pandas as pd

import numpy
import tensorflow as tf
from commons.load_indicator import load
from commons.utils import measure_difference
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

rng = numpy.random

df = load()
df = df.loc[:70, :]
# print(df)
train_X, test_X, train_Y, test_Y = train_test_split(
    df[['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2']], df['high_pluse'])
train_out = train_Y
train_Y = [[_] for _ in train_Y]

tf_x = tf.placeholder(tf.float32, [None, 10])  # input x
tf_y = tf.placeholder(tf.float32, [None, 1])  # input y

# neural network layers
l1 = tf.layers.dense(tf_x, 30, tf.nn.relu)  # hidden layer
l2 = tf.layers.dense(tf_x, 60, tf.nn.relu)  # hidden layer
l1_output = tf.layers.dense(l1, 1)
output = tf.layers.dense(l1_output, 1)

loss = tf.losses.mean_squared_error(tf_y, output)  # compute cost
optimizer = tf.train.AdamOptimizer(learning_rate=0.1)
train_op = optimizer.minimize(loss)

sess = tf.Session()  # control training and others
sess.run(tf.global_variables_initializer())  # initialize var in graph

for step in range(1500):
    # train and net output
    _, l, pred = sess.run([train_op, loss, output], {tf_x: train_X, tf_y: train_Y})
    if step % 10 == 0:
        print('loss is: ' + str(l))
        # print(pred)
        # print('prediction is:' + str(pred))

output_pred = sess.run(output, {tf_x: test_X})

res = [_[0] for _ in output_pred]
# print(train_out,test_Y)
print(len(train_out), len(output_pred))
loss = mean_absolute_error(test_Y, output_pred)
measure_difference(output_pred, test_Y, loss)
