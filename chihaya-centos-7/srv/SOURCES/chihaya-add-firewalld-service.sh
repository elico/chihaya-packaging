#!/usr/bin/env bash

firewall-offline-cmd --new-service=chihaya

firewall-offline-cmd --service=chihaya --set-description=Chihaya-Bittorent-Tracker
firewall-offline-cmd --service=chihaya --set-short=Chihaya

firewall-offline-cmd --service=chihaya --add-port=6880/tcp

firewall-offline-cmd --service=chihaya --add-port=6969/tcp
firewall-offline-cmd --service=chihaya --add-port=6969/udp
