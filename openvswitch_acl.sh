#!/bin/bash

ACTION=${1?Type of mitigation not specified}

if [[ "$ACTION" = "set" ]]; then
        ovs-ofctl add-flow br0 priority=2,in_port=4,dl_dst=b8:ac:6f:8b:86:0f,actions=drop
else
	ovs-ofctl --strict del-flows br0 priority=2,in_port=4,dl_dst=b8:ac:6f:8b:86:0f
fi

