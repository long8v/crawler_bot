import pickle

def pickle_open(file_name):
    with open('{}.p'.format(file_name), 'rb') as f:
        return pickle.load(f)
        
def pickle_save(file_name, obj_name):
    with open('{}.p'.format(file_name), 'wb') as f:
        pickle.dump(obj_name, f)