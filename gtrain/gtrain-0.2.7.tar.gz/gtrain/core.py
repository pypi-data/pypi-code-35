import tensorflow as tf
import os
import time
import datetime

from gtrain.data import Data
from gtrain.model import Model

"""
Prototypes of model and data classes:

class Model:
    def __init__(self,args):
        # stores settings of the model

    def build(self):
        # builds whole model in tensorflow
        # stores placeholders, loss and accuracy

        
    def get_loss(self):
        return self.loss
    
    def get_accuracy(self):
        return self.accuracy

    def get_train_summaries(self):
        return []
        # training sumaries of the model should be added here

    def get_dev_summaries(self):
        return []
        # dev sumaries of the model should be added here

    def get_placeholders(self):
        # returns list of placeholders

    def name(self):
        # returns specific name of the model for the initial parameters

class Data:
    def __init__(self, args):
        # stores sources or raw data
        # both, training and validation data have to avaliable
        
    def set_placeholders(self,pl_list):
        # pl_list is a list of placeholders getted from procedure get_placeholders of Model class
        # stores placehoders that are used in feed dictionary for the model

    def get_next_batch(self):
        # returns feed dictionary of one batch of training data
    
    def accumulate_grad(self):
        # returns True if the previous gen_next_batch data should be used just for accumulation gradients
        # returns False if the model shoudl be learned with previously accumulated gradients 

    def get_next_dev_batch(self):
        # returns feed dictionary of one batch of dev data
    
    def train_ended(self):
        # this procedure is started when the training is ended
"""
def gtrain(
    model,
    data,
    optimizer=tf.train.AdamOptimizer(),
    max_fails=5,
    num_steps=100,
    evaluate_every=10,
    checkpoint_every=10,
    num_checkpoints=5,
    out_dir=None,
    varbose_level=1,
    additional_summaries=True,
    dtype=tf.float32):
    """
gtrain implements general purpouse training algorithm
    gtrain implements general purpouse training algorithm
    :param model: Model object defining model that should be trained
    :param data: Data object defining data and their batches used in training algorithm
    :param optimizer: tf optimizer class to be used else is used
    :param max_fails:
    :param num_steps: Data object defining data and their batches used in training algorithm
    :param evaluate_every: if the index of the training step is divisible by evaluate_every then in this point the network is evaluated on dev data
    :param checkpoint_every: if the index of the training step is divisible by checkpoint_every then the models with parameters is saved
    :param num_checkpoints: how deep history of checkpoints is avaliable at the end of training
    :param out_dir: output directory where checkpoints and summaries are stored
    :param varbose_level:
    :param additional_summaries:
    :return:
    """

    if not issubclass(type(model), Model):
        print("ERROR: model argumetn in gtrain function must be of the gtrain.model.Model class.")
    if not issubclass(type(data), Data):
        print("ERROR: model argumetn in gtrain function must be of the gtrain.data.Data class.")

    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():

            # further cnn is a model

            with tf.name_scope("Model"):
                model.build()
            data.set_placeholders(model.get_placeholders())

            # Define Training procedure
            global_step = tf.Variable(0, name="global_step", trainable=False, dtype=dtype)

            # Accumulative
            with tf.name_scope("Accumulate"):
                tvs = tf.trainable_variables()
                accum_vars = [tf.Variable(tf.zeros_like(tv.initialized_value()), trainable=False, dtype=dtype) for tv in tvs]
                accum_loss = tf.Variable(0.0, trainable=False, dtype=dtype)
                accum_hits = tf.Variable(0.0, trainable=False, dtype=dtype)
                accum_count = tf.Variable(0.0, trainable=False, dtype=dtype)
                zero_ops = [tv.assign(tf.zeros_like(tv)) for tv in accum_vars] + [accum_loss.assign(0.0), accum_hits.assign(0.0), accum_count.assign(0.0)]
                zero_dev_ops = [accum_loss.assign(0.0), accum_hits.assign(0.0), accum_count.assign(0.0)]
                gvs = optimizer.compute_gradients(model.get_loss(), tvs)
                accum_ops = [accum_vars[i].assign_add(gv[0]) for i, gv in enumerate(gvs)] + [
                    accum_loss.assign_add(model.get_loss()),
                    accum_hits.assign_add(model.get_hits()),
                    accum_count.assign_add(model.get_count()),
                ]
                accum_dev_ops = [accum_loss.assign_add(model.get_loss()), accum_hits.assign_add(model.get_hits()), accum_count.assign_add(model.get_count())]
                train_op = optimizer.apply_gradients([(accum_vars[i], gv[1]) for i, gv in enumerate(gvs)], global_step=global_step)
            sess.run(zero_ops)

            loss_summary = tf.summary.scalar("loss", accum_loss)
            acc_summary = tf.summary.scalar("accuracy", accum_hits / accum_count)
            summaries_list = [loss_summary, acc_summary, model.get_train_summaries()]

            if out_dir:
                with tf.name_scope("Summaries"):
                    # Summaries for loss and accuracy
                    if additional_summaries:
                        # Keep track of gradient values and sparsity
                        grad_summaries = list()
                        for g, v in gvs:
                            if g is not None:
                                grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
                                sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                                grad_summaries.append(grad_hist_summary)
                                grad_summaries.append(sparsity_summary)
                        summaries_list.append(tf.summary.merge(grad_summaries))

                        # Keep track of trainable variable values
                        value_summaries = list()
                        for v in tf.trainable_variables():
                            value_summary = tf.summary.histogram("{}/value/hist".format(v.name), v)
                            value_sparse_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(v))
                            value_summaries.append(value_summary)
                            value_summaries.append(value_sparse_summary)
                        summaries_list.append(tf.summary.merge(value_summaries))

                # Train Summaries
                train_summary_op = tf.summary.merge(summaries_list)
                train_summary_dir = os.path.join(out_dir, "summaries", "train")
                train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

                # Dev summaries
                dev_summary_op = tf.summary.merge([
                    loss_summary,
                    acc_summary,
                    model.get_dev_summaries()])
                dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
                dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

                # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
                checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
                checkpoint_prefix = os.path.join(checkpoint_dir, model.name())
                if not os.path.exists(checkpoint_dir):
                    os.makedirs(checkpoint_dir)
                saver = tf.train.Saver(tf.global_variables(), max_to_keep=num_checkpoints)
            else:
                dev_summary_writer = None
                train_summary_op = model.get_loss()
                dev_summary_op = model.get_loss()
            # Initialize all variables
            sess.run(tf.global_variables_initializer())
            prev_loss = 1e10
            fails = 0
            loss = prev_loss

            def train_step():
                # acumulate gradients and
                sum_size = 0
                while True:
                    feed_dict = data.get_next_batch()
                    sess.run(accum_ops, feed_dict)
                    if not data.accumulate_grad():
                        break

                _, step, summaries, loss,  hits, count = sess.run(
                    [train_op,  global_step, train_summary_op, accum_loss, accum_hits, accum_count], feed_dict)
                sess.run(zero_ops)
                time_str = datetime.datetime.now().isoformat()
                if varbose_level > 1:
                    print("[train] {}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, hits/count))

                if out_dir:
                    train_summary_writer.add_summary(summaries, step)


            def dev_step(writer=None):
                while True:
                    feed_dict = data.get_next_dev_batch()
                    sess.run(accum_dev_ops, feed_dict)
                    if not data.accumulate_dev():
                        break
                # Evaluates model on a dev set
                step, summaries, loss, hits, count = sess.run(
                    [global_step, dev_summary_op, accum_loss, accum_hits, accum_count], feed_dict)
                sess.run(zero_dev_ops)
                time_str = datetime.datetime.now().isoformat()
                if varbose_level > 0:
                    print("[validation] {}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, hits/count))
                if writer and out_dir:
                    writer.add_summary(summaries, step)
                return loss

            # Training loop
            current_step = tf.train.global_step(sess, global_step)
            for i in range(1, num_steps+1):
                train_step()
                if i % evaluate_every == 0:
                    if varbose_level > 0:
                        print("\nEvaluation:")
                    prev_loss = loss
                    loss = dev_step(writer=dev_summary_writer)
                    if prev_loss < loss:
                        fails += 1
                        if fails == max_fails:
                            break
                if i % checkpoint_every == 0:
                    if out_dir:
                        path = saver.save(sess, checkpoint_prefix, global_step=i)
                        if varbose_level > 0:
                            print("Saved model checkpoint to {}\n".format(path))
            data.train_ended()
            model.train_ended(sess)
            if out_dir:
                path = saver.save(sess, checkpoint_prefix, global_step=i)
                if varbose_level > 0:
                    print("Saved model checkpoint to {}\n".format(path))
                dev_summary_writer.close()
                train_summary_writer.close()


def strain(model, data, optimizer=tf.train.AdamOptimizer(), num_steps=100, session=None):
    """
    Build model and conduct pure loop with optimizer at the end the train_ended method is called on model
    :param model:
    :param data:
    :param num_steps: number of steps
    :param session: if it is not provided the new is created and returned
    :return: session
    """
    if session is None:
        session = tf.Session()
        with session.as_default():
            model.build()
            session.run(tf.global_variables_initializer())

    data.set_placeholders(model.get_placeholders())
    train_op = optimizer.minimize(model.get_loss())
    session.run(tf.variables_initializer(optimizer.variables()))
    for i in range(num_steps):
        train_op.run(data.get_next_batch(), session=session)
    model.train_ended(session)
    return session

