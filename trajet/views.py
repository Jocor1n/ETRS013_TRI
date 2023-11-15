from django.shortcuts import render
from django.http import HttpResponse
from zeep import Client
import pandas as pd
import requests
import math
import os
from django.conf import settings
from .forms import Calculer, Trajet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Rayon de la Terre en kilomètres

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2)**2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


def do_request(lattitude=46.2276, longitude=2.2137):
    base_url = "https://api.openchargemap.io/v3/poi/"
    parameters = {
    "countrycode": "FR",  # For France
    "latitude": lattitude,
    "longitude": longitude,
    "distance": 100,
    "output": "json",
    "maxresults": 10,  # You might want to increase this if allowed
    "key": settings.OPENCHARGEMAP
    }

    response = requests.get(base_url, params=parameters)
    data = response.json()
    
    locations = [(item["AddressInfo"]["Latitude"], item["AddressInfo"]["Longitude"], item["AddressInfo"]["Town"], item["AddressInfo"]["StateOrProvince"]) for item in data]
    return locations

file_path = os.path.join(settings.BASE_DIR, 'trajet', 'cities.csv')
df = pd.read_csv(file_path)

def List_Vehicules():

   #   headers = {
   #   "x-client-id": settings.API_KEY_OpenChargeMap,
   #   "x-app-id": settings.API_KEY_APP_ID,
   #   "Content-Type": "application/json",
   #   }

   #   query = """
   #   query {
   # vehicleList(page: 0, size: 8) {
   #   id
   #   naming {
   #     make
   #     model
   #     chargetrip_version
   #   }
   #   media {
   #     image {
   #       thumbnail_url
   #     }
   #   }
   #   range {
   #       chargetrip_range {
   #           best
   #           worst
   #           }
        
   #       }
   #   connectors{
   #       time
   #       }
   #   }
   # }
   #   """

   #   response = requests.post("https://api.chargetrip.io/graphql", headers=headers, json={"query": query})
    data = {'data': {'vehicleList': [{'id': '646ca73f3f6beb1fcbdbdf70', 'naming': {'make': 'Abarth', 'model': '500e', 'chargetrip_version': 'Convertible'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/646cad69aaf5a9205eafdd1a-e09bde673cfb63561b9f0e35a2be489f30839a3e.png'}}, 'range': {'chargetrip_range': {'best': 242, 'worst': 207}}, 'connectors': [{'time': 255}, {'time': 25}]}, {'id': '646ca7235452611fc99432b0', 'naming': {'make': 'Abarth', 'model': '500e', 'chargetrip_version': 'Hatchback'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/646cad57090bbf205ced291b-188880bbb3365522700ed0b30bcabd14e9aa825b.png'}}, 'range': {'chargetrip_range': {'best': 238, 'worst': 204}}, 'connectors': [{'time': 255}, {'time': 25}]}, {'id': '638157687592b0f2c57fc08f', 'naming': {'make': 'Abarth', 'model': '500e', 'chargetrip_version': 'Scorpionissima'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/6385be4b150257d93e72d848-f0e2178714a873acb2f18d8301694359e3b53ab1.png'}}, 'range': {'chargetrip_range': {'best': 208, 'worst': 179}}, 'connectors': [{'time': 255}, {'time': 25}]}, {'id': '5f043da2bc262f1627fc0333', 'naming': {'make': 'Aiways', 'model': 'U5', 'chargetrip_version': '63 kWh (2020 - 2022)'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/642d1f78b401be28fae31ff4-b23533754d1063ca7c975f9edaf6b3265f2e4b33.png'}}, 'range': {'chargetrip_range': {'best': 354, 'worst': 304}}, 'connectors': [{'time': 645}, {'time': 34}]}, {'id': '6261f0371b50697eb77bf4cd', 'naming': {'make': 'Aiways', 'model': 'U5', 'chargetrip_version': '63 kWh (early 2022)'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/627492cbbf2e2c73dbc9bf72-052a1ecdf9acd75a9644a3737630bb9196c10585.png'}}, 'range': {'chargetrip_range': {'best': 354, 'worst': 304}}, 'connectors': [{'time': 390}, {'time': 34}]}, {'id': '635332c66aa59107aeace234', 'naming': {'make': 'Aiways', 'model': 'U6', 'chargetrip_version': '63 kWh'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/63d93846baca136bd3582486-fad61a614ce2f6087cb83650e516097813bc8bf6.png'}}, 'range': {'chargetrip_range': {'best': 367, 'worst': 315}}, 'connectors': [{'time': 390}, {'time': 34}]}, {'id': '6454c68da1f0fa1f0c5b6a17', 'naming': {'make': 'Alfa Romeo', 'model': 'Tonale', 'chargetrip_version': '1.3T Plug-In Hybrid Q4 '}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/645d368ac4654ce2d6e7f0cc-f116632b2a41b7a18a84c934afca9d5c5eacbc25.png'}}, 'range': {'chargetrip_range': {'best': 59, 'worst': 51}}, 'connectors': [{'time': 120}]}, {'id': '63b4174d179de8267cf6d6e3', 'naming': {'make': 'Audi', 'model': 'A3 Sportback', 'chargetrip_version': '40 TFSI e'}, 'media': {'image': {'thumbnail_url': 'https://cars.chargetrip.io/63bd20e48c96922417998c4e-983f314abfa1b2db2f2bd450c94cd35f6e26ec40.png'}}, 'range': {'chargetrip_range': {'best': 65, 'worst': 56}}, 'connectors': [{'time': 210}]}]}}
     # if response.status_code == 200:
         # data = response.json()
         # print(data)
    vehicles = data["data"]["vehicleList"]
    Liste_vehicules = []
    for vehicle in vehicles :
      info = {'marque':vehicle["naming"]["make"]}
      info.update({'modele':vehicle["naming"]["model"]})
      info.update({'VersionRechargement':vehicle["naming"]["chargetrip_version"]})
      info.update({'ImageDuVehicule' : vehicle["media"]["image"]["thumbnail_url"]})
      info.update({'AutonomieMax' :vehicle["range"]["chargetrip_range"]["best"]})
      info.update({'AutonomieMin' :vehicle["range"]["chargetrip_range"]["worst"]})
      info.update({'time' :vehicle["connectors"][0]["time"]})
      try:
          info.update({'time2' :vehicle["connectors"][1]["time"]})
      except IndexError:
          info.update({'time2' :None})
      Liste_vehicules.append(info)
    # else:
    #     print(f"Erreur: {response.status_code} - {response.text}")
    return Liste_vehicules

@login_required
def index(request):
    
   markers = []
   Resultat = ""
   index_of_min_distance = ""
   Autonomie, TempsDeRechargement  = 0, 0
   #locations = do_request() 
   locations=[(48.8566,2.3522,"Paris","Ile-De-France")]
   Liste_vehicules = List_Vehicules();
   if request.method == "POST" and 'calculer' in request.POST: 
       form = Calculer(request.POST)
       if form.is_valid() :
           DistanceKM = form.cleaned_data['DistanceKM']
           DistanceMetre = form.cleaned_data['DistanceMetre']
           vitesse = form.cleaned_data['vitesse']
           autonomie = form.cleaned_data['autonomie']
           TempsDeChargementHeures = form.cleaned_data['TempsDeChargementHeures']
           TempsDeChargementMinutes = form.cleaned_data['TempsDeChargementMinutes']
           client = Client('http://127.0.0.1:8001/?wsdl')
           Resultat = client.service.addition(DistanceKM ,DistanceMetre, vitesse, autonomie, TempsDeChargementHeures, TempsDeChargementMinutes)
       
       # affichage = f'Pour un trajet de {distance} km à la vitesse de {vitesse} km/h, avec une autonomie de {autonomie} km avec un temps de chargement de {TempsDeChargement} minutes, le temps de trajet sera de {Resultat}'
   if request.method == "POST" and 'sauvegarder' in request.POST: 
      form = Trajet(request.POST)
      if form.is_valid():
          VilleDepart = form.cleaned_data['VilleDepart']
          VilleArrivee = form.cleaned_data['VilleArrivee']
          Autonomie = form.cleaned_data["Autonomie"]
          TempsDeRechargement = form.cleaned_data["TempsDeRechargement"]
          if int(TempsDeRechargement) == 0:
              TempsDeRechargement = form.cleaned_data["TempsDeRechargement2"]
          latitudeDepart = df.loc[df['label'] == VilleDepart, 'latitude'].values[0]
          longitudeDepart = df.loc[df['label'] == VilleDepart, 'longitude'].values[0]
          latitudeArrivee = df.loc[df['label'] == VilleArrivee, 'latitude'].values[0]
          longitudeArrivee = df.loc[df['label'] == VilleArrivee, 'longitude'].values[0]
          latitude_moyenne = (latitudeDepart + latitudeArrivee) / 2
          longitude_moyenne = (longitudeDepart + longitudeArrivee) / 2
          #locations = do_request(latitude_moyenne,longitude_moyenne)
          
          markers=[(latitudeDepart,longitudeDepart,VilleDepart),(latitudeArrivee,longitudeArrivee,VilleArrivee)]
          
          distances = [haversine_distance(latitudeDepart, longitudeDepart, lat, lon) for lat, lon, distance, state in locations]
          min_distance = min(distances)
          index_of_min_distance = distances.index(min_distance)
      else:
          print(form.errors)
          
   return render(request, 'input.html', {'labels':df["label"].tolist(), 'markers':markers, 'result':Resultat, 'locations':locations, 'index_of_min_distance':index_of_min_distance, 'Liste_vehicules':Liste_vehicules, 'data': 0, 'Autonomie': Autonomie, 'Autonomie_5' : Autonomie/5, 'TempsDeRechargement':TempsDeRechargement, 'OPENCHARGEMAP': settings.OPENCHARGEMAP})