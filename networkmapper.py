from nmap import PortScanner


class NetworkMapper:
    def __init__(self) -> None:
        """Creates nmap.PortScanner()
        Starts menu"""
        self.nmap_menu = "[1] - Scan all ports (with info about services)\n" \
                         "[2] - Scan ports from 1 to 1024\n" \
                         "[3] - Scan custom range of ports\n" \
                         "[4] - Scan one specific port\n" \
                         "[0] - Return to main menu"
        self.nm = PortScanner()
        self.menu()

    def _handle_nmap_output(self, ip: str) -> None:
        """Handles nmap output of given ip.
        Shows protocol, state, open ports, ip, info about port"""
        try:
            for protocol in self.nm[ip].all_protocols():
                print("=" * 32)
                print("Protocol:", protocol)
                print("State:", self.nm[ip].state())
                ports = sorted(self.nm[ip][protocol].keys())
                host = self.nm[ip][protocol]
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
            print("=" * 32)
        except KeyError:
            print("An error occurred. May be problem in internet connection?")
            exit(1)

    def _scan_all_ports(self, ip: str) -> None:
        """Scans all ports of given ip"""
        self.nm.scan(ip)
        self._handle_nmap_output(ip)

    def _scan_ports_from_1_to_1024(self, ip: str) -> None:
        """Scans ports from 1 to 1024 of given ip"""
        self.nm.scan(ip, "1-1024")
        self._handle_nmap_output(ip)

    def _scan_custom_range_of_ports(self, ip: str, start_port: str, end_port: str) -> None:
        """Scans custom range of ports of given ip"""
        self.nm.scan(ip, f"{start_port}-{end_port}")
        self._handle_nmap_output(ip)

    def _scan_one_port(self, ip: str, port: str) -> None:
        """Scans one port of given ip"""
        self.nm.scan(ip, port)
        self._handle_nmap_output(ip)

    def menu(self) -> None:
        """Shows menu and handles user input"""
        print(self.nmap_menu)

        choice = input("> ")

        ip = input("IP: ")

        match choice:
            case "1":
                self._scan_all_ports(ip)
            case "2":
                self._scan_ports_from_1_to_1024(ip)
            case "3":
                start_port = input("Start port: ")
                end_port = input("End port: ")
                self._scan_custom_range_of_ports(ip, start_port, end_port)
            case "4":
                port = input("Port: ")
                self._scan_one_port(ip, port)
            case "0":
                pass


if __name__ == "__main__":
    NetworkMapper()
