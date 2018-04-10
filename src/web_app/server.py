from bottle import run, static_file, post, get, request, template, response
from ..utils import (base_path, read_ballot, verify_voter, create_ballot,
                     verify_vote, save_object, log, open_object, read_votes)
from os.path import join
from json import dumps, loads
import threading
from ast import literal_eval

response.content_type = 'application/json'

ballots = ['b1', 'b2', 'b3']
ballot_locks = {}

voter_locks = {}
voters = {}


for b in ballots:
    create_ballot(b)
    save_object([], join(base_path, 'data/votes/', b))
    ballot_locks[b] = threading.Lock()
    voter_locks[b] = threading.Lock()
    voters[b] = []


@get('/public-key/<ballot_name>')
def download_public_key(ballot_name):
    log('info', 'Public key for {} requested.'.format(ballot_name))
    return static_file(ballot_name,
                       root=join(base_path, 'data/public-keys'),
                       download=ballot_name)


@get('/download-votes/<ballot_name>')
def download_votes(ballot_name):
    log('info', 'Votes of {} requested.'.format(ballot_name))
    return static_file(ballot_name,
                       root=join(base_path, 'data/votes'),
                       download=ballot_name)

@get('/votes/<ballot_name>')
def show_votes(ballot_name):
    return read_votes(ballot_name)


@post('/sign-blind-msg/<ballot_name>')
def sign_message(ballot_name):
    try:
        email = request.forms.get('email')
        password_hash = request.forms.get('password_hash')
        token = {
            'email': email,
            'password_hash': password_hash
        }
        msg = request.forms.get('msg')

        email, is_valid = verify_voter(token)

        if email in voters[ballot_name]:
            log('info', '{} tried to vote again.'.format(email))
            return dumps({'code': 409, 'error': 'Already casted vote.'})

        if is_valid:
            A = read_ballot(ballot_name)
            msg_signature = A.sign(msg)

            with voter_locks[ballot_name]:
                voters[ballot_name].append(email)

            log('info', '{} successfully taken a signed vote.'.format(email))
            return dumps({'code': 200, 'msg_signature': msg_signature})

        log('info', '{} is an invalid voter.'.format(email))
        return dumps({'code': 400, 'error': 'Not a valid voter.'})

    except Exception as e:
        log('exception sign', e)
        return dumps({'code': 500, 'error': e})


@post('/dump-vote/<ballot_name>')
def dump_vote(ballot_name):
    try:
        msg = literal_eval(request.forms.get('msg'))
        msg_signature = long(request.forms.get('msg_signature'))

        vote = {
            'msg': msg,
            'msg_signature': msg_signature
        }

        with ballot_locks[ballot_name]:
            path = join(base_path, 'data/votes/', ballot_name)
            prev_votes = open_object(path)

            if not verify_vote(vote, prev_votes, ballot_name):
                log('info', 'Invalid vote, vote: {}'.format(vote['msg']))
                return dumps({'code': 408, 'error': 'Invalid vote.'})

            prev_votes.append(vote)
            save_object(prev_votes, path)

        log('info', 'Vote dumped, Vote: {}'.format(vote['msg']))
        return dumps({'code': 200, 'msg': 'Successfully dumped vote.'})

    except Exception as e:
        log('exception dump', e)
        return dumps({'code': 500, 'error': e})


run(host='10.64.10.171', port=8080)
