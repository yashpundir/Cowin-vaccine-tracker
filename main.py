import datetime
import os
import requests
import schedule
from twilio.rest import Client

# ambala_code = 193
# chd_code = 108
# meerut = 676
pkl_code = 187

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def function():
    result = []
    today = datetime.datetime.today()
    date = f"{today.day}-{today.month}-{today.year}"

    # Twilio Authentication
    account_sid = os.environ['twilio_sid'] 
    auth_token = os.environ['twilio_auth_token'] 
    client = Client(account_sid, auth_token)

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={pkl_code}&date={date}"
    res = requests.get(url, headers=headers)

    if res.ok:
        res_json = res.json()

        for center in res_json['centers']:
            place = {}
            flag = False
            for session in center['sessions']:
                if (session['min_age_limit']==18) and (session['available_capacity']>0) and not(flag):
                    flag = True
                    place[center['name']] = [session['available_capacity']]
                    
                elif flag and (session['min_age_limit']==18) and (session['available_capacity']>0):
                    place[center['name']].append(session['available_capacity'])
            
            if flag:
                result.append(place)

    else:
        result = 'error in res'


    if len(result)>0:
        message = client.messages.create(from_='whatsapp:+14155238886',  
                                        body=f"Your cowin code is \n{result}",      
                                        to='whatsapp:+917000263689')

    else:
        message = client.messages.create(from_='whatsapp:+14155238886',  
                                        body=f"Your cowin code is \nno slots available",      
                                        to='whatsapp:+917000263689')
    

schedule.every(6).hours.do(function)
while True:
    schedule.run_pending()
