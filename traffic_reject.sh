#!/bin/bash

TYPE=${1?Type of mitigation not specified}
PREFIX=${2?Mitigation prefix not specified}

file="/etc/bird/traffic_reject.conf"

#Empty file
> $file

#Specify header and footer of file
header="filter traffic_reject { if net ~ [$PREFIX] then {"
footer="} else accept;}"

#Mitigation techniques
bgp_arp="bgp_next_hop = 10.0.0.112; accept;"
bgp_ce="reject;"

#Set the header
echo $header >> $file

if [[ "$TYPE" = "bgp_arp" ]]; then
	echo $bgp_pe >> $file
elif [[ "$TYPE" == "bgp_ce" ]]; then
	echo $bgp_ce >> $file
else
	#Accept traffic -> no mitigation active
	echo "accept;" >> $file
fi

#Set the footer
echo $footer >> $file

#Result
echo "Done! Result for filter is:"
echo ""
cat $file

echo ""
echo "-----------------------"
echo "Reconfiguring Bird:"
echo ""
birdc configure
