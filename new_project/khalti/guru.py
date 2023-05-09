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
			

encryption_public_key = """-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3S+RBbsDVTuvORx/rB2B\nen+ziBlHrzD1orQlsxcZsUlfUtv3GhrvsREt0XtFcwMan8Et2ztpdAu2dtV6AQ7X\nCcQDEIzUPU/ncniO/W0sekXyfcO1eCi8+uKIDs70LxFHhj932Do6a7C6WTSMtfl8\nVTrm9aNOTDN+KYOitOWozt8RKhAPLsII7C2uP79yyoNm0nCTFPPHMXqf9pk8zXW0\nJS/7VS60M6QxxJgLSuj4r7QDtKc5imj+4QM0ek2KFcSLZFvel9C/R2phrX/sf7Hu\ncuImmSRX7yMkxu3ev+XdhGV3SqSkuRNrAAuLYg4N9EOuC0L5ir4XeFfGz7IZ0sdS\npQIDAQAB\n-----END PUBLIC KEY-----"""

signing_private_key = """-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAzVOjkmagyR23N0wCeVRvvzDy/vslzlWkxkUhO3r7hl+ENSML\n1/aVF8Wx0JGHUH13u3wKs0wYYX6uf5uFvwfNLJ61iojaPWyTICZctU96SsoC/jTu\n1v4aKXjC3BbvnnYOy+GibWUWMoNI6zcsg8EkWXrH/36bNaKVnoA18Kfh1d312EOu\noqJocsvOCfXlCirSdrQkKALe2Ze4mrDvWylOnHE5OUF7RBY+h5FHzJGcOA3S8Ou2\nQWwv8KRNF+iFrbIgBxJQbS9CNEkuOQOl3Cp4sCI+8UZN1jJ77uA/dYtkzVmLSflH\nqY3Y/FvEU+CQtJlcdPHciui4TogKyB0KxCj2LQIDAQABAoIBAQCeHmvX4UqutkCS\nx+kb0Gdh3+sxauz5UcDbov7tlE7AcywX045aWJ0GOostp/SBiq265tJCszYPVoRA\n5t5/dx2M4AfD0JHoPYWre39nbPYrRBg79T18uSAikcnVvZ/38siAP5lbDz6h1bJA\n2TNhn0pD0ibUXYZfLn50Gh3v3wkuLSbvlFMBHGgZ1vfQEb3K7w7dVa0FBLXK4Vw6\n23qEZ+n3zOvqr9jLcwiAH0dbeDDZZq4YciF3hxAU4ngwUv3LaLfprAcOQShv6h2J\nJJ8Naifml/ZmB8SINaULopBPzBHXSUyny5E0kLMJUYv7VM6b9136Zp27j60ox8hD\n++ef8rltAoGBANRbLdiYnc2TYYqICIJJGIjlwO2NGyzhoaUvWSUSUF7dvE6Zg20B\nsZUKRdNQFfftTQNExFcTLPkZ1sMc9wrxnSuGdV/zcZ5iswupl21NkpJ9OaQF0r8B\n6ch+yW9dQHFqs+xGK51CAZn5JgJxCrYkaiyvAQ/BkVxp3e76du2RuqjrAoGBAPeG\nnXRWR52bAhFbN4J+dMJhDv+Lp1ZXrAXlJ00OpjsOfxbjTulUo7uY4TNaQvswkQ/f\nm3b414Aa+n7XnjcNJYzoB6TpB1LOg80Nmn2VEymaOrzie4Ya00NQze1yeTFX2NkK\n+YL7IBV4JYjEI12gJbjFM71xB0BrLiigqSTu5RdHAoGBANHo52KpSaOCQfL8EN0o\ngBYidhjbWLd+uZhdO1NHzSZZLODNInrIJ8/Zfbgp++09JtlKSoKAM/5wKjhoE1NA\nDkqN+MxGClOz4KRwmXy0J2SiYC3gi7e/nmZP3bI1jZQPE5dErawfKRIYlBfpwdrW\nGBXfT79RaezdwUGPV6vyV37NAoGBAONzobBLsFdVHxtP1Lxm82fCxINykvw2Z+6q\n2ehnM71E3ufrTJIAosw5+Ya0xKQJxuLtOPCkTXJ8V/7Cp7IytHS8qnmRYJdpCZgd\njf8kQ42RGbSD8boTYFqVIAW3kUIUVUFsYkdH9/2CgAsjINRh2wfkvlywRledpbbT\nm1pC4+T1AoGAfpaXko6dPzW+T536rKDvh7KRzdQr2X1Md7HynKFn3EYxPUkaczDQ\nbh1u8E0deEZL6DiZGTZZnpF3dwQ4qMsPP3y6aHKzJSIsxdMQi2eeWMFQk6OyqNm0\nzAPKzuyuyvEJLYfMUvy3LiAMfszJBUal41SXT2JDWxrvGpKLuLNZFUU=\n-----END RSA PRIVATE KEY-----"""

sha = SHA(

    public_key=encryption_public_key, 
    signing_key=signing_private_key
)

# # ACCOUNT NAME VALIDATION
data = {
 "institutionId":"c11e7ba1-e05a-4d04-89a6-2fa053a2faad",
 "destinationAccountNo": sha.encrypt("00130MNS000045120001"),
 "beneficiaryAccountName": sha.encrypt("Guru Infosys"),
 "beneficiaryMobileNo": sha.encrypt("9800000000"),
 "accountType": "BANK"
}

# VALIDATE TRANSACTION
# data = {
# 	"merchantId": "1001",
# 	"institutionId": "5c2ef94a-f4cb-46b0-bcfd-7a1f27efc9aa",
# 	"serviceOptionId": "3a2507f0-6b45-4c49-8213-80d77f03c2bf",
# 	"originatingTransactionId": "Khalti_003",
# 	"transactionDateTime": "2023-01-08 15:28:40",
# 	"sourceAccountNo": sha.encrypt("9844694450"),
# 	"debtorBank": "KHALTI",
# 	"debtorBankBranch": "WALLET",
# 	"amount": "1000.00",
# 	"currency": "NPR",
# 	"serviceCharge": "0.00",
# 	"senderName": sha.encrypt("Guru"),
# 	"senderAddress": "Kathmandu",
# 	"beneficiaryMobileNo": sha.encrypt("9800000000"),
# 	"senderContactDetail": "9844694450",
# 	"destinationAccountNo": sha.encrypt("00130MNS000045120001"),
# 	"beneficiaryAccountName": sha.encrypt("Guru Infosys"),
# 	"beneficiaryAddress": "Kathmandu",
# 	"remarks": "test sahakari withdraw",
# 	"additionalFields": {
# 	"relationship": "Brother"
# 	}
# }

# CONFIRM TRANSACTION 
# data = {
#     "originatingTransactionId": "Khalti_003",
#     "confirmationDateTime": "2023-01-08 15:28:40",
#     "gwOriginatedId": "c530bd26-270d-469b-8124-35a86c28b1cf"
# }

# CHECK TRANSACTION STATUS
# data = {
# "institutionId": "5c2ef94a-f4cb-46b0-bcfd-7a1f27efc9aa",
# "originatingTransactionId": "Khalti_0003"
# }

signature = sha.sign(data)

print(json.dumps(data), end="\n\n")

print(signature)