from bottle import run, static_file, post, get, request, template, response
from ..utils import (base_path, read_ballot, verify_voter, create_ballot,
                     verify_vote, save_object)
from os.path import join
from json import dumps
import threading

response.content_type = 'application/json'

ballots = ['b1', 'b2', 'b3']
ballot_locks = {}

voters_lock = threading.Lock()
voters = {}

for b in ballots:
    create_ballot(b)
    save_object([], join(base_path, 'data/votes/', b))
    ballot_locks[b] = threading.Lock()
    voters[b] = []


@get('/public-key/<ballot_name>')
def download_public_key(ballot_name):
    return static_file(ballot_name,
                       root=join(base_path, 'data/public-keys'),
                       download=ballot_name)


@post('/sign-blind-msg/<ballot_name>')
def sign_message(ballot_name):
    try:
        data = request.json
        id, email, is_valid = verify_voter(data['token'])
        if email in voters[ballot_name]:
            return dumps({'code': 409, 'error': 'Already casted vote.'})
        if is_valid:
            with voters_lock:
                voters[ballot_name].append(email)
            A = read_ballot(ballot_name)
            return dumps({'code': 200, 'signed_msg': A.sign(data['msg'])})
        return dumps({'code': 400, 'error': 'Not a valid voter.'})
    except Exception as e:
        return dumps({'code': 500, 'error': str(e)})


@post('/dump-vote/<ballot_name>')
def dump_vote(ballot_name):
    try:
        data = request.json
        while ballot_locks[ballot_name]:
            path = join(base_path, 'data/votes/', ballot_name)
            prev_votes = open_object(path)
            if not verify_vote(data['vote'], prev_votes):
                return dumps({'code': 408, 'error': 'Invalid vote format.'})
            prev_votes.append(data['vote'])
            save_object(prev_votes, path)
        return dumps({'code': 200, 'msg': 'Successfully dumped vote.'})
    except Exception as e:
        return dumps({'code': 500, 'error': str(e)})


run(host='localhost', port=8080)
