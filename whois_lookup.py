from whois import query
from whois.exceptions import FailedParsingWhoisOutput, UnknownTld


class Whois:
    def __init__(self) -> None:
        domain = input("Domain: ")
        self.whois_handler(domain)

    @staticmethod
    def whois_handler(domain: str) -> None:
        try:
            domain_info = query(domain)
        except FailedParsingWhoisOutput:
            print("Domain does not exist.")
            exit(1)
        except UnknownTld:
            print("Unknown TLD")
            exit(1)

        try:
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
        except AttributeError as e:
            print("Some entry does not exist.", e)


if __name__ == "__main__":
    Whois()
