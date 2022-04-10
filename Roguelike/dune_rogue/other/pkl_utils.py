import pickle


def load_pkl(target_path):
    """ Loads pickle file
    :argument target_path: path to be loaded from
    :return: loaded object
    """
    with open(target_path, 'rb') as handle:
        return pickle.load(handle)


def save_pkl(target_path, data):
    """ Saves object to pickle
    :argument target_path: path to save
    :argument data: object to save
    """
    with open(target_path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
