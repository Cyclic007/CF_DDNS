import os
from sys import platform

OS = platform

print(os.getcwd())

if OS.lower()[1] == "l":
    #this means it is a luinux system
    print("adding to cron")
    script = open("CF_DDNS.sh","w")
    script.write("python3 ./mian.py")
    os.system("chmod +x CF_DDNS.sh")

    os.system("crontab -l -u root | cat - "+os.getcwd()+" | crontab -u root -")