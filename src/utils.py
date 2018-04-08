import cPickle as pickle
from resource import Authority
from os.path import join

base_path = '/home/adithya/Prog/networking-project/src/'

def save_object(obj, file_path):
	with open(file_path, 'wb') as file:
		pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)

def open_object(file_path):
	with open(file_path, 'rb') as file:
		return pickle.load(file)


def create_ballot(ballot_name):
	A = Authority()
	save_object(A, join(base_path, 'data/authority-objects/', ballot_name))
	save_object(A.pub_key, join(base_path, 'data/public-keys/', ballot_name))
	return A.priv_key, A.pub_key


def read_ballot(ballot_name):
	return open_object(join(base_path, 'data/authority-objects/', ballot_name))

def verify_voter(token):
	return 0, 0, False


def verify_vote(vote, prev_votes):
	'''
	{
		'vote': ...
		'signature': ...
	}
	'''
	return True



