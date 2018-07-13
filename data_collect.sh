#!/bin/bash

INTERVAL="1"  # update interval in seconds

if [ -z "$1" ]; then
        echo
        echo usage: $0 [network-interface]
        echo
        echo e.g. $0 eth0
        echo
        echo shows packets-per-second
        exit
fi

IF=$1
let i="0"

now=`date '+%Y_%m_%d__%H_%M_%S'`
filename="$now""_metrics.csv"
echo "PPS,BPS(kB),Time(s)" >> /home/rp2/output/$filename


while true
do
        RP1=`cat /sys/class/net/$1/statistics/rx_packets`
        TP1=`cat /sys/class/net/$1/statistics/tx_packets`

	RB1=`cat /sys/class/net/$1/statistics/rx_bytes`
        TB1=`cat /sys/class/net/$1/statistics/tx_bytes`

        sleep $INTERVAL

        RP2=`cat /sys/class/net/$1/statistics/rx_packets`
        TP2=`cat /sys/class/net/$1/statistics/tx_packets`

	RB2=`cat /sys/class/net/$1/statistics/rx_bytes`
        TB2=`cat /sys/class/net/$1/statistics/tx_bytes`

        TXPPS=`expr $TP2 - $TP1`
        RXPPS=`expr $RP2 - $RP1`

	TBPS=`expr $TB2 - $TB1`
        RBPS=`expr $RB2 - $RB1`
	TKBPS=`expr $TBPS / 1024`
        RKBPS=`expr $RBPS / 1024`

	echo "$TXPPS,$TKBPS,$i" >> /home/rp2/output/$filename
	i=$(($i + 1))

	echo "TX $1: $TXPPS pkts/s RX $1: $RXPPS pkts/s"
	echo "TX $1: $TKBPS kB/s RX $1: $RKBPS kB/s"
	echo ""
done

