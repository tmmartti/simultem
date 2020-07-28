import requests
import json
import pickle
from get_token import new_token
from datetime import date, datetime, timedelta

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def get_available_units(token, reservation_id):
    api_url = 'https://api.apaleo.com/availability/v1/reservations/' + reservation_id + '/units'
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

    
def unit_list(reservation_id):    
    try:
        rooms = get_available_units(old_token, reservation_id)['units']
        return rooms
    except:
        rooms = get_available_units(new_token, reservation_id)['units']
        print ('Used a new token')
        return rooms

def get_cleanliness(token, unit_id):
    api_url = 'https://api.apaleo.com/inventory/v1/units/' + unit_id
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

def cleanliness(unit_id):    
    try:
        cleanliness_status = get_cleanliness(old_token, unit_id)
        return cleanliness_status['status']['condition']
    except:
        cleanliness_status = get_available_units(new_token, unit_id)
        print ('Used a new token')
        return cleanliness_status['status']['condition']

def get_booking_details(token, reservation_id):
    api_url = 'https://api.apaleo.com/booking/v1/reservations/' + reservation_id
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

def booking_details(reservation_id):
    try:
        details = get_booking_details(old_token, reservation_id)
        return details
    except:
        details = get_booking_details(new_token, reservation_id)
        print ('Used a new token')
        return details

def assign_unit_call(token, reservation_id):
    put_url_base = 'https://api.apaleo.com/booking/v1/reservation-actions/' + reservation_id + '/assign-unit/'
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    available_units = unit_list(reservation_id)
    booking_arrival = booking_details(reservation_id)['arrival']
    arrival_time = datetime.fromisoformat(booking_arrival)
    arrival_date = arrival_time.date()
    today = date.today()
    tomorrow = today + timedelta(days=1)
    if arrival_date not in [today, tomorrow]:
        unit_id = available_units[0]['id']
        put_url = put_url_base + unit_id
        response = requests.put(put_url, headers=headers)
        print (response)
        if response.status_code != 200:
            print ('Failed assign to ' + unit_id)
        else: 
            print ('Assigned to ' + unit_id)
    else:
        dirty = []
        for unit in available_units:
            unit_id = unit['id']
            cleanliness_status = cleanliness(unit_id)
            if cleanliness_status == 'Clean':
                put_url = put_url_base + unit_id
                response = requests.put(put_url, headers=headers)
                print (response)
                if response.status_code != 200:
                    print ('Failed assign to ' + unit_id)
                else: 
                    print ('Assigned to ' + unit_id)
                break
            else:
                dirty.append(unit_id)
        if len(dirty) == len(available_units):
            print ('No clean units available')
            unit_id =available_units[0]
            put_url = put_url_base + unit_id
            response = requests.put(put_url, headers=headers)
            print (response)
            if response.status_code != 200:
                print ('Failed assign to ' + unit_id)
            else: 
                print ('Assigned to dirty ' + unit_id)
    
def assign_unit(reservation_id):
    try:
        unit = assign_unit_call(old_token, reservation_id)
    except:
        unit = assign_unit_call(new_token, reservation_id)
        print ('Used a new token')

assign_unit('NRYPWBDD-1')