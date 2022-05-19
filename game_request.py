import requests
headers = { 
    'TRN-api-key': 'd24c19bf-7b49-480b-9aa9-3752c5016253' #this is where we pass the headers
}
r = requests.get('https://api.fortnitetracker.com/v1/store', headers=headers) # This is where we call the API
print(r.json())