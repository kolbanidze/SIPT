from os import getenv
from dotenv import load_dotenv, set_key
from requests import request
from requests.exceptions import ConnectionError


class SpamDB:
    def __init__(self) -> None:
        self.get_api_key()
        ip = input("IP: ")
        self.get_spam_info(ip)

    @staticmethod
    def get_api_key() -> None:
        """Gets API key from dotenv (.env)"""
        # Getting API key

        if load_dotenv():
            if getenv('API') is None:
                print(
                    "You need to register at https://abuseipdb.com and get free API key. "
                    "Then enter it here and it will be automatically saved")
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
    def get_spam_info(ip: str) -> None:
        """Gets spam info about ip using abuseipdb api v2.
        Prints all available info about ip and handles errors"""
        url = 'https://api.abuseipdb.com/api/v2/check'
        api = getenv('API')

        querystring = {
            'ipAddress': f'{ip}',
            'maxAgeInDays': '180'
        }
        headers = {
            'Accept': 'application/json',
            'Key': f'{api}'
        }

        try:
            response = request(method='GET', url=url, headers=headers, params=querystring).json()
        except ConnectionError:
            print("Connection Error. Please check your internet connection.")
            exit(1)

        if response.get('errors') is not None:
            print("Error", response['errors'][0]['detail'])
            exit(1)

        data = response['data']

        print('='*32)
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
        print('='*32)


if __name__ == "__main__":
    SpamDB()
