from django.test import TestCase
import json

# Create your tests here.

data = {
    "movies": [
        {
            "name": "Chhakka Panja 4 (PG)",
            "theatres": [
                {
                    "name": "FCube Cinemas (Chabhil, Kathmandu)",
                    "shows": [
                        {
                            "show_id": "55424:fcube",
                            "datetime": "2023-03-20T11:00:00+05:45",
                            "auditorium_name": "Cube 3",
                            "use_new_layout": False
                        },
                        {
                            "show_id": "55427:fcube",
                            "datetime": "2023-03-20T14:00:00+05:45",
                            "auditorium_name": "Cube 3",
                            "use_new_layout": False
                        }]
                        
                }]
        },{
            "name": "Chhakka Panja 4 (PG)",
            "theatres": [
                {
                    "name": "FCube Cinemas (Chabhil, Kathmandu)",
                    "shows": [
                        {
                            "show_id": "55424:fcube",
                            "datetime": "2023-03-20T11:00:00+05:45",
                            "auditorium_name": "Cube 3",
                            "use_new_layout": False
                        },
                        {
                            "show_id": "55427:fcube",
                            "datetime": "2023-03-20T14:00:00+05:45",
                            "auditorium_name": "Cube 3",
                            "use_new_layout": False
                        }]
                        
                }]
        }]
}


# a = data.get('movies')
# b = a[0] 
# c = b.get('name')
# print (a)
# print (b) 
# print (c)

# for i in a:
    # print(a[0].get("name"))


# a = len(data.get('movies'))
# for i in a:

# a = data.get('movies')
# for i in a:
#     d = (x for x in data.get('movies')[0].get("name"))
#     print ("".join(d))



data_data = {
        "displayName": "Toribari Khanepani Tatha Sarsafai Upabhokta Samiti ",
        "address": "Barahachetra Na.pa.-1 Sunsari",
        "contact": "025-550100",
        "apiUsername": "L!v3:Tor!b@r!",
        "paymentCode": "NP-ES-TORIBARI",
        "nameApi": "trbr",
        "logoPath": "watersoft.com.np/WaterTariffSystem-web/logoUpload/469_1676022884127.jpg?pfdrid_c=true",
        "organizationType": "water"
    }

displayName = data_data.get('displayName')
address = data_data.get('address')
contact = data_data.get('contact')
apiUsername = data_data.get('apiUsername')
paymentCode = data_data.get('paymentCode')


new_data ={
        "display_name":displayName,
        "address": address,
        "contact": contact,
        "api_username": apiUsername,
        "payment_code": paymentCode
}

new_data = json.dumps(new_data)
print (new_data)