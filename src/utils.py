import pickle as pickle
from os.path import join
from hashlib import md5
import datetime

from server import log_lock
from resource import Authority


base_path = '/home/adithya/Prog/networking-project/src/'


def log(type, text):
    curr_log = '{} : [{}] {}'.format(datetime.datetime.now(),
                                     type.upper(), text)
    with log_lock:
        logs = open_object(join(base_path, 'data/log'))
        logs.append(curr_log)
        save_object(logs, join(base_path, 'data/log'))
    print curr_log


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


true_parties = {
    'b1': ['b1_p0', 'b1_p1', 'b1_p2', 'b1_p3'],
    'b2': ['b2_p0', 'b2_p1', 'b2_p2', 'b2_p3'],
    'b3': ['b3_p0', 'b3_p1', 'b3_p2', 'b3_p3']
}


def verify_vote(vote, prev_votes, ballot_name):

    try:
        bias_eq = filter(lambda x: x['msg']['bias'] ==
                         vote['msg']['bias'], prev_votes)

        if len(bias_eq) > 0:
            log('info', 'Vote clash, vote: {}, votes: {}'
                .format(str(vote['msg']),
                        str(map(lambda x: x['msg'], bias_eq))))
            return False

        if vote['msg']['party'] not in true_parties[ballot_name]:
            log('info', 'Invalid party, party: {}, valid_parties: {}'
                .format(str(vote['msg']['party']),
                        str(true_parties[ballot_name])))
            return False

        A = read_ballot(ballot_name)

        if not A.verify_msg(str(vote['msg']), vote['msg_signature']):
            log('info', 'Invalid signature, vote: {}'.format(str(vote['msg'])))
            return False

        log('info', 'Successful vote Auth, vote: {}'.format(str(vote['msg'])))
        return True
    except Exception as e:
        log('exception verify vote', e)
        return False


def read_votes(ballot_name):
    votes = open_object(join(base_path, 'data/votes/', ballot_name))
    vote_counts = {}

    for p in true_parties[ballot_name]:
        vote_counts[p] = 0

    for x in votes:
        vote_counts[x['msg']['party']] += 1

    return vote_counts
