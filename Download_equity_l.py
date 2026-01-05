import requests



def download_csv(output_path="EQUITY_L.csv"):
    # Target URL
    url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

    # Optional: a nicer User-Agent (some servers block default Python UA)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    # Optional: set a timeout (in seconds)
    timeout = 30
    try:
        with requests.get(url, headers=headers, timeout=timeout, allow_redirects=True) as resp:
            resp.raise_for_status()  # raise HTTPError for bad responses (4xx/5xx)

            # If the server sends binary data, write as binary
            with open(output_path, "wb") as f:
                f.write(resp.content)

        print(f"Downloaded: {output_path}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {getattr(http_err.response, 'text', '')}")
    except requests.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
'''
if __name__ == "__main__":
    download_csv('C:/Users/HP/')  # you can pass a path like download_csv('path/to/EQUITY_L.csv')
'''
