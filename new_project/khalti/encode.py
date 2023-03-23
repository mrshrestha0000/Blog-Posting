import json
from django.http import JsonResponse
from datetime import datetime
from base64 import b64encode
from django.views.decorators.csrf import csrf_exempt


from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


@csrf_exempt
def encrtpt_data(request):
    
    keys = list(request.POST.keys())

    new_data = {}

    for key in keys:
        new_data[key]= request.POST.get(key)

    print(new_data)

    local_time = datetime.now() # timezone should be in Asia/Kathmandu (i.e. UTC+5:45)
    new_data['nonce'] = int(local_time.timestamp())
    key_file_path = "/home/saphal/Desktop/MofinTestMerchantKey.pem"
    with open(key_file_path) as fkey:
        _key = fkey.read().replace("\\n", "\n")
        private_key = RSA.importKey(_key)

    digest = SHA256.new()
    dump_data = json.dumps(new_data).encode()
    b64data = b64encode(dump_data)
    digest.update(b64data)

    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(digest)
    b64signature = b64encode(signature)

    response = {
    "data": b64data.decode(),
    "signature": b64signature.decode(),
    "nonce": new_data['nonce']
    }

    return JsonResponse(response)

 
# <for account validate>
# data = {
#     "nonce":"0000",
#     "bank":"NMBBNPKA",
#     "account_no":"00011112222",
#     "account_holder_name":"Saphal Shrestha"
# }

# <Fund Transfer Charge API>
# data = {
#     "nonce":"0000",
#     "bank":"NMBBNPKA",
#     "amount":"10000"
# }

# <Fund Transfer to Bank API>
# data = {
#     "nonce":"0000",
#     "amount":"10000",
#     "bank":"NMBBNPKA",
#     "account_no":"00011112222",
#     "account_holder_name":"Saphal Shrestha",
#     "reference":"test_khalti_008"
# }



# <Khalti user exists>
# data = {
#     "nonce":"111",
#     "identity":"9800000000",
#     "amount":"1000",
#     "reference":"test_kahlti_1sdkjbckxsd0"
# }


# <Fund load API documentatation>
# data = {
#     "nonce": "1234567890",
#     "amount": "1000",
#     "user": "9800000000",
#     "reference": "test_khalti_00101",
#     "remarks": "<load remarks>"
# }


