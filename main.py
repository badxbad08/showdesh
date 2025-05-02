import requests
from urllib.parse import parse_qs
import json

def handler(request, response):
    # Log the request query string
    print(f"Request query string: {request.query_string}")

    # Extract query parameters
    query_params = parse_qs(request.query_string)
    country = query_params.get('country', [None])[0]
    
    if not country:
        return response.json({"error": "Missing 'country' query parameter"}, status=400)

    url = "https://otp-api.shelex.dev/api/countries"
    headers = {
        "authority": "otp-api.shelex.dev",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://otp.shelex.dev",
        "referer": "https://otp.shelex.dev/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
    }

    try:
        print(f"Sending request to {url} with headers {headers}")
        # Make the request to fetch country data
        response_data = requests.get(url, headers=headers)
        
        # Log the status code of the response
        print(f"API response status code: {response_data.status_code}")

        if response_data.status_code == 200:
            countries = response_data.json()
            filtered_data = [
                item for item in countries if item.get('country') == country
            ]
            
            if filtered_data:
                return response.json(filtered_data)
            else:
                return response.json({"error": "Country not found"}, status=404)
        else:
            return response.json({"error": "Failed to fetch data from source", "status": response_data.status_code}, status=500)
    except Exception as e:
        # Log the error
        print(f"Error occurred: {str(e)}")
        return response.json({"error": str(e)}, status=500)
