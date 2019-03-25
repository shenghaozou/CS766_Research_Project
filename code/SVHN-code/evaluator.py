import tensorflow as tf
import sys

sys.path.append('.')
from donkey import Donkey
from model import Model
import numpy as np

class Evaluator(object):
    def __init__(self, path_to_eval_log_dir):
        self.summary_writer = tf.summary.FileWriter(path_to_eval_log_dir)

    def evaluate(self, path_to_checkpoint, path_to_tfrecords_file, num_examples, global_step):
        batch_size = 128

        num_batches = num_examples // batch_size
        needs_include_length = False

        with tf.Graph().as_default():
            id_batch, image_batch, length_batch, digits_batch = Donkey.build_batch(path_to_tfrecords_file,
                                                                         num_example=num_examples,
                                                                         batch_size=batch_size,
                                                                         shuffled=False)
            print(batch_size)
            length_logits, digits_logits = Model.inference(image_batch, drop_rate=0.0)
            length_predictions = tf.argmax(length_logits, axis=1)
            digits_predictions = tf.argmax(digits_logits, axis=2)

            if needs_include_length:
                labels = tf.concat([tf.reshape(length_batch, [-1, 1]), digits_batch], axis=1)
                predictions = tf.concat([tf.reshape(length_predictions, [-1, 1]), digits_predictions], axis=1)
            else:
                labels = digits_batch
                predictions = digits_predictions

            labels_string = tf.reduce_join(tf.as_string(labels), axis=1)
            predictions_string = tf.reduce_join(tf.as_string(predictions), axis=1)

            accuracy, update_accuracy = tf.metrics.accuracy(
                labels=labels_string,
                predictions=predictions_string)

            tf.summary.image('image', image_batch)
            tf.summary.scalar('accuracy', accuracy)
            tf.summary.histogram('variables',
                                 tf.concat([tf.reshape(var, [-1]) for var in tf.trainable_variables()], axis=0))
            summary = tf.summary.merge_all()

            ids_total = []
            labels_total = []
            predictions_total = []
            with tf.Session() as sess:
                sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
                coord = tf.train.Coordinator()
                threads = tf.train.start_queue_runners(sess=sess, coord=coord)

                restorer = tf.train.Saver()
                restorer.restore(sess, path_to_checkpoint)

                for k in range(num_batches):
                    sess.run(update_accuracy)

                    ids, labels, predictions = sess.run([id_batch, labels_string, predictions_string])
                    accuracy_val, summary_val = sess.run([accuracy, summary])
                    self.summary_writer.add_summary(summary_val, global_step=global_step)

                    ids_total.extend(ids)
                    labels_total.extend(labels)
                    predictions_total.extend(predictions)

                coord.request_stop()
                coord.join(threads)

            ids_total = np.array(ids_total)
            labels_total = np.array(labels_total)
            predictions_total = np.array(predictions_total)
            print(ids_total.shape, labels_total.shape, predictions_total.shape)
            with open('result.txt', 'w') as f:
                f.write('ID\tprediction\tlabel\n')
                for i in range(len(labels_total)):
                    f.write(str(ids_total[i])+'\t'+str(predictions_total[i])+'\t'+str(labels_total[i])+'\n')

        return accuracy_val
