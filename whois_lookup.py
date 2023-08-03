from whois import query
from whois.exceptions import FailedParsingWhoisOutput, UnknownTld, WhoisCommandFailed


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
        except WhoisCommandFailed:
            print("Something went wrong while getting WHOIS info. Check your internet connection.")
            exit(1)

        # Checking if the query result is not empty
        if domain_info is None:
            print("Something went wrong while getting WHOIS info. Check your domain")
            exit(1)

        if domain_info.name != '':
            print(f"Name: {domain_info.name}")
        if domain_info.tld != '':
            print(f"TLD: {domain_info.tld}")
        if domain_info.registrar != '':
            print(f"Registrar: {domain_info.registrar}")
        if domain_info.registrant_country != '':
            print(f"Registrant Country: {domain_info.registrant_country}")

        # Format day.month.year
        if domain_info.creation_date is not None:
            print(f"Creation date: {domain_info.creation_date.strftime('%d.%m.%Y')}")
        if domain_info.expiration_date is not None:
            print(f"Expiration date: {domain_info.expiration_date.strftime('%d.%m.%Y')}")
        if domain_info.last_updated is not None:
            print(f"Last updated: {domain_info.last_updated.strftime('%d.%m.%Y')}")

        if domain_info.status != '':
            print(f"Status: {domain_info.status}")
        if domain_info.statuses != ['']:
            print(f"Statuses: {' '.join(domain_info.statuses)}")
        if domain_info.dnssec != '':
            print(f"DNSSEC: {domain_info.dnssec}")
        if domain_info.name_servers != ['']:
            print(f"Name servers: {' '.join(domain_info.name_servers)}")
        if domain_info.registrant != '':
            print(f"Registrant: {domain_info.registrant}")
        if domain_info.emails != ['']:
            print(f"Emails: {' '.join(domain_info.emails)}")


if __name__ == "__main__":
    Whois()
