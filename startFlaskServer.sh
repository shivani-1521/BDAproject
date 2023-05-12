#!/bin/bash
cd show_webpage
external_ip=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip" -H "Metadata-Flavor: Google" | grep .)
echo "View webpage at external IP address of this instance at port 5000: $external_ip:5000"
python3 renderWithNews.py