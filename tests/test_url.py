import requests

# Replace with your actual Render URL
url = "https://housing-price-api-ruxm.onrender.com/predict"

# The features for the house you want to price
house_data = {
    "MedInc": 8.3252,   # Median Income in block
    "AveRooms": 6.9841, # Average rooms
    "AveOccup": 2.5555  # Average house occupancy
}

# Send the POST request
response = requests.post(url, json=house_data)

# Print the result
if response.status_code == 200:
    print("Success!")
    print(response.json())
else:
    print("Error:", response.text)