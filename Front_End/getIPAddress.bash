#!/usr/bin/env bash

ip a | grep $1 | awk '/inet/ {print $2}' | awk -F'/' '{print $1}'
