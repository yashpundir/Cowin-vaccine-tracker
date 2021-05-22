import datetime
import os
import requests
import schedule
from twilio.rest import Client


pkl_code = {'place':[187,'pkl']}
chd_code = {'place':[108,'chd']}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

with open('D:/Yash/Python Projects/Cowin vaccine tracker/proxies.txt','r') as file:
    data = file.readlines()

proxies = {'https': data[0][9:-2].split(','),
            'SOCKS4': data[1][10:-1].split(',')}


def function(code):

    result = []
    today = datetime.datetime.today()
    date = f"{today.day}-{today.month}-{today.year}"

    # Twilio Authentication
    account_sid = os.environ['twilio_sid'] 
    auth_token = os.environ['twilio_auth_token'] 
    client = Client(account_sid, auth_token)

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={code['place'][0]}&date={date}"
    
    got_through = False
    for key in proxies:
        for ip in proxies[key]:
            try:
                res = requests.get(url, headers=headers, proxies={key:ip}, timeout=5)
                if res.ok:
                    got_through = True
                    break
            except:
                continue
        
        if got_through==True:
            break
        
        else:
            continue
    

    if got_through:
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

        if len(result)==0:
            result = f"not available in {code['place'][1]}"

    else:
        result = 'error_in_res'


    client.messages.create(from_='whatsapp:+14155238886',  
                                        body=f"Your cowin code is {result}",      
                                        to='whatsapp:+917000263689')

    
    
   
schedule.every(6).hours.do(function, code=pkl_code)
schedule.every(6).hours.do(function, code=chd_code)
while True:
    schedule.run_pending()
