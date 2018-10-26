import os
from threading import Thread


class LRU(Thread):
    """
    Watch the cache folder location out of sync
    Remove least used files when size exceed maximum set
    """
    __id = 0
    __maximum_length = 4
    __cache_folder_location = "./static/tmp/"

    def __init__(self):
        """
        __cache_dict = { id, filename }
        """
        Thread.__init__(self)
        # reading current cache folder
        # creating cache_arr
        self.__cache_dict = {}
        self.__update_cache_arr()

    @staticmethod
    def __next_id():
        LRU.__id += 1
        return LRU.__id

    def __update_cache_arr(self):
        """
        watch the cache folder and update __cache_dict according to it
        """
        cache_content = os.listdir(LRU.__cache_folder_location)

        current_files = self.__cache_dict.values()

        for filename in cache_content:
            if filename not in current_files:
                self.__cache_dict[LRU.__next_id()] = filename
            else:
                list(current_files).remove(filename)


    def __remove_least_recent_file(self):
        """
        remove least used file
        """
        # print(self.__cache_dict.keys())
        file_to_remove = self.__cache_dict[min(self.__cache_dict.keys())]

        self.__cache_dict.pop(min(self.__cache_dict.keys()))
        try:
            os.remove(LRU.__cache_folder_location + file_to_remove)
            print("removed", file_to_remove, "from cache")
        except FileExistsError:
            pass

    def run(self):
        while True:
            self.__update_cache_arr()
            while len(self.__cache_dict) > LRU.__maximum_length:
                self.__remove_least_recent_file()
