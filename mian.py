import configparser
import os
import cloudflare
import requests


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
    config.set("DNSDeets","DNSRecordID","changeThis")
    config.set("DNSDeets", "zoneID","ChangeThis")
    config.set("DNSDeets","domainName","cookiecamp.org")
    config.add_section("debug")
    config.set("debug","ipv4_Service", "http://ipinfo.io/ip")
    config.write(cfgfile)
    cfgfile.close()


configur = configparser.ConfigParser()
configur.read("CF_DDNS_Config.ini")

email = configur.get("UserInfo","Email")
apiKey = configur.get("UserInfo","ApiKey")
dnsRecordID = configur.get("DNSDeets","DNSRecordID")
zoneID = configur.get("DNSDeets","zoneID")
ipv4Service = configur.get("debug","ipv4_Service")
domainName = configur.get("DNSDeets","domainName")
# print(email)
# print(dnsRecordID)
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
responce = client.dns.records.get(
    dns_record_id=dnsRecordID,
    zone_id=zoneID,
)

endIPindex = str(responce).find(", name=")

fetchedIP = "".join(str(responce).split())[17:endIPindex-1]
print(fetchedIP)
if fetchedIP != ipv4:
    responce = client.dns.records.edit(
        dns_record_id=dnsRecordID,
        zone_id=zoneID,
        type="A",
        name=domainName,
        content=ipv4,
    )

