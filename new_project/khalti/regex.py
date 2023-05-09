import re
import requests, random, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



base_url = "https://uatservices.khalti.com"
uat_test_token = "TEST:e6FgwunPqYZgRPoJltLA"
uat_live_token = "3aQN4uqeR57L0tfxrmvO" 
amount = 10

# phone_number = input("Please enter your phone number: ")
@csrf_exempt
def recharge(request):

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        print ("phone_number:",phone_number)


        smart = re.compile("^96[0-9]{8}|988[0-9]{7}")
        ncell = re.compile('^(98[012])|(970)[0-9]{7}$')
        nt_prepaid = re.compile('^9[78][46][0-9]{7}$')
        nt_postpaid = re.compile('^985[0-9]{7}$')
        cd_prepaid = re.compile('^97[46][0-9]{7}$')
        cd_postpaid = re.compile('^975[0-9]{7}$')

    # Validate the phone number against the regex

        if re.match(smart, phone_number):
            nt_postpaid_url = f"{base_url}/api/use/smartcell/"
            data = {
                "token":uat_live_token,
                "reference":random.randint(1, 100000000000000000000),
                "amount":amount,
                "number":phone_number
            }

            response = requests.post(url=nt_postpaid_url, data=data)
            res = response.json()
            status = res.get("status")

            if status == True:
                return JsonResponse({
                    "service_response":res,
                    "token_used":uat_live_token,
                    "Service_used":"smart"
                    }, safe=False)
            
            if status == False:  
                return JsonResponse({
                    "Error_message":res,
                    "Service_used":"smart"
                }, safe=True)

        elif re.match(ncell, phone_number):
            nnt_postpaid_url = f"{base_url}/api/use/ncell/"
            data = {
                "token":uat_live_token,
                "reference":random.randint(1, 100000000000000000000),
                "amount":amount,
                "number":phone_number
            }

            response = requests.post(url=nnt_postpaid_url, data=data)
            res = response.json()
            status = res.get("status")

            if status == True:
                return JsonResponse({
                    "service_response":res,
                    "token_used":uat_live_token,
                    "Service_used":"ncell"
                    }, safe=False)
            
            if status == False: 
                return JsonResponse({
                    "Error_message":res,
                    "Service_used":"ncell"
                }, safe=True)
                
        elif re.match(nt_prepaid, phone_number):
            nt_prepaid_url = f"{base_url}/api/use/ntc/"
            data = {
                "token":uat_live_token,
                "reference":random.randint(1, 100000000000000000000),
                "amount":amount,
                "number":phone_number
            }

            response = requests.post(url=nt_prepaid_url, data=data)
            res = response.json()
            status = res.get("status")

            if status == True:
                return JsonResponse({
                    "service_response":res,
                    "token_used":uat_live_token,
                    "Service_used":"nt_prepaid"
                    }, safe=False)
            
            if status == False:
                
                return JsonResponse({
                    "Error_message":res,
                    "Service_used":"nt_prepaid"
                }, safe=True)


        elif re.match(nt_postpaid, phone_number):
            nt_postpaid_url = f"{base_url}/api/use/ntc/"
            data = {
                "token":uat_live_token,
                "reference":random.randint(1, 100000000000000000000),
                "amount":amount,
                "number":phone_number
            }

            response = requests.post(url=nt_postpaid_url, data=data)
            res = response.json()
            status = res.get("status")

            if status == True:
                return JsonResponse({
                    "service_response":res,
                    "token_used":uat_live_token,
                    "Service_used":"nt_postpaid"
                    }, safe=False)
            
            if status == False:
                
                return JsonResponse({
                    "Error_message":res,
                    "Service_used":"nt_postpaid"
                }, safe=True)

        elif re.match(cd_prepaid, phone_number):
            return JsonResponse({
                    "Service_used":"cd_prepaid"
                }, safe=True)

        elif re.match(cd_postpaid, phone_number):
            return JsonResponse({
                    "Service_used":"cd_postpaid"
                }, safe=True)

        else:
            return JsonResponse({
                    "Error_message":"Invlaid number."
                })
        

