from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, requests
from datetime import datetime
from base64 import b64encode


from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


# Create your views here.
@csrf_exempt
def bankload(request):
    amount: request.get.POST('amount')
    user: request.get.POST('user')
    reference: request.get.POST('reference')
    remarks: request.get.POST('remarks')
    data = {
    "nonce": "nonce",
    "amount": amount,
    "user": user,
    "reference": reference,
    "remarks": remarks
    } 
    print (data)
    if request.method == "POST":
        local_time = datetime.now() # timezone should be in Asia/Kathmandu (i.e. UTC+5:45)
        data['nonce'] = int(local_time.timestamp())
        key_file_path = "/home/saphal/Downloads/TestTestKumariBankLoad.pem"
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

        print (json.dumps(response))
        print (data['nonce'])

        return JsonResponse(response, safe=False)
        # return json.dumps(response), data['nonce']
    

@csrf_exempt
def movies_views(request):  

    if request.method == "POST":
        url = "https://khalti.com/api/v5/service/use/movie/search/"
        headers = {
            "Authorization":"token 4bcb893557584c364f8e069b136d29af97440edd",
            "Content-Type":"application/json"
        }
        context = {}
        response = requests.post(url, headers = headers)

        print ("response:",response)

        movie_data = response.json()
        a = movie_data.get('movies')
        b= []

        for i in a:
            d = i.get("name")
            b.append(d)
            print (d)
            
        return JsonResponse( {"data": b}, safe=False)
    
@csrf_exempt
def new_khanepani(request):
    payment_code = request.POST.get('payment_code')
    if request.method == "POST":
        url = "https://watersoft.com.np/WaterTariffSystem-web/webresources/billing/organizations"
        # url = "https://khalti.com/api/v5/service/use/movie/search/"

        headers = {
            # "Content-Type":"application/json",
            "Authorization":"Basic a2hhbHRpOmsjQGxUITEyMTIx"
        }
        context = {
          
        }
        response = requests.get(url, headers = headers)
        paymentCode = response.json()
        # a = paymentCode[1]
        # b = a.get('paymentCode')
        # print (b)

        for i in paymentCode:
            validate_display_name = i.get('displayName')
            validate_address = i.get('address')
            validate_contact = i.get('contact')
            validate_apiUsername = i.get('apiUsername')
            validate_payment_code =  i.get('paymentCode')

            if validate_payment_code == payment_code:
                
                new_data = {
                    "display_name": validate_display_name,
                    "address": validate_address,
                    "contact": validate_contact,
                    "api_username": validate_apiUsername,
                    "payment_code": validate_payment_code
                }
                return JsonResponse(new_data, safe=False)
                           
        error_message = {
            "error": "Khanepani not found with payment code. "
        }
        return JsonResponse(error_message, safe=False)
    else:
        error_message = {
            "error": "Method not allowed. "
        }
        return JsonResponse(error_message, safe=False)
    
@csrf_exempt
def counter_update(request):
    payment_code = request.POST.get('payment_code')
    service_slug = request.POST.get('service_slug')

    if request.method == "POST":
        url = "https://watersoft.com.np/WaterTariffSystem-web/webresources/billing/organizations"
        # url = "https://khalti.com/api/v5/service/use/movie/search/"

        headers = {
            # "Content-Type":"application/json",
            "Authorization":"Basic a2hhbHRpOmsjQGxUITEyMTIx"
        }
        response = requests.get(url, headers = headers)
        paymentCode = response.json()

        for i in paymentCode:
            validate_display_name = i.get('displayName')
            validate_address = i.get('address')
            validate_contact = i.get('contact')
            validate_apiUsername = i.get('apiUsername')
            validate_payment_code =  i.get('paymentCode')

            if validate_payment_code == payment_code:
                
                context = {
                    "display_name": validate_display_name,
                    "address": validate_address,
                    "contact": validate_contact,
                    "api_username": validate_apiUsername,
                    "payment_code": validate_payment_code,
                    "service_slug":service_slug
                }


# from data_migration import change_softlab_to_watermark

# def change_karmaiya_to_watermark():
#     service_slug = "karmaiya-khanepani"
#     counter_defaults = {
#         "display_name": "Karmaiya Khanepani",
#         "address": "Bagmati N.Pa.-11 Karmaiya, Sarlahi",
#         "contact": "krmya",
#         "api_username": "L!v3:K@rm!y@",
#         "payment_code": "NP-ES-KARMAIYA",
#     }
#     change_softlab_to_watermark(service_slug, counter_defaults)

                # return JsonResponse(log, safe=False)
                return render(request, "khalti/khanepani.html", context=context)
                           
        error_message = {
            "error": "Khanepani not found with payment code. "
        }
        return JsonResponse(error_message, safe=False)
    else:
        error_message = {
            "error": "Method not allowed. "
        }
        return JsonResponse(error_message, safe=False)

    

    

