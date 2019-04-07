import tensorflow as tf
from abc import ABC


class Model(ABC):
    def build(self):
        pass

    def get_loss(self):
        pass

    def get_hits(self):
        pass

    def get_count(self):
        pass

    def get_train_summaries(self):
        pass

    def get_dev_summaries(self):
        pass

    def get_placeholders(self):
        pass

    def train_ended(self, session):
        pass

    def name(self):
        pass



class FCNet(Model):
    #example of child of Model class
    def __init__(self, layer_sizes, activation_function=tf.nn.sigmoid, useCrossEbtropy=True):
        self.input_size = layer_sizes[0]
        self.num_classes = layer_sizes[-1]
        self.layer_sizes = layer_sizes
        self.cross_entropy = useCrossEbtropy
        self.activation_function=activation_function

    def build(self):
        with tf.name_scope("Input"):
            self.x = tf.placeholder(tf.float32,shape=[None, self.input_size], name="Input...")
        with tf.name_scope("Target"):
            self.t = tf.placeholder(tf.float32,shape=[None, self.num_classes], name="Target_output")
            tc = tf.argmax(self.t,1,name="Target_classes")
        with tf.name_scope("FC_net"):
            flowing_x = self.x
            self.W = list()
            self.b = list()
            ls = self.layer_sizes
            for i in range(len(ls)-1):
                with tf.name_scope("layer_{}".format(i)):
                    W = tf.get_variable(shape=[ls[i], ls[i+1]], name="Weights_{}".format(i), initializer=tf.contrib.layers.xavier_initializer())
                    b = tf.get_variable(shape= [ ls[i+1]], name="Biases_{}".format(i), initializer=tf.contrib.layers.xavier_initializer())
                    self.W.append(W)
                    self.b.append(b)
                    flowing_x = self.activation_function(tf.nn.xw_plus_b(flowing_x, W, b))

            y = flowing_x

            with tf.name_scope("Output"):
                self.out = tf.nn.softmax(y)
            with tf.name_scope("Loss"):
                if self.cross_entropy:
                    self.loss = tf.reduce_mean(
                        tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=self.t))
                else:
                    self.loss = tf.reduce_mean(
                        tf.nn.l2_loss(self.out-self.t))
            with tf.name_scope("Accuracy"):
                hits_list = tf.cast(tf.equal(tf.argmax(y, 1), tc), tf.float32)
                self.hits = tf.reduce_sum(hits_list)
                self.count = tf.cast(tf.size(hits_list), tf.float32)
        
    def get_loss(self):
        return self.loss

    def get_out(self):
        return self.out
    
    def get_hits(self):
        return self.hits

    def get_count(self):
        return self.count

    def get_train_summaries(self):
        return []

    def get_dev_summaries(self):
        return []

    def get_placeholders(self):
        return self.x, self.t

    def name(self):
        return "FC_net_{}".format("-".join([str(ls) for ls in self.layer_sizes]))

    def train_ended(self, session):
        self.trained_W = session.run(self.W)
        self.trained_b = session.run(self.b)

