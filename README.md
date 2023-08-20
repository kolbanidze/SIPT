# SIPT: Simple IP Tool

Cross-platform simple ip tools. It is a simple project to automate my routine. 


# Functions

## Network Mapper (nmap)

 - Scan all ports
 - Scan first 1024 ports
 - Scan custom range of ports
 - Scan one specific port
 
 P.S. It will also show all available info about port

## WHOIS

Just getting all info about domain

## DNS Records info

Getting all DNS Records of some domain. 

## Complex IP/Domain Info

It will show website ip info and if was entered domain will show WHOIS info.

## Spam DB Check

It will check if entered IP address is in Spam DB. It uses [AbuseIPDB](https://abuseipdb.com) and to use it you need free api key (need a registration). You need to enter your api key only once, then it will be saved in .env file (in plaintext).

# Libraries & API

For nmap it uses: python-[nmap](https://pypi.org/project/python-nmap/)
For WHOIS it uses: [whois](https://pypi.org/project/whois/)
For getting DNS Records it uses: [dnspython](https://pypi.org/project
/dnspython/)
For getting Complex IP/Domain Info it uses: socket (getting ip from domain), ipapi.co (getting ip info) and [whois](https://pypi.org/project/whois/) (for getting WHOIS info)
For checking in spam db it uses: [AbuseIPDB API (v2)](https://docs.abuseipdb.com/?python#check-endpoint)

# Installation
P.S. you need to add nmap and whois binaries to your path.

Windows: [nmap](https://nmap.org/download.html#windows), [whois](https://learn.microsoft.com/en-us/sysinternals/downloads/whois). 

Linux: depends on your package manager. More likely packages name will be same

For Fedora it is ```sudo dnf install nmap whois```

```
git clone https://github.com/kolbanidze/SIPT
cd SIPT
pip install -r requirements.txt
```

# Usage

```
python main.py
```
or
```
python3 main.py
```
