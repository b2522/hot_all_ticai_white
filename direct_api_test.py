import requests

# Test the time-sharing data API directly
print("Testing Flask API endpoint...")
try:
    # Test with a valid stock code
    response = requests.get('http://127.0.0.1:5000/api/time-sharing-data?code=300593', timeout=10)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("API response received successfully")
        
        # Check if the expected fields are present
        if 'data' in data:
            if 'preClose' in data['data']:
                print(f"preClose: {data['data']['preClose']}")
            else:
                print("ERROR: preClose field missing")
                print(f"Available fields in data: {list(data['data'].keys())}")
        
        # Print the structure of the response
        print(f"Response structure: {list(data.keys())}")
    else:
        print(f"ERROR: API returned status code {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"Exception occurred: {e}")
