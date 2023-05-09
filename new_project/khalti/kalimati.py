import hmac, hashlib, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sign_kalimati(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        # payload2 = request.POST.get('payload2')
        print ("key",key)
        data = {
            "key":key
        }
        payload = json.dumps(data)
        secret_key = 'PdSgVkYp3s6v9y$B&E)H+MbQeThWmZq4t7w!z%C*F-JaNcRfUjXn2r5u8x/A?D(G'
        hash_object = hashlib.sha256(payload.encode())
        mac = hmac.new(secret_key.encode(), hash_object.digest(), hashlib.sha256).hexdigest()
        print ({'mac': mac})
        return JsonResponse({'mac': mac})
