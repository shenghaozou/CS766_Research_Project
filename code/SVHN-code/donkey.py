import tensorflow as tf


class Donkey(object):

    @staticmethod
    def _preprocess(image):
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        image = tf.multiply(tf.subtract(image, 0.5), 2)
        image = tf.reshape(image, [64, 64, 3])
        image = tf.random_crop(image, [54, 54, 3])
        return image

    @staticmethod
    def _read_and_decode(filename_queue):
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features={
                'id': tf.FixedLenFeature([], tf.int64),
                'image': tf.FixedLenFeature([], tf.string),
                'length': tf.FixedLenFeature([], tf.int64),
                'digits': tf.FixedLenFeature([5], tf.int64)
            })
        id = tf.cast(features['id'], tf.int32)
        image = Donkey._preprocess(tf.decode_raw(features['image'], tf.uint8))
        length = tf.cast(features['length'], tf.int32)
        digits = tf.cast(features['digits'], tf.int32)
        return id, image, length, digits

    @staticmethod
    def build_batch(path_to_tfrecord_file, num_example, batch_size, shuffled):
        assert tf.gfile.Exists(path_to_tfrecord_file), "%s not found" % path_to_tfrecord_file

        filename_queue = tf.train.string_input_producer([path_to_tfrecord_file], num_epochs=None)
        id, image, length, digits = Donkey._read_and_decode(filename_queue)

        min_queue_examples = int(0.4 * num_example)
        if shuffled:
            id_batch, image_batch, length_batch, digits_batch = tf.train.shuffle_batch([id, image, length, digits],
                                                                             batch_size=batch_size,
                                                                             num_threads=2,
                                                                             capacity=min_queue_examples + 3 * batch_size,
                                                                             min_after_dequeue=min_queue_examples)
        else:
            id_batch, image_batch, length_batch, digits_batch = tf.train.batch([id, image, length, digits],
                                                                     batch_size=batch_size,
                                                                     num_threads=2,
                                                                     capacity=min_queue_examples + 3 * batch_size)


        return id_batch, image_batch, length_batch, digits_batch
