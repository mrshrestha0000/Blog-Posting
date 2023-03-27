import json
import logging

from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

logger = logging.getLogger(__name__)


class SHA:
	def __init__(self, private_key='', public_key='', signing_key='', *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		if not (private_key or public_key):
			logger.error('[SHA] Either private key or public key is required')
			raise Exception("Either private key or public key is required")

		_pvt_key = private_key.replace("\\n", "\n")
		_pub_key = public_key.replace("\\n", "\n")
		_signing_key = signing_key.replace("\\n", "\n")

		if _pvt_key:
			self._private_key = RSA.importKey(_pvt_key)

		if _pvt_key and not _pub_key:
			self._public_key = self._private_key.publickey()
		elif _pub_key:
			self._public_key = RSA.importKey(_pub_key)

		self._signing_key = RSA.importKey(_signing_key)

	def encrypt(self, data: str):
		encryptor = PKCS1_OAEP.new(self._public_key, SHA256)
		cipher_text = encryptor.encrypt(data.encode())
		b64_encoded_data = b64encode(cipher_text)
		return b64_encoded_data.decode()

	def decrypt(self, data: str):
		decryptor = PKCS1_OAEP.new(self._private_key, SHA256)
		b64_decoded_data = b64decode(data.encode())
		decipher_text = decryptor.decrypt(b64_decoded_data)
		return decipher_text.decode()

	def sign(self, data: dict):
		_payload = json.dumps(data, separators=(',', ':'))
		digest = SHA256.new(_payload.encode())
		# Signing key must be private key
		signer = PKCS1_v1_5.new(self._signing_key)
		signature = signer.sign(digest)
		b64signature = b64encode(signature)

		return b64signature.decode()

	def verify_sign(self, data, signature):
		public_key = self.get_key()

		payload = json.dumps(data)
		b64data = payload.encode()
		hash = SHA256.new(b64data)
		verifier = PKCS1_v1_5.new(public_key)

		try:
			is_verified = verifier.verify(hash, signature)
			print(is_verified)
			print("Signature is valid.")
		except Exception:
			print("Signature is invalid.")

