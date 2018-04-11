import datetime
from utils import *
from requests import *
from hashlib import md5
from resource import Blinder
import json
import random

B = None


def get_sign(email, password, party, ballot_name):

    global B

    public_key = open_object(join(base_path, 'data/public-keys/', ballot_name))
    B = Blinder(public_key)

    message = {
        'party': party,
        'bias': md5(str(datetime.datetime.now()) +
                    str(random.random())).hexdigest()
    }

    B.update_random()
    blind_msg = B.blind_msg(str(message))

    r = post('http://10.64.10.171:8080/sign-blind-msg/{}'.format(ballot_name),
             data={
                 'email': email,
                 'password_hash': md5(password).hexdigest(),
                 'msg': blind_msg
    })

    return message, r.json()


def dump_vote(message, msg_signature, ballot_name):
    r = post('http://10.64.10.171:8080/dump-vote/{}'.format(ballot_name),
             data={
                 'msg': str(message),
                 'msg_signature': msg_signature
    })
    return r.json()


def show_votes(ballot_name):
    r = get('http://10.64.10.171:8080/votes/{}'.format(ballot_name))
    return r.json()


def sign_and_dump(email, password, party, ballot_name):

    global B

    m, r = get_sign(email, password, party, ballot_name)

    if r['code'] == 200:
        r = dump_vote(m, B.unblind_msg(r['msg_signature'][0]), ballot_name)
        print json.dumps(r, indent=1)
    else:
        print json.dumps(r, indent=1)

    print json.dumps(show_votes(ballot_name), indent=1)


# sign_and_dump('email1', 'password1', 'b1_p0', 'b1')
