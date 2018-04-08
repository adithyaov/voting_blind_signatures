from bottle import route, run, template
from ...utils import create_ballot

ballots = ['b1', 'b2', 'b3']
for b in ballots:
	create_ballot(b)

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)


