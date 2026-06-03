from pymongo import MongoClient
import requests
import config
import base64
from datetime import datetime, timezone
from geopy.distance import geodesic

# Author: Rory L Groom
# brief- this script is used to request location data from hologram.io and incorporate that data into our MongoDB database
# Right now, the data is being sent to my own personal database, but the data can be easily redirected with a different 
# connection string. 
#
# As of now, this will be stored in a single "location" collection. Will not search and update existing packets in entire database
# however, it will timestamp the last time it was updated, as well as store an array of past locations with their respective 
# timestamps 
#
# 

uri = config.test_mongo_uri
client = MongoClient(uri)


def update_locations():
    #Hologram

    #encode credentials using base64
    encoded_credentials = base64.b64encode(config.credentials.encode('utf-8')).decode('utf-8')
    #create header with hologram creds
    headers = {
    'Authorization': f'Basic {encoded_credentials}'
    }
    response = requests.get(config.hologram_url_location, headers= headers)
    #convert response object to json
    data = response.json()
    #extract useful data from response
    all_devices = data["data"]

    # get rest of paginated data. Stores data we want to use in variable all_devices
    while(data["continues"]):
        new_request = requests.get(f'https://dashboard.hologram.io{data["links"]["next"]}', headers= headers)
        data = new_request.json()
        all_devices.extend(data["data"])

    # filters list to only include devices with valid locations. When hologram sends out packets without location info, 
    # long and lat will be empty strings. Turns list into lookup table
    clean_devices = []
    for device in all_devices:
        if device["latitude"] and device["longitude"]:
            clean_devices.append(device)
    
    collection = client.get_collection("Device_Test")

    #turn database into lookup table
    mongo_locations = {}
    for device in collection.find({}):
        mongo_locations[device["deviceid"]] = device
        
    # used for output message
    number_updated = 0
    # variable decides if we need to insert new documents in mongoDB
    new_locations = False
    # stores new entries, bulk inserts new locations to mongo
    new_location_docs = []
    
    # compare locations from hologram response to existing mongoDB locations
    for clean_device in clean_devices:
        device_id = clean_device["deviceid"]
        # if current hologram packet device id is in lookup table
        if device_id in mongo_locations:
            matching_doc = mongo_locations[device_id]

            # calculate the distance between the old and the new locations. If the distance is greater than the range specified by hologram, then update. 
            # otherwise, keep the location the same. Helps reduce redundancy and saves space in MongoDB
            old = (matching_doc["latitude"], matching_doc["longitude"])
            new = (clean_device["latitude"], clean_device["longitude"])
            distance_apart = geodesic(old,new).meters

            if distance_apart > clean_device["range"]:
                query = {"deviceid": device_id}
                # update operation, will update 
                update_operation = {
                    "$set": {"latitude": clean_device["latitude"], "longitude": clean_device["longitude"],
                            "Last Updated (UTC)": datetime.now(timezone.utc)},
                    "$push": {"Previous Locations": {"latitude": matching_doc["latitude"], "longitude": matching_doc["longitude"],
                                                     "timestamp": matching_doc["Last Updated (UTC)"]} }
                }
                collection.update_one(query, update_operation)
                number_updated += 1

        else:
            new_locations = True
            clean_device["Last Updated (UTC)"] = datetime.now(timezone.utc)
            clean_device["Previous Locations"] = []
            new_location_docs.append(clean_device)

    if new_locations:
        result = collection.insert_many(new_location_docs)
        print("Created", len(result.inserted_ids), "new documents")
    else:
        print("No new documents")

            

    if number_updated == 0:
        print("No updated locations")
    elif number_updated == 1:
        print("Updated ", number_updated, " device location")
    else:
        print("Updated ", number_updated, " device locations")


except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)
