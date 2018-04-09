#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:37:41 2018

@author: dineshvashisht
"""

import time
import json
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import _pickle as pickle
from random import SystemRandom
from requests import *


class Blinder():
    """docstring for Blinder"""
    def __init__(self, pub_key):
        self.pub_key=pub_key
        self.r = SystemRandom().randrange(self.pub_key.n >> 10, self.pub_key.n)
        
        
    def blind(self, msg_digest):
        return self.pub_key.blind(msg_digest, self.r)

    def blind_msg(self, msg):
        return self.blind(hash(msg))

    def unblind_msg(self, blinded_msg):
        return self.pub_key.unblind(blinded_msg, self.r)

    def update_random(self):
        self.r = SystemRandom().randrange(self.pub_key.n >> 10, self.pub_key.n)
def open_object(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

auth_id={'token':'a'}

#message in json format
msg_json = json.dumps({'v_for':"Prabal",'ballet_id':"GS",'timestamp':time.time()})

#getting the public key from file b1
pub_key=open_object("b1")
B=Blinder(pub_key)
bm = B.blind_msg(msg_json)
print(len(str(bm)))
auth_id['msg']=bm
msg=(auth_id)
print(type(msg))
#send the msg to authenticator
r = post("http://10.64.10.171:8080/sign-blind-msg/b1",json=msg)
print(r.text)





