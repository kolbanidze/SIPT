from networkmapper import NetworkMapper
from whois_lookup import Whois
from dns_records import DnsRecords
from complex_info import ComplexInfo
from spam_db import SpamDB

main_menu = """
[1] - Nmap
[2] - Whois
[3] - DNS Records Info
[4] - Complex IP/domain info
[5] - Spam DB Check (Free API key required)
[0] - Exit"""


def entry() -> None:
    print(main_menu)
    choice = input("> ")

    match choice:
        case "1":
            NetworkMapper()
            entry()
        case "2":
            Whois()
            entry()
        case "3":
            DnsRecords()
            entry()
        case "4":
            ComplexInfo()
            entry()
        case "5":
            SpamDB()
            entry()
        case "0":
            exit(0)


if __name__ == "__main__":
    entry()
