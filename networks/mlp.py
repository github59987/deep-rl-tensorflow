import tensorflow as tf

from .layers import *
from .network import Network

class MLPSmall(Network):
  def __init__(self,
               sess,
               observation_dims,
               history_length,
               output_size,
               hidden_sizes=[],
               batch_size=None,
               weights_initializer=initializers.xavier_initializer(),
               biases_initializer=tf.zeros_initializer,
               hidden_activation_fn=tf.nn.relu,
               output_activation_fn=tf.nn.softmax,
               name='MLPSmall'):
    super(MLPSmall, self).__init__(sess)

    self.var = {}
    with tf.variable_scope(name):
      layer = self.inputs = tf.placeholder('float32', [batch_size, history_length] + observation_dims, 'inputs')

      if len(layer.get_shape().as_list()) == 3:
        assert layer.get_shape().as_list()[1] == 1
        layer = tf.reshape(layer, [-1] + layer.get_shape().as_list()[2:])

      for idx, hidden_size in enumerate(hidden_sizes + [output_size]):
        w_name = 'w%d' % idx
        w = tf.get_variable(w_name,
            [layer.get_shape().as_list()[-1], hidden_size], initializer=weights_initializer)
        self.var[w_name] = w

        if biases_initializer is None:
          layer = tf.matmul(layer, w)
        else:
          b_name = 'b%d' % idx
          b = tf.get_variable(b_name,
              [hidden_size], initializer=biases_initializer)
          self.var[b_name] = b
          layer = tf.nn.bias_add(tf.matmul(layer, w), b)

        if hidden_activation_fn and idx < len(hidden_sizes):
          layer = hidden_activation_fn(layer)
        elif output_activation_fn and idx == len(hidden_sizes):
          layer = output_activation_fn(layer)

      self.outputs = layer
