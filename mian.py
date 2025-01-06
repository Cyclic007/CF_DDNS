import configparser
import os
import cloudflare
import requests
import logging
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
    config.set("DNSDeets","domainName","google.com")
    config.set("DNSDeets","IP version(IPv4, IPv6 or both, will assume ipv4 if empty)","IPv4")
    config.add_section("debug")
    config.set("debug","ipv4_Service", "http://ipinfo.io/ip")
    config.set("debug","log","no")
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
ipVersion = configur.get("DNSDeets","IP version(IPv4, IPv6 or both, will assume ipv4 if empty)")
loging = configur.get("debug","log")
logDir = "logs"
if loging.lower() == "yes":
    if not(os.path.isfile(logDir)):
        os.makedirs(logDir)


    # Create a logger
    logger = logging.getLogger(logDir)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    handler = logging.FileHandler('CFDDNS.log')
    handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # gets and sets the IPv6 and AAAA record
    if ipVersion == "IPv6" or ipVersion == "both":
        ipv6 = get_ipv6_address()
        if ipv6:
            logout = "your ipv6 is "+ str(ipv6)
            logger.info(logout)
        else:
            logger.error("no IPv6 found are you connected to network")
            exit(3)
        client = cloudflare.Cloudflare(
            api_token=apiKey
        )
        responce = client.dns.records.get(
            dns_record_id=dnsRecordIDs[0],
            zone_id=zoneID,
        )
        endIPindex = str(responce).find(", name=")

        fetchedIP = "".join(str(responce).split())[17:endIPindex-1]
        logger.info("your AAAA record IPv6 is "+fetchedIP)

        if fetchedIP != ipv6:
            responce = client.dns.records.edit(
                dns_record_id=dnsRecordIDs[0],
                zone_id=zoneID,
                type="AAAA",
                name=domainName,
                content=ipv6,
            )

    # gets and sets IPv4 and the A record
    if ipVersion == "IPv4" or ipVersion == "both" or ipVersion =="":
        r = requests.get(ipv4Service)
        try:
            ipv4 = r.text
        except:
            logger.error("are you connected to the internet")
            exit(4)
        logger.info("your IPv4 is "+ipv4)

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
            logger.info("your A DNS record contains "+fetchedIP)
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

# gets and sets the IPv6 and AAAA record
if ipVersion == "IPv6" or ipVersion == "both":
    ipv6 = get_ipv6_address()
    if ipv6:
        pass
    else:

        exit(3)
    client = cloudflare.Cloudflare(
        api_token=apiKey
    )
    responce = client.dns.records.get(
        dns_record_id=dnsRecordIDs[0],
        zone_id=zoneID,
    )
    endIPindex = str(responce).find(", name=")

    fetchedIP = "".join(str(responce).split())[17:endIPindex-1]

    if fetchedIP != ipv6:
        responce = client.dns.records.edit(
            dns_record_id=dnsRecordIDs[0],
            zone_id=zoneID,
            type="AAAA",
            name=domainName,
            content=ipv6,
        )

# gets and sets IPv4 and the A record
if ipVersion == "IPv4" or ipVersion == "both" or ipVersion =="":
    r = requests.get(ipv4Service)
    try:
        ipv4 = r.text
    except:
        print("are you connected to the internet")
        exit(4)


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

        if fetchedIP != ipv4:
            responce = client.dns.records.edit(
                dns_record_id=dnsRecordIDs[0],
                zone_id=zoneID,
                type="A",
                name=domainName,
                content=ipv4,
            )
