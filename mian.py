import configparser
import os
import cloudflare
import requests

import socket

def get_ipv6_address():

    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
        s.connect(('2001:4860:4860::8888', 80)) # Google's public DNS IPv6 address
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()
configfile_name = "CF_DDNS_Config.ini"
# Check if there is already a configurtion file
if not(os.path.isfile(configfile_name)):
    # Create the configuration file as it doesn't exist yet
    cfgfile = open(configfile_name, "w")

    # Add content to the file
    config = configparser.ConfigParser()
    config.add_section("UserInfo")
    config.set("UserInfo", "Email", "example@google.com")
    config.set("UserInfo","ApiKey","<inputApiKey>")
    config.add_section("DNSDeets")
    config.set("DNSDeets","DNSRecordIDs (separate by commas AAAA record goes first if using IPv6)","changeThis")
    config.set("DNSDeets", "zoneID","ChangeThis")
    config.set("DNSDeets","domainName","cookiecamp.org")
    config.set("DNSDeets","IP version(IPv4, IPv6 or both)","IPv4")
    config.add_section("debug")
    config.set("debug","ipv4_Service", "http://ipinfo.io/ip")
    config.write(cfgfile)
    cfgfile.close()
    exit()


configur = configparser.ConfigParser()
configur.read("CF_DDNS_Config.ini")

email = configur.get("UserInfo","Email")
apiKey = configur.get("UserInfo","ApiKey")
dnsRecordIDs = configur.get("DNSDeets","DNSRecordIDs (separate by commas AAAA record goes first if using IPv6)").split(",")
zoneID = configur.get("DNSDeets","zoneID")
ipv4Service = configur.get("debug","ipv4_Service")
domainName = configur.get("DNSDeets","domainName")
ipVersion = configur.get("DNSDeets","IP version(IPv4, IPv6 or both)")

# gets and sets the IPv6 and AAAA record
if ipVersion == "IPv6" or ipVersion == "both":
    ipv6 = get_ipv6_address()
    if ipv6:
        print("IPv6 address:", ipv6)
    else:
        print("No IPv6 address found.")
    client = cloudflare.Cloudflare(
        api_token=apiKey
    )
    responce = client.dns.records.get(
        dns_record_id=dnsRecordIDs[0],
        zone_id=zoneID,
    )
    endIPindex = str(responce).find(", name=")

    fetchedIP = "".join(str(responce).split())[17:endIPindex-1]
    print(fetchedIP)
    if fetchedIP != ipv6:
        responce = client.dns.records.edit(
            dns_record_id=dnsRecordIDs[0],
            zone_id=zoneID,
            type="AAAA",
            name=domainName,
            content=ipv6,
        )

# gets and sets IPv4 and the A record
if ipVersion == "IPv4" or ipVersion == "both":
    r = requests.get(ipv4Service)
    try:
        ipv4 = r.text
    except:
        print("are you connected to the internet")
        exit()
    print(ipv4)

    client = cloudflare.Cloudflare(
        api_token=apiKey
    )
    if ipVersion == "both":
        responce = client.dns.records.get(
            dns_record_id=dnsRecordIDs[1],
            zone_id=zoneID,
        )

        endIPindex = str(responce).find(", name=")

        fetchedIP = "".join(str(responce).split())[17:endIPindex-1]
        print(fetchedIP)
        if fetchedIP != ipv4:
            responce = client.dns.records.edit(
                dns_record_id=dnsRecordIDs[1],
                zone_id=zoneID,
                type="A",
                name=domainName,
                content=ipv4,
            )
    else:
        responce = client.dns.records.get(
            dns_record_id=dnsRecordIDs[0],
            zone_id=zoneID,
        )

        endIPindex = str(responce).find(", name=")

        fetchedIP = "".join(str(responce).split())[17:endIPindex-1]
        print(fetchedIP)
        if fetchedIP != ipv4:
            responce = client.dns.records.edit(
                dns_record_id=dnsRecordIDs[0],
                zone_id=zoneID,
                type="A",
                name=domainName,
                content=ipv4,
            )
