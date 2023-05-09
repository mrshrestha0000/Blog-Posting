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
			


encryption_public_key = """-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArkkGZ2SQ9r8zlStsqWVc\nRKkp4QzBkyT6IUkSvAM25MuEbAW09Xxdzn8BTZNrmtpYVW5ErI1k3JtTNLnNIWEw\n3kvhgamdsZiEpfpq1VffbYoXZIP8m2L+7J17vdtyBFPYH7qvW6VwSBDdZ8d4Avj3\na4wbiUwuyEYJWX5ca/PnU0I2qCbsSQ1kKgG+iF12TQmc7ewr1yZdAKKM28TISkib\nhhuxlCgzdPiE7hrEFSKKN+NB3SEfr1jZOguoMDUP5StbgGjqw+qkvmTRCo+DXmjt\nZi9Pno2Q60qIg3Zg5k7S4wGRTdPS7i7TKk/EsMez8zni17pnf2vxzNDvgXlkQVHC\nKwIDAQAB\n-----END PUBLIC KEY-----"""

signing_private_key = """-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCmmiMURyr1pXwB\n+sH6BgMNegG8yWR106xdkOUXjhVZhI5krfTKWhrcHCIFJx6ffYCIz+SijXftL9S5\nLtYJsgsxwtrdpoc3kO5IlA1kMCH/PppK1zzcv/P0DMSuLvjPgReR0JpPUyvX7tAq\nWHe/W9JGAd5bugt5gLBmB8P5bo62IkBPVMPVdzxKfzf/4wOK9EGG2xTbK7zvGrw9\ngdcXkeRhAhUnXeQUHhwnf5mxBfKWXMLPHEg+7JVrDKNRJYKigo4fEfWyT4gQ1jC1\nkV4j5ySSILZi+CfNSrum4c5fAkDY/xm4pc0oUHtqqPjw9lwzmc/CG3RoUzxFSBvu\ndfspPN3xAgMBAAECggEAIuknsqcbHHB55NxL6315BEjttkapU3twogarytzOIn0B\nbZ16LzDkcf0/L787zoX4+jI+IcXtPHmKZOeomE2DxQCk5k9wBDfNhs3nZHgll5vh\nrw8dRNDAaQKH8EwNfUX6z2Zb/4VZKZ10Z3s0VJgEHwFjO+tnXiWWUTsNWOZO52E9\ndOfbLfFQGd4tZQl/JnTdx0kzn6itwHbbwQZqDYpjPeWQrKV9WupLeM2m3QYtXTde\nzvvG0RS/J+wGSDeDwLlNPvYDwTU4qC/wLulVGU3lZx7Nvsedlihom6657SCUkzMK\nmE1MmgkgaJ11W5slXCF0HpdmkV7q/C+j8k2pURaatQKBgQDNJzyns4bzeSuWM3WQ\nc39ycen1E0k37MS7l28dmLvKzkqiH5dEzZiN/eGXgDCRL4/kMxB3xAElvNlcsCUT\nlDLvZP5D3ATGcgwIfSK7IEXt5ywLmCiJBRnW6J53+nHglWRBI09TZMAOJAg+Gn9M\npIb+HxJDvH719tsW/ouxJlTfxwKBgQDP5N46L5yyRIr92E3Un5fGhcvX5x81L0mH\nCRebbZD7dlRhEy5l2lppjKMalFu4d6gqHlsnuUhggz9eyI/qeZvhwX3EwPeGmDK/\nAxvQSCetnf8IwHVaQtTsDIM/NLPWUrYfOipfTkdTiYPa5kNxoA8kVBlnr4xjLf9B\n25W9VKZEhwKBgD6gKa3v6dRNOvcBAnR0LYWcLJU5q/I8ftndInhgdYM1cicHib/h\nGx7NT55V7X2EjWJWDELjPI5uldPrmYXeiaX2qH/CnFqP2giFWqLQ+Ufkd9eaPVWG\njxrBrA5oD3dFY3NW+hI1AUPP0AxVPmMBHoxYo9S1p/QhxUPBtJcBYotlAoGBAMlw\nTFw48i5R+BOLWa7ijOARmLi0/Co+jZJInxU9jzP5Lj15poWOk/ieCxSgGFefqdRV\n4aGWCKlrwyWGVNyvxPl00Paqu60xIEqxKmwg3kF+TDYgthUlmMa4QRwnZvIO5uVP\nKOt8H+Sz5I1gfI1GuCVNT+iF0xPu59zadjckJI9VAoGBAKrUiwxSoHp88WnoKza7\nfy4V5fI1jsKEDNceWB1zrzmA6avO6fhrGcUnIEjxos1UPpGvEzw1e5z7g70JmnTH\nflxBg+7gHqk3BPou/ffsVGo9+vbEKxkKBwKztKfliWcQQH05kgO+tfxnIpflGHkb\nSDwAKwBpHDTgY3RoshIv38Iw\n-----END PRIVATE KEY-----"""

sha = SHA(

    public_key=encryption_public_key, 
    signing_key=signing_private_key
)

# # ACCOUNT NAME VALIDATION
data = {
 "institutionId":"X5SZgi7kzX4Il+mEO7PUag==",
 "destinationAccountNo": sha.encrypt("007.12429.01.06.SS.1"),
 "beneficiaryAccountName": sha.encrypt("PARBATI GHIMIRE"),
 "beneficiaryMobileNo": sha.encrypt("9818252527"),
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

print(json.dumps(data), end="\n")

print("signature : ",signature)