from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from datetime import datetime
from base64 import b64encode


from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


# Create your views here.


@csrf_exempt
def movies_views(request):

    if request.method == "POST":
        url = "https://khalti.com/api/v5/service/use/movie/search/"
        headers = {
            "Authorization": "token 65fc9318e581f3afc14dc8ed0590fc6c3803eb31",

            "Content-Type": "application/json"
        }
        context = {}
        response = requests.post(url, headers=headers)

        # print ("response:",response)

        movie_data = response.json()
        a = movie_data.get('movies')
        b = []

        for i in a:
            d = i.get("name")
            b.append(d)
            # print (d)

        length = len(b)

        return JsonResponse({"data": b, "movies_count": length}, safe=False)


@csrf_exempt
def new_khanepani(request):
    payment_code = request.POST.get('payment_code')
    if request.method == "POST":
        url = "https://watersoft.com.np/WaterTariffSystem-web/webresources/billing/organizations"

        headers = {
            # "Content-Type":"application/json",
            "Authorization": "Basic a2hhbHRpOmsjQGxUITEyMTIx"
        }
        context = {

        }
        response = requests.get(url, headers=headers)
        paymentCode = response.json()

        for i in paymentCode:
            validate_display_name = i.get('displayName')
            validate_address = i.get('address')
            validate_contact = i.get('contact')
            validate_apiUsername = i.get('apiUsername')
            validate_payment_code = i.get('paymentCode').strip()

            if validate_payment_code == payment_code:

                new_data = {
                    "counter_name": validate_display_name,
                    "service_name": validate_display_name,
                    "counter_info": {
                        "display_name": validate_display_name,
                        "address": validate_address,
                        "contact": validate_contact,
                        "api_username": validate_apiUsername,
                        "payment_code": validate_payment_code,
                    }
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
            "Authorization": "Basic a2hhbHRpOmsjQGxUITEyMTIx"
        }
        response = requests.get(url, headers=headers)
        paymentCode = response.json()

        for i in paymentCode:
            validate_display_name = i.get('displayName')
            validate_address = i.get('address')
            validate_contact = i.get('contact')
            validate_apiUsername = i.get('apiUsername')
            validate_payment_code = i.get('paymentCode')

            if validate_payment_code == payment_code:

                context = {
                    "display_name": validate_display_name,
                    "address": validate_address,
                    "contact": validate_contact,
                    "api_username": validate_apiUsername,
                    "payment_code": validate_payment_code,
                    "service_slug": service_slug
                }
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


# def migrate_sage_movies(request):
#     if request.method == "POST":
#         # service_name = request.get.POST('service_name')
#         url = request.POST.get('url')
# #         # api_user_v2 = request.get.POST('api_username')
#         token_url_v2 = request.POST.get('token_url_v2')
#         # location_id = request.get.POST('location_id')
#         # api_secret_v2 = request.get.POST('api_secret_v2')
#         # api_password_v2 = request.get.POST('api_password_v2')
#         # showinfo_url_v2 = request.get.POST('showinfo_url_v2')
#         # deadline_obj_str = request.get.POST('deadline_obj_str')
#         # show_list_v2_url = request.get.POST('show_list_v2_url')
#         # deadline_obj_str = request.get.POST('deadline_obj_str')
#         # show_list_v2_url = request.get.POST('show_list_v2_url')
#         # movies_list_v2_url = request.get.POST('movies_list_v2_url')
#         # seat_select_url_v2 = request.get.POST('seat_select_url_v2')
#         # clear_selection_url_v2 = request.get.POST('clear_selection_url_v2')
#         # download_url_v2 = request.get.POST('download_url_v2')

#         a = {
#             "url":url,
#             "token_url_v2":token_url_v2
#         }

#         print (token_url_v2)
#         return JsonResponse(a, self=False)


@csrf_exempt
def migrate_sage_movies(request):

    if request.method == "POST":
        service_name = request.POST.get('service_name')
        url = request.POST.get('url')
        api_user_v2 = request.POST.get('api_username')
        token_url_v2 = request.POST.get('url')+'api/v1/Cinema/GetUserToken'
        location_id = request.POST.get('location_id')
        api_secret_v2 = request.POST.get('secret_key')
        api_password_v2 = request.POST.get('api_password')
        showinfo_url_v2 = request.POST.get('url')+'api/v1/Cinema/GetShowDetail'
        deadline_obj_str = datetime.now().isoformat(timespec="minutes")
        show_list_v2_url = request.POST.get('url')+'api/v1/Cinema/GetShowList'
        movies_list_v2_url = request.POST.get(
            'url')+'api/v1/Cinema/GetMovieList'
        seat_select_url_v2 = url+'api/v1/Cinema/GetSeatSelection'
        clear_selection_url_v2 = url+'api/v1/Cinema/ClearSelection'
        download_url_v2 = url+'api/v1/Cinema/GetUserTicket'

        a = {
            "service_name": service_name,
            "url": url,
            "counter_info": {
                "api_user_v2": api_user_v2,  # api_username
                "token_url_v2": token_url_v2,
                "location_id": location_id,
                "api_secret_v2": api_secret_v2,
                "api_password_v2": api_password_v2,
                "showinfo_url_v2": showinfo_url_v2,
                "deadline_obj_str": deadline_obj_str,
                "show_list_v2_url": show_list_v2_url,
                "movies_list_v2_url": movies_list_v2_url,
                "seat_select_url_v2": seat_select_url_v2,
                "clear_selection_url_v2": clear_selection_url_v2,
                "download_url_v2": download_url_v2
            }
        }
        return JsonResponse(a, safe=False)

import base64

@csrf_exempt
def uranus(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        name = request.POST.get('name')
        username = request.POST.get('username')
        company_code = request.POST.get('company_code')
        password = request.POST.get('password')
        client_id = "{client_id}"

        concat_username = username+"_"+company_code

        encoded_auth = base64.b64encode(f"{concat_username}:{password}".encode("utf-8")).decode("utf-8")
        auth_header = f"Basic {encoded_auth}"

        return JsonResponse({"data_to_post_on_service_update_counter":{
            "service_name": name,
            "counter_info": {
                "detail_url": f"{url}/api/Payment/Inquiry/{client_id}",
                "Username": concat_username,
                "Password": password,
                "payment_url": f"{url}/api/Payment/Payment"
            }
        },
        "Authorization":f"{auth_header}"
        })

