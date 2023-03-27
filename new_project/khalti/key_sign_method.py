import json
from datetime import datetime
from base64 import b64decode, b64encode

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

key_file_path = "sign/keys/hamro_tech.pem"

def verify_request(data, signature):
	digest = SHA256.new()
	signature = b64decode(signature)
	data = b64decode(data)
	digest.update(data)

	with open(key_file_path) as fkey:
		_key = fkey.read().replace("\\n", "\n")
		private_key = RSA.importKey(_key)

	verifier = PKCS1_v1_5.new(private_key)
	is_valid = verifier.verify(digest, signature)
	return data.decode()

def sign_request(data):
	# local_time = datetime.now() # timezone should be in Asia/Kathmandu (i.e. UTC+5:45)
	# data['nonce'] = int(local_time.timestamp())

	with open(key_file_path) as fkey:
		_key = fkey.read().replace("\\n", "\n")
		private_key = RSA.importKey(_key)

	digest = SHA256.new()
	dump_data = json.dumps(data).encode()
	b64data = b64encode(dump_data)
	digest.update(b64data)

	signer = PKCS1_v1_5.new(private_key)
	signature = signer.sign(digest)
	b64signature = b64encode(signature)
	response = {
		"data": b64data.decode(),
		"signature": b64signature.decode()
	}

	return json.dumps(response)
