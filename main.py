import nmap
import whois
import dns.resolver
import requests
import socket
import os
from dotenv import load_dotenv

DNS_RECORDS_LOG_FILE = "dns_log.txt"

def start_nmap():
    def _scan_ports(scanallports=False, scan1024ports=False, scancustomrangeofports=False, scanoneport=False):
        ip = input("IP: ")
        if scanallports:
            print("Please wait while nmap is scanning ports")
            nm.scan(ip)
        elif scan1024ports:
            print("Please wait while nmap is scanning ports")
            nm.scan(ip, "1-1024")
        elif scancustomrangeofports:
            start_port = input("Start: ")
            end_port = input("End: ")
            print("Please wait while nmap is scanning ports")
            nm.scan(ip, f"{start_port}-{end_port}")
        elif scanoneport:
            port = input("Port: ")
            print("Please wait while nmap is scanning ports")
            nm.scan(ip, f"{port}")
        else:
            print("You must specify scan mode")
            exit(1)

        for protocol in nm[ip].all_protocols():
            print("-" * 32)
            print("Protocol:", protocol)
            print("State:", nm[ip].state())

            ports = sorted(nm[ip][protocol].keys())
            host = nm[ip][protocol]
            for port in ports:
                if host[port]['state'] == 'open':
                    print(f"Port: {port}"
                          f"\n\tState: {host[port]['state']}"
                          f"\n\tReason: {host[port]['reason']}"
                          f"\n\tName: {host[port]['name']}"
                          f"\n\tProduct: {host[port]['product']}"
                          f"\n\tVersion: {host[port]['version']}"
                          f"\n\tExtra info: {host[port]['extrainfo']}"
                          f"\n\tCPE: {host[port]['cpe']}")
        start_nmap()
    print(nmap_menu)
    try:
        choice = int(input("> "))
    except ValueError:
        print("You need to type only number. Try again")
        exit(1)

    nm = nmap.PortScanner()

    match choice:
        case 1:
            _scan_ports(scanallports=True)
        case 2:
            _scan_ports(scan1024ports=True)
        case 3:
            _scan_ports(scancustomrangeofports=True)
        case 4:
            _scan_ports(scanoneport=True)
        case 99:
            entry()

def start_whois(no_domain_entry=False, domain="example.com"):
    if not no_domain_entry:
        domain = input("Domain: ")
    domain_info = whois.query(domain)
    print("-"*32)
    print(f"Name: {domain_info.name}")
    print(f"TLD: {domain_info.tld}")
    print(f"Registrar: {domain_info.registrar}")
    print(f"Registrant Country: {domain_info.registrant_country}")
    # Format day.month.year
    print(f"Creation date: {domain_info.creation_date.strftime('%d.%m.%Y')}")
    print(f"Expiration date: {domain_info.expiration_date.strftime('%d.%m.%Y')}")
    print(f"Last updated: {domain_info.last_updated.strftime('%d.%m.%Y')}")
    print(f"Status: {domain_info.status}")
    print(f"Statuses: {' '.join(domain_info.statuses)}")
    print(f"DNSSEC: {domain_info.dnssec}")
    print(f"Name servers: {' '.join(domain_info.name_servers)}")
    print(f"Registrant: {domain_info.registrant}")
    print(f"Emails: {' '.join(domain_info.emails)}")
    entry()

def dns_records_info(no_domain_entry=False, domain="example.com"):
    if not no_domain_entry:
        domain = input("Domain: ")
    dns_records_types = [
        'A', 'AAAA', 'CAA', 'CERT', 'CNAME', 'DNSKEY', 'DS',
        'HTTPS', 'LOC', 'MX', 'NAPTR', 'NS', 'PTR', 'SMIMEA',
        'SRV', 'SSHFP', 'SVCB', 'TLSA', 'TXT', 'URI'
    ]

    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    # Cloudflare Public DNS
    dns.resolver.default_resolver.nameservers = ['1.1.1.1', '1.0.0.1', '2606:4700:4700::1111', '2606:4700:4700::1001']
    for record in dns_records_types:
        try:
            query_answer = dns.resolver.resolve(domain, record)
            for data in query_answer:
                print(f"Record: {record}\n\t{data}")
        # Logging non-existent dns records
        except Exception as e:
            with open(DNS_RECORDS_LOG_FILE, 'a+') as file:
                file.write(f"{e}\n")
    with open(DNS_RECORDS_LOG_FILE, 'a') as file:
        file.write('-'*64+'\n')
    print(f"Non-existent DNS records were written into {DNS_RECORDS_LOG_FILE}")
    entry()

def complex_ip_info():
    def _is_domain(address):
        return not address.replace('.', '').isnumeric()

    address = input("IP/Domain: ")
    if _is_domain(address):
        try:
            ip = socket.gethostbyname(address)
        except socket.gaierror:
            print("That domain doesn't have a website.")
            exit(1)
    else:
        # In case if input address is ip
        ip = address

    data = requests.get(f"https://ipapi.co/{ip}/json/").json()
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

    if _is_domain(address):
        print('-' * 32)
        print("WHOIS Info:")
        start_whois(no_domain_entry=True, domain=address)

        print('-'*32)
        print("All DNS records:")
        dns_records_info(no_domain_entry=True, domain=address)

    entry()


def spam_db_check():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print("You need to register at https://abuseipdb.com and get free API key. Then enter it here and it will"
              " be automatically saved")
        api_key = input("API Key: ")
        with open('.env', 'w') as file:
            file.write(f"API={api_key}")
        exit(0)

    url = 'https://api.abuseipdb.com/api/v2/check'
    api = os.getenv('API')

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
    except KeyError:
        print("Error. Did you entered correct ip?")
        print(f"API Answer: {response.json()}")
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
    entry()


nmap_menu = """
[1] - Scan all ports (with info about services)
[2] - Scan ports from 1 to 1024
[3] - Scan custom range of ports
[4] - Scan one specific port
[99] - Return to main menu"""

main_menu = """
[1] - Nmap
[2] - Whois
[3] - DNS Records Info
[4] - Complex IP/domain info
[5] - Spam DB Check (Free API key required)
[99] - Exit"""

def entry():
    print(main_menu)
    try:
        choice = int(input("> "))
    except ValueError:
        print("You need to type only number. Try again")
        exit(1)

    match choice:
        case 1:
            start_nmap()
        case 2:
            start_whois()
        case 3:
            dns_records_info()
        case 4:
            complex_ip_info()
        case 5:
            spam_db_check()
        case 99:
            exit(0)

if __name__ == "__main__":
    entry()
