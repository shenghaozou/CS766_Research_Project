import tensorflow as tf
from model import Model
import matplotlib.pyplot as plt
from PIL import Image
import os

tf.app.flags.DEFINE_string('image', None, 'Path to image file')
tf.app.flags.DEFINE_string('img_dir', None, 'Path to image dir')
tf.app.flags.DEFINE_string('restore_checkpoints', None,
                           'Path to restore checkpoint (with out postfix), e.g. ./logs/train/model.ckpt-100')
tf.app.flags.DEFINE_string('output_file', None, 'result file')
FLAGS = tf.app.flags.FLAGS


def main(_):
    #path_to_image_file = FLAGS.image
    #path_to_restore_checkpoints = FLAGS.restore_checkpoints
    output_file = FLAGS.output_file
    path_to_image_dir = FLAGS.img_dir
    path_to_restore_checkpoints = 'Models/SVHN/tensorflow_model/model.ckpt-328000'
    
    model = Model()
    images = tf.placeholder(dtype=tf.float32, shape=[1, 54, 54, 3])
    length_logits, digits_logits = model.inference(images, drop_rate=0.0)
    length_predictions = tf.argmax(length_logits, axis=1)
    digits_predictions = tf.argmax(digits_logits, axis=2)
    digits_predictions_string = tf.reduce_join(tf.as_string(digits_predictions), axis=1)
    sess = tf.Session()
    restorer = tf.train.Saver()
    restorer.restore(sess, path_to_restore_checkpoints)

    f = open(output_file, 'w')
    for i in range(1, 13068 + 1):
        path_to_image_file = os.path.join(path_to_image_dir, '{}.png'.format(i))
        image = tf.image.decode_jpeg(tf.read_file(path_to_image_file), channels=3)
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        image = tf.multiply(tf.subtract(image, 0.5), 2)
        image = tf.reshape(image, [64, 64, 3])
        # image = tf.image.resize_images(image, [64, 64])
        # image = tf.reshape(image, [64, 64, 3])
        # image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        # image = tf.multiply(tf.subtract(image, 0.5), 2)
        image = tf.image.resize_images(image, [54, 54])
        imgs = sess.run(tf.reshape(image, [1, 54, 54, 3]))
	
        length_predictions_val, digits_predictions_string_val, digits_predictions_val = sess.run(
            [length_predictions, digits_predictions_string, digits_predictions], feed_dict = {images: imgs})
        title = 'length: %d\ndigits= %d, %d, %d, %d, %d' % (length_predictions_val[0],
                                                            digits_predictions_val[0][0],
                                                            digits_predictions_val[0][1],
                                                            digits_predictions_val[0][2],
                                                            digits_predictions_val[0][3],
                                                            digits_predictions_val[0][4])

        print('%d %s' % (length_predictions_val[0], digits_predictions_string_val[0]), file=f, flush = True)

    f.close()

if __name__ == '__main__':
    tf.app.run(main=main)
