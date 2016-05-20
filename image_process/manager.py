
import os
import imghdr
from .image import Image
from .database import Database


class Manager:

    def __init__(self):
        self.__database = Database()
        self.__images = []
        self.__distances = []
        self.__query_result = []
        self.__result_index = 0
        self.__query_image = None
        self.__bin_number = 256

    def load_image_folder(self, folder_path):
        self.__images = []
        for item in os.listdir(folder_path):
            file_path = os.path.join(folder_path, item)
            if imghdr.what(file_path) is not None:          # xác định xem file đầu vào có phải là file ảnh không
                image = Image()
                if len(item) < 7:
                    image.set_category('0')
                else:
                    image.set_category(item[0])
                image.read(file_path)
                self.__images.append(image)

    def set_database(self, path):
        self.__database.set_path(path)

    def save_database(self):
        self.__database.erase()
        self.__database.saves(self.__images)

    def load_database(self):
        self.__images = []
        self.__images = self.__database.loads()

    def query_image(self, file_path, bin_number=256, top_number=75):
        self.__bin_number = bin_number
        self.__query_result = []
        self.__result_index = 0
        if imghdr.what(file_path) is not None:          # xác định xem file đầu vào có phải là file ảnh không
            self.__query_image = Image()
            self.__query_image.read(file_path)
            self.__distances = []

            if len(self.__images) == 0:
                return 'Data is empty!'

            for img in self.__images:
                d = self.__query_image.calc_distance(img, bin_number)
                print(img.get_file_path(), ' - distance: ', d)
                self.__distances.append(d)

            # sắp xếp kết quả
            # cùng lúc sắp xếp 2 list __distances và images theo __distances
            combined = zip(self.__distances, self.__images)
            z = sorted(combined)
            self.__distances, self.__images = zip(*z)

            top_number = min(top_number, len(self.__images))
            for i in range(0, top_number):
                self.__query_result.append(self.__images[i])

            # i = 0
            # for d in self.__distances:
            #     print('khoang cach ', i, ': ', d, " - ", self.__images[i].get_file_path())
            #     i += 1

    def get_image(self):
        if len(self.__query_result) != 0:
            img = self.__query_result[self.__result_index]
            return img.get_file_path()

    def next_image(self):
        self.__result_index += 1
        if self.__result_index >= len(self.__query_result):
            self.__result_index = 0

    def back_image(self):
        self.__result_index -= 1
        if self.__result_index < 0:
            self.__result_index = len(self.__query_result)

    def draw_query_image_histogram(self, file_path, bin_number=256):
        if imghdr.what(file_path) is not None:
            self.__query_image = Image()
            self.__query_image.read(file_path)
            self.__query_image.draw_histogram(bin_number)

    def draw_result_image_histogram(self):
        if len(self.__query_result) != 0:
            img = self.__query_result[self.__result_index]
            img.draw_histogram(self.__bin_number)
