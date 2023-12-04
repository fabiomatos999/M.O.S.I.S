import argparse
import os
parser = argparse.ArgumentParser(description='Start Host Software')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-n",
                   "--nobackup",
                   action="store_true",
                   help="Start host software without backing up Raspberry Pi")
group.add_argument("-i",
                   "--ipaddress",
                   type=str,
                   help="IP address of the Raspberry Pi",
                   default="raspberrypi.local")
parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help='Output Folder for the Generated Report')

args = parser.parse_args()
