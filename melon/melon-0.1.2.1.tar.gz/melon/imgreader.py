import sys
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from tqdm import tqdm

from melon.imgreader_denominations import Denominations as denom
from melon.label_format import LabelFormat
from melon.reader import Reader

try:
    from PIL import Image as pil_image

    logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
except ImportError:
    pil_image = None


class ImageReader(Reader):
    _default_data_format = "channels_first"
    _default_channels = 3
    _default_height = 255
    _default_width = 255
    _default_normalize = True
    _default_preserve_aspect_ratio = False
    _default_num_threads = 4
    _default_label_format = LabelFormat.one_hot

    _unsupported_file_formats = [".svg"]

    def __init__(self, source_dir, options=None):
        """
        :param source_dir: source directory of the image files
        :param options: reader options
        """
        self.__source_dir = source_dir
        self.__height = options.get(denom.height) if options and denom.height in options else self._default_height
        self.__width = options.get(denom.width) if options and denom.width in options else self._default_width
        self.__format = options.get(denom.data_format) if options and denom.data_format in options else self._default_data_format

        self.__label_format = LabelFormat[options.get(denom.label_format)] if options and denom.label_format in options \
            else self._default_label_format

        self.__normalize = options.get(denom.normalize) if options and denom.normalize in options else self._default_normalize
        self.__preserve_aspect_ratio = options.get(denom.preserve_aspect_ratio) if options and denom.preserve_aspect_ratio in options \
            else self._default_preserve_aspect_ratio
        self.__offset = 0
        self._log = logging.getLogger(__name__)

        try:
            self.__num_threads = options.get(denom.num_threads) if options and denom.num_threads in options else multiprocessing.cpu_count()
            self._log.info("Number of workers set to %s", self.__num_threads)
        except NotImplementedError:
            self.__num_threads = self._default_num_threads

        self.__labels, self.__classes, self.__files = self._read_meta()
        if options and denom.batch_size in options:
            self.__batch_size = min(options.get(denom.batch_size), len(self.__files))
        else:
            self.__batch_size = len(self.__files)

    def read(self):
        """
        Logic to read the images into the output format of "mxCxHxW or mxHxWxC"
        :param
        :return: tuple of 4-D array of "mxCxHxW or mxHxWxC" and labels
        """
        try:
            files = self.__files[self.__offset:self.__offset + self.__batch_size]
            m = len(files)

            y = np.empty(m, dtype=np.int32)
            if self.__format == "channels_first":
                x = np.ndarray(shape=(m, self._default_channels, self.__height, self.__width), dtype=np.float32)
            elif self.__format == "channels_last":
                x = np.ndarray(shape=(m, self.__height, self.__width, self._default_channels), dtype=np.float32)
            else:
                raise ValueError("Unknown data format %s" % self.__format)

            with tqdm(total=m, unit="file", desc="Total", leave=False) as pbar:
                with ThreadPoolExecutor(max_workers=self.__num_threads) as executor:
                    thread_batch_size = max(1, m // self.__num_threads)
                    remainder = m % self.__num_threads

                    futures = []
                    for i in range(0, m, thread_batch_size):
                        batch_start = i
                        is_final_batch = (i == m - remainder - thread_batch_size)
                        batch_end = i + thread_batch_size + (remainder if is_final_batch else 0)

                        future = executor.submit(self._worker, files[batch_start:batch_end], batch_start, x, y, pbar)
                        futures.append(future)
                        if is_final_batch:
                            break

                    for future in as_completed(futures):
                        try:
                            future_result = future.result()
                        except Exception  as e:
                            self._log.error("Failed to get future {}".format(str(e)))

                    if self.__label_format == LabelFormat.one_hot and self.__classes:
                        y = self._convert_to_one_hot(y)
            return x, y

        finally:
            self.__offset += self.__batch_size

    def has_next(self):
        return self.__offset < len(self.__files)

    def _validate_file(self, file):
        if file.suffix in self._unsupported_file_formats:
            self._log.warning("Unsupported file format %s", file.suffix)
            return False
        if file.name.startswith("labels") or file.name.startswith("."):
            return False
        return True

    def _read_meta(self):
        try:
            labels, classes = self._read_labels_and_classes()
        except Exception as e:
            raise ValueError("Failed to read labels. {}".format(str(e)))

        try:
            files = self._list_and_validate(self.__source_dir)
        except Exception as e:
            raise ValueError("Failed to read image files. {}".format(str(e)))

        return labels, classes, files

    def _read_labels_and_classes(self):
        """
        Reads labels file and returns mapping of file to label
        :param dir: source directory
        :return: tuple of 'dictionary of file to label mapping' and 'set of all distinct classes'
        """
        labels = {}
        classes = []

        labels_files = list(Path(self.__source_dir).glob("labels*"))
        if not labels_files:
            self._log.info("No labels file provided. Label vector will not be loaded.")
            return labels, classes

        max_class = - sys.maxsize
        file = labels_files[0]
        read_files = False
        with open(str(file)) as infile:
            for line in infile:
                line = line.strip()
                if not line: continue
                if line == "#map":
                    read_files = True
                    continue
                if read_files:
                    parts = line.split(":")
                    if len(parts) != 2:
                        self._log.warning("Skipping malformed line in labels file %s", line)
                        continue
                    label = parts[1].strip()
                    if label:
                        label = int(label)
                        labels[parts[0].strip()] = label
                        max_class = max(max_class, label)

        if max_class > 0:
            classes = list(range(max_class + 1))

        return labels, classes

    def _img_to_arr(self, img_file, dtype=np.float32):
        img = pil_image.open(img_file)
        with img:
            # if img.mode != 'RGB':
            #     img = img.convert('RGB')

            # if self.__preserve_aspect_ratio:
            #     wpercent = (self.__width / float(img.size[0]))
            #     self.__height = int((float(img.size[1]) * float(wpercent)))

            img = img.resize((self.__width, self.__height), pil_image.BICUBIC)
            arr = np.asarray(img, dtype=dtype)
            if len(arr.shape) == 3:
                # RGB
                if self.__format == 'channels_first':
                    arr = arr.transpose(2, 0, 1)
            elif len(arr.shape) == 2:
                # Greyscale
                if self.__format == 'channels_first':
                    arr = arr.reshape((1, arr.shape[0], arr.shape[1]))
                else:
                    arr = arr.reshape((arr.shape[0], arr.shape[1], 1))
            else:
                raise ValueError('Unsupported image shape: %s' % (arr.shape,))

            if self.__normalize:
                arr /= self.__width

        return arr

    def _convert_to_one_hot(self, y):
        return np.eye(len(self.__classes))[y]

    def _worker(self, batch, index, x, y, pbar):
        start = str(index)
        end = str(index + len(batch) - 1)

        for file in batch:
            label = self.__labels.get(file.name) if file.name in self.__labels else -1
            x[index] = self._img_to_arr(file)
            y[index] = label
            index += 1
            pbar.update(1)

        return "Processed thread batch [{},{}]".format(start, end)
