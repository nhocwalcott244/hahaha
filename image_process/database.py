import pickle

__author__ = "Cuong Nguyen Ngoc"


class Database:

    def __init__(self):
        self.__file_path = None

    # thiết lập đường dẫn tới file database
    def set_path(self, file_path):
        self.__file_path = file_path

    # lưu 1 object vào file database
    def save(self, item):
        with open(self.__file_path, 'wb') as f:
            pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

    # lưu danh sách object vào file database
    def saves(self, items):
        with open(self.__file_path, 'wb') as f:
            for item in items:
                pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

    # lấy ra 1 object từ file database
    def load(self):
        with open(self.__file_path, 'rb') as f:
            return pickle.load(f)

    # lấy ra danh sách object từ file database
    def loads(self):
        items = []
        with open(self.__file_path, "rb") as f:
            while True:
                try:
                    item = pickle.load(f)
                    items.append(item)
                except EOFError:
                    break
        return items

    # erase database
    def erase(self):
        open(self.__file_path, "w").close()
