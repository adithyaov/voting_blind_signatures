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
from random import SystemRandom
class Verifier:
	"""docstring for Verifier"""
	def __init__(self, pub_key):
		self.pub_key = pub_key
		
	def verify(self, msg_digest, msg_signature):
		return self.pub_key.verify(msg_digest, (msg_signature,))

	def verify_msg(self, msg, msg_signature):
		return self.verify(hash(msg), msg_signature)
class Authority(Verifier):
	"""docstring for Authority"""
	def __init__(self):
		self._priv_key = RSA.generate(3072)
		pub_key = self._priv_key.publickey()
		Verifier.__init__(self, pub_key)

	def sign(self, msg_blinded):
		return self._priv_key.sign(msg_blinded, 0)
class Blinder(Verifier):
	"""docstring for Blinder"""
	def __init__(self, pub_key):
		Verifier.__init__(self, pub_key)
		self.r = SystemRandom().randrange(self.pub_key.n >> 10, self.pub_key.n)
		
	def blind(self, msg_digest):
		return self.pub_key.blind(msg_digest, self.r)

	def blind_msg(self, msg):
		return self.blind(hash(msg))

	def unblind_msg(self, blinded_msg):
		return self.pub_key.unblind(blinded_msg, self.r)

	def update_random(self):
		self.r = SystemRandom().randrange(self.pub_key.n >> 10, self.pub_key.n)


auth_id={'v_id':'a'}
msg = json.dumps({'v_for':"Prabal",'ballet_id':"GS",'timestamp':time.time()})
#message in json format
msg_json = (msg).encode('utf-8')
A=Authority()
B=Blinder(A.pub_key)
bm = B.blind_msg(msg_json)
auth_id['blind_msg']=bm
msg=json.dumps(auth_id)
print(msg)

#send the msg to authenticator




