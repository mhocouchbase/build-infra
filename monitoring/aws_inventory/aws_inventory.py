#!/usr/bin/env python3


import sys
import argparse
import json
import tabulate

import config
import utils

# Get aws inventories and write output to result.txt
# inputs: 
#   profile:             profile value in aws config, i.e "cb-qe".
#   service-classes:     a list of aws sdk classes the script is going to check.
#                        a full list is defined in config.py as AWS_CLASSES.keys()
def get_inventories_by_class(profile, service_classes):
    for service_class in service_classes:
        regions =utils.get_aws_service_regions(profile,service_class)
        inventory = utils.get_inventory(profile, regions, config.AWS_CLASSES[service_class], service_class)
        if 'instance' in inventory:
            ec2_events=utils.get_cloudtrail_start_ec2_events(profile, regions)
            #for i in inventory['instance']:
            for index in range(len(inventory['instance'])):
                if inventory['instance'][index]['InstanceId'] in ec2_events:
                    inventory['instance'][index]['Username']=ec2_events[inventory['instance'][index]['InstanceId']]
                else:
                    inventory['instance'][index]['Username']="Unknown"
        with open('result.txt', 'w') as f:
            f.write(f"{service_class}:\n")
            for key in inventory.keys():
                f.write(f"{key}:\n")
                header = inventory[key][0].keys()
                rows =  [x.values() for x in inventory[key]]
                f.write(tabulate.tabulate(rows, header))
                f.write(f"\n")
    
def parse_args():
    parser = argparse.ArgumentParser(description="Checking current AWS inventories\n\n")
    parser.add_argument('--profile', '-p', help='aws profile', required=True)
    parser.add_argument('--classes', '-c', help='comma separated service classes')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.classes is not None:
        service_classes=list(args.classes.split(","))
    else:
        service_classes=list(config.AWS_CLASSES.keys())
    profile=args.profile
    print(service_classes)

    accountID=utils.get_accountID(profile)
    if(set(service_classes).issubset(config.AWS_CLASSES.keys())):
        get_inventories_by_class(profile, service_classes)
    else:
        print("One or more classes provided, is not supported")
        print(config.AWS_CLASSES.keys())
    

if __name__ == '__main__':
    main()
