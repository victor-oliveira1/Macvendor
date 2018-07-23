#!/usr/bin/env bash
#Copyright © 2018 Victor Oliveira <victor.oliveira@gmx.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar. See the COPYING file for more details.

OUI_URL=http://standards-oui.ieee.org/oui.txt
OUI_FILE=~/.oui.txt
MAC=$1
MAC_SEP=": -"

checkoui(){
# Check if oui file exists. If don't then download
    if [ ! -e ${OUI_FILE} ]; then
        echo Downloading OUI file...
        curl --output ${OUI_FILE} ${OUI_URL}
    fi
}

macvalidate(){
# Verify if mac is valid
    mac=${MAC}
    for sep in ${MAC_SEP}; do
        mac=${mac//${sep}/}
    done

    if [ ${#mac} -lt 6 -o ${#mac} -gt 12 ]; then
        return 1
    elif [[ ! ${mac} =~ ^[[:xdigit:]]+$ ]]; then
        return 1
    else
        return 0
    fi
}

macvendor(){
# Return the vendor of determined mac
    vendor=$(grep -i ${mac:0:6} ${OUI_FILE}| cut -f3)
    if [[ -z ${vendor} ]]; then
        echo ${MAC} - No vendor found
    else
        echo ${MAC} - ${vendor}
    fi
}


if macvalidate; then
    checkoui
    macvendor
else
    echo "Invalid MAC!"
fi
