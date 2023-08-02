import dns.resolver
from dns.resolver import Resolver
from settings import DNS_RECORDS_LOG_FILE, DEFAULT_DNS_RESOLVER


class DnsRecords:
    def __init__(self) -> None:
        # Setting up DNS Resolver
        default_resolver = Resolver(configure=False)
        dns_provider_choice = input("Enter DNS resolver (0 - default (cloudflare), 1 - custom): ")
        match dns_provider_choice:
            case "0":
                default_resolver.nameservers = DEFAULT_DNS_RESOLVER
            case "1":
                dns_nameservers = []
                while True:
                    dns_nameserver = input("Enter DNS nameserver (0 - when done): ")
                    if dns_nameserver == "0":
                        default_resolver.nameservers = dns_nameservers
                        break
                    else:
                        dns_nameservers.append(dns_nameserver)

        # Domain
        domain = input("Domain: ")
        self.get_all_records(domain)

    @staticmethod
    def get_all_records(domain: str) -> None:
        dns_records_types = [
            'A', 'AAAA', 'CAA', 'CERT', 'CNAME', 'DNSKEY', 'DS',
            'HTTPS', 'LOC', 'MX', 'NAPTR', 'NS', 'PTR', 'SMIMEA',
            'SRV', 'SSHFP', 'SVCB', 'TLSA', 'TXT', 'URI'
        ]
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
            file.write('=' * 64 + '\n')
        print(f"Non-existent DNS records were written into {DNS_RECORDS_LOG_FILE}")


if __name__ == "__main__":
    DnsRecords()
