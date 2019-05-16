import SegmentCharacters
import TrainRecognizeCharacters
from refine import template_match,fraction_match
import pickle
print("Loading model")
filename = './finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

print('Model loaded. Predicting characters of number plate')
classification_result = []
for each_character in SegmentCharacters.characters:
    # converts it to a 1D array
    each_character = each_character.reshape(1, -1);
    result = model.predict(each_character)
    classification_result.append(result)

print('Classification result')
print(classification_result)

plate_string = ''
for eachPredict in classification_result:
    plate_string += eachPredict[0]

print('Predicted license plate')
print(plate_string)

# it's possible the characters are wrongly arranged
# since that's a possibility, the column_list will be
# used to sort the letters in the right order

column_list_copy = SegmentCharacters.column_list[:]
SegmentCharacters.column_list.sort()
rightplate_string = ''
for each in SegmentCharacters.column_list:
    rightplate_string += plate_string[column_list_copy.index(each)]

print('License plate')
print(rightplate_string)

import requests
import json


ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
print(my_ip)
lat1=28.5205
lng1=77.2015

lat2=28.7040
lng2=77.1311

lat3=28.6697
lng3=77.1471

geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()
lat=lat3
lng=lng3
print(geo_data)
'''
import geocoder
g = geocoder.ip('me')
lat = g.latlng[0]
lng = g.latlng[1]
print(lat,lng)
'''
import json
import datetime

now = datetime.datetime.now()
dati = now.strftime("%Y-%m-%d %H:%M")
time = dati.split(' ')[-1]
date = dati.split(' ')[0]

x = {
  "Number Plate Number": rightplate_string,
  "Latitude": lat,
  "Longitude": lng,
  "Date": date,
  "Time": time
}

y = json.dumps(x)

with open("./model_results/result1.JSON","w") as f:
    f.write(y)
from firebase import firebase

firebase = firebase.FirebaseApplication('https://hack-bpit.firebaseio.com/')
result = firebase.post("/latlong", x)
result1=firebase.get('https://hack-bpit.firebaseio.com/latlong','Longitude')
print(result1)

'''
 print(TrainRecognizeCharacters.image_data)
 for label in rightplate_string.split():
    fraction_match(label,TrainRecognizeCharacters.image_data,TrainRecognizeCharacters.training_dataset_dir)
'''