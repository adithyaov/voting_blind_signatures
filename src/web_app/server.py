from bottle import run, static_file, post, get, request, template, response
from ..utils import base_path, read_ballot, verify_voter
from os.path import join
from json import dumps
import threading

response.content_type = 'application/json'

ballots = ['b1', 'b2', 'b3']

create_ballots(ballots)

votings_lock = threading.Lock()
votings = {}

for b in ballots:
	votings[b] = []


@get('/public-key/<ballot_name>')
def download_public_key(ballot_name):
    return static_file(ballot_name, root=join(base_path, 'data/public-keys'), download=ballot_name)

@post('/sign-blind-msg/<ballot_name>')
def sign_message(ballot_name):
	try:
		data = request.json
		id, email, is_valid = verify_voter(data['token'])
		if email in votings[ballot_name]:
			return dumps({'code': 409, 'error': 'Already casted vote.'})
		if is_valid:
			with votings_lock:
				votings[ballot_name].append(email)
			A = read_ballot(ballot_name)
			return dumps({'code': 200, 'signed_msg': A.sign(data['msg'])})
		return dumps({'code': 400, 'error': 'Not a valid voter.'})
	except:
		return dumps({'code': 500, 'error': 'Improper data format.'})


run(host='localhost', port=8080)


