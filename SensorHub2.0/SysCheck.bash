#!/bin/bash

PH=$(sudo i2cdetect -y 1 0x63 0x76 | tail -n 2 | awk '/63/ {print 1}')
TEMPERATURE=$(sudo i2cdetect -y 1 0x63 0x76 | tail -n 2 | awk '/68/ {print 1}')
DISSOLVED_OXYGEN=$(sudo i2cdetect -y 1 0x63 0x76 | tail -n 2 | awk '/67/ {print 1}')
PRESSURE=$(sudo i2cdetect -y 1 0x63 0x76 | tail -n 2 | awk '/76/ {print 1}')

if [[ "$PH" == "" ]]; then
	PH=0
fi

if [[ "$TEMPERATURE" == "" ]]; then
	TEMPERATURE=0
fi

if [[ "$DISSOLVED_OXYGEN" == "" ]]; then
	DISSOLVED_OXYGEN=0
fi

if [[ "$PRESSURE" == "" ]]; then
	PRESSURE=0
fi

echo "$PH$TEMPERATURE$DISSOLVED_OXYGEN$PRESSURE"
