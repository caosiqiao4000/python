# encoding:utf-8

import tensorflow as tf
tf.enable_eager_execution()
print(tf.add(1, 2).numpy())

hello = tf.constant('Hello, TensorFlow!')
print(hello.numpy())