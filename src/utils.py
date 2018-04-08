import cPickle as pickle
from resource import *
from os.path import join

def save_object(obj, file_path):
	with open(file_path, 'wb') as file:
		pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


def create_ballot(ballot_name):
	A = Authority()
	save_object(A.priv_key, join('./keys/private', ballot_name))
	save_object(A.pub_key, join('./keys/pub_key', ballot_name))
	return A.priv_key, A.pub_key

















