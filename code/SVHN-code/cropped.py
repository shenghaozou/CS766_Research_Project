import tensorflow as tf
import os
import numpy as np
import matplotlib.image as mpimg
import h5py
from PIL import Image

class ExampleReader(object):
    def __init__(self, path_to_image_files):
        self._path_to_image_files = path_to_image_files
        self._num_examples = len(self._path_to_image_files)
        self._example_pointer = 0

    @staticmethod
    def _get_attrs(digit_struct_mat_file, index):
        """
        Returns a dictionary which contrains keys: label, left, top, width and height, each key has multiple
        values.

        :param digit_struct_mat_file:
        :param index:
        :return:
        """
        attrs = {}
        f = digit_struct_mat_file
        item = f['digitStruct']['bbox'][index].item()
        for key in ['label', 'left', 'top', 'width', 'height']:
            attr = f[item][key]
            values = [f[attr.value[i].item()].value[0][0] for i in range(len(attr))] \
                if len(attr) > 1 else [attr.value[0][0]]
            attrs[key] = values
        return attrs

    @staticmethod
    def _preprocess(image, bbox_left, bbox_top, bbox_width, bbox_height):
        cropped_left, cropped_top, cropped_width, cropped_height = (int(round(bbox_left - 0.15 * bbox_width)),
                                                                    int(round(bbox_top - 0.15 * bbox_height)),
                                                                    int(round(bbox_width * 1.3)),
                                                                    int(round(bbox_height * 1.3)))
        image = image.crop([cropped_left, cropped_top, cropped_left + cropped_width, cropped_top + cropped_height])
        image = image.resize([64, 64])
        return image

    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    @staticmethod
    def _float_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def read_and_convert(self, digit_struct_mat_file):
        """
        Read and convert to example, returns None if no data is available

        :param digit_struct_mat_file:
        :return:
        """
        if self._example_pointer == self._num_examples:
            return None
        path_to_image_file = self._path_to_image_files[self._example_pointer]
        index = int(path_to_image_file.split('/')[-1].split('.')[0]) - 1
        self._example_pointer += 1

        attrs = ExampleReader._get_attrs(digit_struct_mat_file, index)
        label_of_digits = attrs['label']
        length = len(label_of_digits)
        if length > 5:
            # skip this example
            return self.read_and_convert(digit_struct_mat_file)

        attrs_left, attrs_top, attrs_width, attrs_height = map(lambda x: [int(i) for i in x],
                                                               [attrs['left'], attrs['top'], attrs['width'],
                                                                attrs['height']])
        min_left, min_top, max_right, max_bottom = (min(attrs_left),
                                                    min(attrs_top),
                                                    max(map(lambda x, y: x + y, attrs_left, attrs_width)),
                                                    max(map(lambda x, y: x + y, attrs_top, attrs_height)))
        center_x, center_y, max_side = ((min_left + max_right) / 2.0,
                                        (min_top + max_bottom) / 2.0,
                                        max(max_right - min_left, max_bottom - min_top))
        bbox_left, bbox_top, bbox_width, bbox_height = (center_x - max_side / 2.0,
                                                        center_y - max_side / 2.0,
                                                        max_side,
                                                        max_side)
        image = np.array(ExampleReader._preprocess(Image.open(path_to_image_file), bbox_left, bbox_top, bbox_width,
                                                   bbox_height))
        return index, image

data_dir = 'data'
path_to_test_dir = os.path.join(data_dir, 'test')
path_to_save_dir = os.path.join(data_dir, 'cropped')

path_to_test_digit_struct_mat_file = os.path.join(path_to_test_dir, 'digitStruct.mat')
path_to_image_files = tf.gfile.Glob(os.path.join(path_to_test_dir, '*.png'))
total_files = len(path_to_image_files)
print('%d files found in %s' % (total_files, path_to_test_dir))

with h5py.File(path_to_test_digit_struct_mat_file, 'r') as digit_struct_mat_file:
    example_reader = ExampleReader(path_to_image_files)
    for index, path_to_image_file in enumerate(path_to_image_files):
        print('%d/%d processing %s' % (index + 1, total_files, path_to_image_file))

        i, image = example_reader.read_and_convert(digit_struct_mat_file)
        image = image.astype(dtype=np.int32)
        if image is None:
            break
        
        mpimg.imsave(os.path.join(path_to_save_dir, str(i + 1) + '.png'), image)
