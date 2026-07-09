import requests

def get_weather_summary(city="New Delhi"):
    print(f"[+] Initializing live REST API metrics request for location: {city}")
    # Using open-meteo free API (No authentication key required)
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        geo_res = requests.get(geocoding_url, timeout=10).json()
        if not geo_res.get("results"):
            print("[!] Location coordinates mapping failed.")
            return
            
        location = geo_res["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url, timeout=10).json()
        current = weather_data["current_weather"]
        
        print("\n[✓] Live Atmospheric Environment Summary:\n" + "="*40)
        print(f"Location Target : {location['name']}, {location.get('country', '')}")
        print(f"Core Temperature: {current['temperature']}°C")
        print(f"Wind Velocity   : {current['windspeed']} km/h")
    except Exception as error:
        print(f"[X] Internal data stream mapping exception: {error}")

if __name__ == "__main__":
    get_weather_summary()