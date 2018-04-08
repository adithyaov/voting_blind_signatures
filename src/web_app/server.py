from bottle import run, static_file, post, get, request, template, response
from ..utils import base_path, read_ballot, verify_voter
from os.path import join
from json import dumps

response.content_type = 'application/json'

create_ballots(['b1', 'b2', 'b3'])

@get('/public-key/<ballot_name>')
def download_public_key(ballot_name):
    return static_file(ballot_name, root=join(base_path, 'data/public-keys'), download=ballot_name)

@post('/sign-blind-msg/<ballot_name>')
def sign_message(ballot_name):
	try:
		data = request.json
		if verify_voter(data['token']):
			A = read_ballot(ballot_name)
			return dumps({'code': 200, 'signed_msg': A.sign(data['msg'])})
		return dumps({'code': 400, 'error': 'Not a valid voter.'})
	except:
		return dumps({'code': 500, 'error': 'Improper data format.'})


run(host='localhost', port=8080)


