import os
from sys import platform

OS = platform

print(os.getcwd())

if OS.lower()[1] == "l":
    #this means it is a luinux system
    print("adding to cron")
    os.system("""sudo echo \"[Unit]\\n
    Description=Updates your DNS records\\n
    After=network.target\\n
    
    [Service]\\n
    Type=idle\\n
    Restart=on-failure\\n
    User=root\\n
    ExecStart=/usr/bin/python """
              +os.getcwd()+"main.py"+"""\\n
    RestartSec=30
    [Install]\\n
    WantedBy=multi-user.target\" > /lib/systemd/system/CF_DDNS.service""")
    os.system("sudo chmod 644 /lib/systemd/system/CF_DDNS.service")
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl enable CF_DDNS.service")