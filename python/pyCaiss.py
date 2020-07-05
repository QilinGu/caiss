from ctypes import *

CAISS_MODE_DEFAULT = 0
CAISS_MODE_TRAIN = 1
CAISS_MODE_PROCESS = 2

CAISS_SEARCH_QUERY = 1
CAISS_SEARCH_WORD = 2
CAISS_LOOP_QUERY = 3
CAISS_LOOP_WORD = 4

CAISS_INSERT_OVERWRITE = 1
CAISS_INSERT_DISCARD = 2

CAISS_MANAGE_SYNC = 1
CAISS_MANAGE_ASYNC = 2

CAISS_DISTANCE_EUC = 1
CAISS_DISTANCE_INNER = 2
CAISS_DISTANCE_JACCARD = 3
CAISS_DISTANCE_EDITION = 99

CAISS_ALGO_HNSW = 1
CAISS_ALGO_NSG = 2


class PyCaiss:
    def __init__(self, path, max_thread_size, algo_type, manage_type):
        self._caiss = CDLL(path)
        self._caiss.CAISS_Environment(max_thread_size, algo_type, manage_type)


    def create_handle(self, handle):
        return self._caiss.CAISS_CreateHandle(pointer(handle))


    def init(self, handle, mode, distance_type, dim, model_path):
        path = create_string_buffer(model_path.encode(), len(model_path)+1)
        return self._caiss.CAISS_Init(handle, mode, distance_type, dim, path)


    def train(self, handle, data_path, max_data_size, normalize,
              max_index_size, precision, fast_rank, real_rank, step, max_epoch, show_span):
        return self._caiss.CAISS_Train(handle, data_path, max_data_size, normalize,
                                       max_index_size, precision, fast_rank, real_rank, step, max_epoch, show_span)


    def sync_search(self, handle, info, search_type, top_k, filter_edit_distance):
        word = create_string_buffer(info.encode(), len(info)+1)
        ret = self._caiss.CAISS_Search(handle, word, search_type, top_k, filter_edit_distance, None, None)
        if 0 != ret:
            return ''

        size = c_int(0)
        ret = self._caiss.CAISS_GetResultSize(handle, byref(size))
        if 0 != ret:
            return ''

        result = create_string_buffer(size.value)
        ret = self._caiss.CAISS_GetResult(handle, result, size)
        if 0 != ret:
            return ''

        return result.value.decode()


    def destroy(self, handle):
        self._caiss.CAISS_DestroyHandle(handle)