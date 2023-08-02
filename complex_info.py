from socket import gethostbyname, gaierror
from requests import get
from requests.exceptions import ConnectionError
from whois_lookup import Whois
from dns_records import DnsRecords


class ComplexInfo:
    def __init__(self) -> None:
        """Init method. Gets ip/domain"""
        address = input("IP/Domain: ")
        self.get_complex_info(address)


    @staticmethod
    def _is_domain(address: str) -> bool:
        return not address.replace('.', '').isnumeric()

    def get_complex_info(self, address: str) -> None:
        """Print complex ip/domain info.
        If domain doesn't have a website shows only WHOIS and DNS records
        If there is website on domain shows WHOIS, DNS records and IP info"""
        if self._is_domain(address):
            try:
                ip = gethostbyname(address)
            except gaierror:
                print("That domain doesn't have a website.")
                print('=' * 16, "WHOIS", '=' * 16)
                Whois.whois_handler(address)
                print('=' * 16, "All DNS Records", '=' * 16)
                DnsRecords.get_all_records(address)
                print('=' * 32)
                exit(0)
        else:
            ip = address

        try:
            print('=' * 16, "IP Info", '=' * 16)
            data = get(f"https://ipapi.co/{ip}/json/").json()
            print(f"IP: {data['ip']}")
            print(f"Version: {data['version']}")
            print(f"City: {data['city']}")
            print(f"Region: {data['region']}")
            print(f"Region code: {data['region_code']}")
            print(f"Country code: {data['country_code']}")
            print(f"Country name: {data['country_name']}")
            print(f"Country TLD: {data['country_tld']}")
            print(f"In EU: {data['in_eu']}")
            print(f"Postal code: {data['postal']}")
            print(f"Latitude: {data['latitude']}")
            print(f"Longitude: {data['longitude']}")
            print(f"Timezone: {data['timezone']}")
            print(f"ASN: {data['asn']}")
            print(f"Organization: {data['org']}")
        except ConnectionError:
            print("An error occurred. Please check your internet connection.")
            exit(1)
        except KeyError as e:
            print("Some entry does not exist.", e)

        if self._is_domain(address):
            print('=' * 16, "WHOIS", '=' * 16)
            Whois.whois_handler(address)
            print('=' * 16, "All DNS Records", '=' * 16)
            DnsRecords.get_all_records(address)

        print('=' * 32)


if __name__ == "__main__":
    ComplexInfo()
