#!/bin/bash
ssh root@10.0.0.5 'bash -s' < traffic_reject.sh unban 3.3.3.0/24;
ssh root@10.0.0.2 'bash -s' < openvswitch_acl.sh unset;


