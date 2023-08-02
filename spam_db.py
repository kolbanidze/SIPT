from os import getenv
from dotenv import load_dotenv, set_key
import requests


class SpamDB:
    def __init__(self):
        self.get_api_key()
        self.get_spam_info()

    @staticmethod
    def get_api_key() -> None:
        # Getting API key

        if load_dotenv():
            if getenv('API') is None:
                print(
                    "You need to register at https://abuseipdb.com and get free API key. Then enter it here and it will "
                    "be automatically saved")
                api_key = input("API Key: ")
                set_key('.env', 'API', api_key)
                load_dotenv()
        else:
            print("You need to register at https://abuseipdb.com and get free API key. Then enter it here and it will "
                  "be automatically saved")
            api_key = input("API Key: ")
            set_key('.env', 'API', api_key)
            load_dotenv()

    @staticmethod
    def get_spam_info() -> None:
        url = 'https://api.abuseipdb.com/api/v2/check'
        api = getenv('API')

        ip = input("IP: ")
        querystring = {
            'ipAddress': f'{ip}',
            'maxAgeInDays': '180'
        }
        headers = {
            'Accept': 'application/json',
            'Key': f'{api}'
        }
        try:
            response = requests.request(method='GET', url=url, headers=headers, params=querystring)
            data = response.json()['data']
        except Exception as e:
            print("Error. Check your ip and internet connection.")
            # print(f"API Answer: {response.json()}")
            print("Error:", e)
            exit(1)

        print(f"IP: {data['ipAddress']}")
        print(f"Is Public: {data['isPublic']}")
        print(f"IP Version: {data['ipVersion']}")
        print(f"Is Whitelisted: {data['isWhitelisted']}")
        print(f"Abuse Confidence Score: {data['abuseConfidenceScore']}%")
        print(f"Country Code: {data['countryCode']}")
        print(f"Usage Type: {data['usageType']}")
        print(f"ISP: {data['isp']}")
        print(f"Domain {data['domain']}")
        print(f"Hostnames: {' '.join(data['hostnames'])}")
        print(f"Is Tor: {data['isTor']}")
        print(f"Total amount of reports: {data['totalReports']}")
        print(f"Number of distinct users: {data['numDistinctUsers']}")
        print(f"Last reported at: {data['lastReportedAt']}")


if __name__ == "__main__":
    SpamDB()
