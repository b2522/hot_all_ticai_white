import requests

print("Checking Flask server status...")
try:
    response = requests.get('http://127.0.0.1:5000/api/time-sharing-data?code=300593', timeout=5)
    print(f"Status code: {response.status_code}")
    print(f"API available: {response.status_code == 200}")
    if response.status_code == 200:
        print("Flask server is running correctly!")
    else:
        print("Flask server returned an error status.")
except Exception as e:
    print(f"Error: {e}")
    print("Flask server is not running or not accessible.")
