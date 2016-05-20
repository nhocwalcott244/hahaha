import cv2
import numpy
from matplotlib import pyplot
import os

__author__ = "Anh Do Nguyet"


class Image:

    def __init__(self):
        self.__file_path = None
        self.__blue_hist = None
        self.__green_hist = None
        self.__red_hist = None
        self.__category = '0'

    # đọc dữ liệu ảnh đầu vào, tính histogram, chuẩn hoá
    def read(self, file_path):
        self.__file_path = file_path
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)

        # lấy histogram của ảnh
        self.__blue_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        self.__green_hist = cv2.calcHist([img], [1], None, [256], [0, 256])
        self.__red_hist = cv2.calcHist([img], [2], None, [256], [0, 256])

    def get_file_path(self):
        return self.__file_path

    def get_category(self):
        return self.__category

    def set_category(self, cat):
        self.__category = cat

    def get_blue_histogram(self, bin_number=256):
        return self.__change_bin_histogram(self.__blue_hist, bin_number)

    def get_green_histogram(self, bin_number=256):
        return self.__change_bin_histogram(self.__green_hist, bin_number)

    def get_red_histogram(self, bin_number=256):
        return self.__change_bin_histogram(self.__red_hist, bin_number)

    def calc_distance(self, image, bin_number=256):
        assert 256 % bin_number == 0               # chỉ xét với số bin là ước của 256

        # blue histogram
        histogram_1 = self.get_blue_histogram(bin_number)
        histogram_2 = image.get_blue_histogram(bin_number)
        s = self.__calc_distance_2_histogram(histogram_1, histogram_2)

        # green histogram
        histogram_1 = self.get_green_histogram(bin_number)
        histogram_2 = image.get_green_histogram(bin_number)
        s += self.__calc_distance_2_histogram(histogram_1, histogram_2)

        # red histogram
        histogram_1 = self.get_red_histogram(bin_number)
        histogram_2 = image.get_red_histogram(bin_number)
        s += self.__calc_distance_2_histogram(histogram_1, histogram_2)

        # return sum of all histograms
        return s

    # hiển thị biểu đồ histogram lên pyplot
    def draw_histogram(self, bin_number=256):
        blue_hist = self.get_blue_histogram(bin_number)
        green_hist = self.get_green_histogram(bin_number)
        red_hist = self.get_red_histogram(bin_number)
        pyplot.figure()
        pyplot.title('Histogram of ' + os.path.basename(self.__file_path))
        pyplot.xlabel("Bins")
        pyplot.ylabel("So pixel da chuan hoa")
        pyplot.plot(blue_hist, color='blue')
        pyplot.plot(green_hist, color='green')
        pyplot.plot(red_hist, color='red')
        pyplot.xlim([0, bin_number])
        pyplot.show()

    # chuyển đổi histogram bin 256 sang các bin nhỏ hơn (là ước của 256)
    def __change_bin_histogram(self, histogram, bin_number):
        assert type(histogram) is numpy.ndarray
        assert histogram.shape[0] % bin_number == 0
        thuong = histogram.shape[0] / bin_number

        # tạo đối tượng lưu trữ histogram mới
        new_histogram = numpy.empty([bin_number, 1])
        for i in range(0, new_histogram.shape[0]):
            new_histogram[i][0] = 0

        # gán giá trị cho histogram mới
        for i in range(0, histogram.shape[0]):
            new_histogram[int(i / thuong)][0] += histogram[i][0]

        # chuẩn hoá histogram
        cv2.normalize(new_histogram, new_histogram, 0, 1, cv2.NORM_MINMAX)
        return new_histogram

    def __calc_distance_2_histogram(self, histogram_1, histogram_2):
        assert type(histogram_1) is numpy.ndarray   # chỉ xét với histogram có kiểu dữ liệu là ndarray
        assert type(histogram_2) is numpy.ndarray
        assert histogram_1.shape == histogram_2.shape   # chỉ xét với histogram có kích thước giống nhau
        s = 0
        for i in range(0, histogram_1.shape[0]):
            dt = abs(histogram_1[i][0] - histogram_2[i][0])
            s += dt
        return s
