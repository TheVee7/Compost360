import requests
import matplotlib.pyplot as plt

api_key = "BL366XG71WDZVE3L"
channel_id = "2509864"

entry_id =[]
field_1_temp = []
field_2_moisture = []

# Construct the ThingSpeak Read API endpoint
endpoint = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"

# Parameters for the GET request
params = {'api_key': api_key}  # Example: Retrieve the last 20 entries

# Make a GET request to the ThingSpeak Read API
response = requests.get(endpoint, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    for entry in data["feeds"]:
        field_1_temp.append(entry['field1'])
        field_2_moisture.append(entry['field2'])
        entry_id.append(entry['entry_id'])
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code}")

plt.plot(entry_id,field_1_temp )

plt.xlabel("S.NO")
plt.ylabel("TEMPRATURE")
plt.title("temprature")
plt.show()

plt.plot(entry_id,field_2_moisture)

plt.xlabel("S.NO")
plt.ylabel("MOISTURE")
plt.title("MOISTURE")
plt.show()
