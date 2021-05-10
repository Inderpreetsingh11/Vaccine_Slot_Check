import requests
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
from SendEmail import send_mail
from pretty_html_table import build_table

#Fetch the pincode for which user wants to check the slots
pincode = input('Enter your pincode : ')
#Buffer DataFrame to avoid sending duplicate mails
df_buffer = pd.DataFrame()

while True:

    hospital_names = []
    fee_type = []
    available = []
    date = []
    age_limit = []
    vaccine = []

    #Gives tomorrow's date in required format
    nextDay = (datetime.today() + timedelta(days=1)).strftime('%d-%m-%Y')
    # Enter your User agent here
    headers = {'User-Agent' : " "}
    #GET API data
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pincode.replace(" ", ""),nextDay), headers=headers)
    #converting the response to json
    response_json = response.json()
    centers = response_json['centers']

    #fetching the data of slots for coming week
    for data in centers:
        for session in data['sessions']:
            hospital_names.append (data['name'])
            fee_type.append (data['fee_type'])
            available.append(session['available_capacity'])
            date.append(session['date'])
            age_limit.append(session['min_age_limit'])
            vaccine.append(session['vaccine'])

    pandasData = {'Centre':hospital_names,
                  'Date':date,
                  'Slots':available,
                  'Fee Type':fee_type,
                  'Age':age_limit,
                  'Vaccine':vaccine}

    #Creating a DataFrame
    df = pd.DataFrame(pandasData)

    #Checing if any slots are avaialable
    if (df.Slots > 0).any():
        #if same data recieved do nothing
        if df_buffer.equals(df[df.Slots > 0]):
            pass
        #else email the list to user
        else:
            non_empty_df = df[df.Slots > 0]
            df_buffer = non_empty_df
            output = build_table (non_empty_df, 'blue_light')
            send_mail (output)

    print('Executed')
    time.sleep(10)

