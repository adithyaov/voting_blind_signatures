import pickle as pickle
from resource import Authority
from os.path import join
from hashlib import sha512, sha256, md5
import datetime


base_path = '/home/adithya/Prog/networking-project/src/'

def log(type, text):
	print '{} : [{}] {}'.format(datetime.datetime.now(), type.upper(), text)

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
	test_users = {
		'email1': md5('password1').hexdigest(),
		'email2': md5('password2').hexdigest(),
		'email3': md5('password3').hexdigest(),
		'email4': md5('password4').hexdigest()
	}
	try:
		if test_users[token['email']] == token['password_hash']:
			log('info', 'Successful user Auth.')
			return token['email'], True
		log('info', 'Failed user Auth.')
		return token['email'], False
	except Exception as e:
		log('exception verify voter', e)
		return 0, False



def verify_vote(vote, prev_votes, ballot_name):
	participants_in_ballot = {
		'b1': ['b1_p0', 'b1_p1', 'b1_p2', 'b1_p3'],
		'b2': ['b2_p0', 'b2_p1', 'b2_p2', 'b2_p3'],
		'b3': ['b3_p0', 'b3_p1', 'b3_p2', 'b3_p3']
	}
	try:
		timestamp_eq = filter(lambda x: x['msg']['timestamp'] == vote['msg']['timestamp'], prev_votes)
		if len(timestamp_eq) > 0:
			log('info', 'Vote clash, vote: {}, votes: {}'.format(str(vote), str(timestamp_eq)))
			return False
		if vote['msg']['participant'] not in participants_in_ballot[ballot_name]:
			log('info', 'Invalid participant, participant: {}, valid_participants: {}'
				.format(str(vote['participant']), str(participants_in_ballot[ballot_name])))
			return False

		A = read_ballot(ballot_name)
		print '---------------------------',A.verify_msg(str(vote['msg']), vote['msg_signature'])
		if not A.verify_msg(str(vote['msg']), vote['msg_signature']):
			log('info', 'Invalid signature, vote: {}'.format(str(vote)))
			return False

		log('info', 'Successful vote Auth, vote: {}'.format(str(vote)))
		return True
	except Exception as e:
		log('exception verify vote', e)
		return 0, False

