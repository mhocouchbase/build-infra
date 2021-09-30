import boto3
import json
import datetime
import collections

#  Get regions by service class.  
#  Return regions that input service class are available in
def get_aws_service_regions(profile, class_name):
    session = boto3.Session(profile_name=profile, region_name="us-east-2")
    client = session.client(class_name)

    regions = client.describe_regions(Filters=[{'Name':'opt-in-status', 'Values':['opt-in-not-required', 'opted-in']}])
    return regions["Regions"]


# Find account ID from profile
def get_accountID(profile):
    session = boto3.Session(profile_name=profile)
    sts = session.client('sts')
    identity = sts.get_caller_identity()
    accountId = identity['Account']
    return accountId

# Make datetime.datetime json object serializable
def json_serial_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# Get inventory by class from reginal service
# Reginal services includes ec2, ecs, efs, etc.
# To-Do: add pagination for large results

def get_inventory_regional(profile,regions,service_class,class_name):
    inventory = collections.defaultdict(list)

    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region['RegionName'])
        client = session.client(class_name)

        for service_name in service_class.keys():
            method=service_class[service_name]['method']
            if hasattr(client, method):
                result=getattr(client,method)()
                key=service_class[service_name]['key']
                if 'subkey' in service_class[service_name].keys():
                    subkey=service_class[service_name]['subkey']
                    for r in result[key]:
                        for i in r[subkey]:
                            i['region']=region['RegionName']
                            inventory[service_name].append({key:i[key] for key in service_class[service_name]['dataset']})
                elif 'filter' in service_class[service_name].keys():
                    for r in result[key]:
                        filterkey=service_class[service_name]['filter']['key']
                        filtervalue=service_class[service_name]['filter']['value']
                        if (r[filterkey] != filtervalue):
                            r['region']=region['RegionName']
                            inventory[service_name].append({key:r[key] for key in service_class[service_name]['dataset']})
                else:
                    for r in result[key]:
                        r['region']=region['RegionName']
                        inventory[service_name].append({key:r[key] for key in service_class[service_name]['dataset']})
    return inventory

# Get inventory by class from global service
# Global services includes autoscaling, batch, ecs, efs, etc.
# To-Do: add pagination for large results

def get_inventory_global(profile,service_class,class_name):
    inventory = collections.defaultdict(list)

    session = boto3.Session(profile_name=profile)
    client = session.client(class_name)

    for service_name in service_class.keys():
        method=service_class[service_name]['method']
        if hasattr(client, method):
            result=getattr(client,method)()
            key=service_class[service_name]['key']
            if 'subkey' in service_class[service_name].keys():
                subkey=service_class[service_name]['subkey']
                for r in result[key]:
                    for i in r[subkey]:
                        i['region']=region['RegionName']
                        inventory[service_name].append({key:i[key] for key in service_class[service_name]['dataset']})
            elif 'filter' in service_class[service_name].keys():
                for r in result[key]:
                    filterkey=service_class[service_name]['filter']['key']
                    filtervalue=service_class[service_name]['filter']['value']
                    if (r[filterkey] != filtervalue):
                        r['region']=region['RegionName']
                        inventory[service_name].append({key:r[key] for key in service_class[service_name]['dataset']})
            else:
                for r in result[key]:
                    r['region']=region['RegionName']
                    inventory[service_name].append({key:r[key] for key in service_class[service_name]['dataset']})
    return inventory
# Get s3 inventory
def get_s3_inventory(profile):

    inventory  = collections.defaultdict(list)

    s3 = boto3.resource('s3')

    for bucket in s3.buckets.all():
        total_size = 0
        for object in bucket.objects.all():
            total_size += object.size
        print("bucket " + getattr(bucket, 'name') + ":" + str(total_size/1024/1024/1024) + "GB")
        inventory['s3'].append({'name': getattr(bucket, 'name'), 'size': str(total_size/1024/1024/1024) + "GB", 'region': region['RegionName']})

    return inventory

# Identify user if any who start ec2 instances from cloudtrail
# Cloudtrail only keeps up to 90 days of events.  
# Hence it might not be possible to find who start the instance.
def get_cloudtrail_start_ec2_events(profile, regions):
    events = {}
    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region['RegionName'])
        client = session.client('cloudtrail')
        response = client.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'RunInstances'
                },
            ]
        )

        for e in response['Events']:
            for resource in e['Resources']:
                if (resource.get('ResourceType') == "AWS::EC2::Instance"):
                    events[resource.get('ResourceName')]=e.get('Username')
    return events

