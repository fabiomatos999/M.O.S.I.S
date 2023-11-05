import argparse
import os
parser = argparse.ArgumentParser(description='Start Host Software')
group = parser.add_mutually_exclusive_group()
group.add_argument("-n",
                   "--nobackup",
                   action="store_true",
                   help="Start host software without backing up Raspberry Pi")
group.add_argument("-i",
                   "--ipaddress",
                   type=str,
                   help="IP address of the Raspberry Pi",
                   default="raspberrypi")
parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help='Output folder for Raspberry Pi Backup')

args = parser.parse_args()
