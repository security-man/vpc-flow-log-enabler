import boto3
import botocore
import json
from botocore.exceptions import ClientError

# setup account input details and define aws profiles
input_switch_statement = input('Choose input type: 1 = comma-separated list of profiles, 2 = path to aws .config file: ')
if input_switch_statement == '1':

    profile_string = input('Specify AWS Profile List: ')
    profile_list = profile_string.split(",")

elif input_switch_statement == '2':

    profile_string = input('Specify .aws config file path: ')
    profile_list = []

    # Using readlines()
    config_file = open(profile_string, 'r')
    file_lines = config_file.readlines()

    # Strips the newline character
    for line in file_lines:
        line_contents = line.split()
        if len(line_contents) > 0:
            if line_contents[0] == '[profile':
                profile_name = line_contents[1].split(']')
                profile_list.append(profile_name[0])

else:
    raise Exception("Sorry, no numbers below zero")

# user-input region to run script in
script_region = input('Enter AWS region to run script in (hit Enter for default eu-west-2): ')
print(script_region)
if script_region == '':
    script_region = "eu-west-2"

# function to list all available vpcs in region
def get_all_vpcs():
    return [vpc.id for vpc in list(ec2_resource.vpcs.all())]

# function to enable vpc flow logs with defined role, log group, log format
def enable_flow_logs(vpc_id, flow_logs_role_arn, log_group):
    try:
        print(
            f"Trying to enable flow logs for {vpc_id},"
            f" using {log_group} log group and role {flow_logs_role_arn}")
        ec2_client.create_flow_logs(
            DeliverLogsPermissionArn=flow_logs_role_arn,
            LogGroupName=log_group,
            ResourceIds=[vpc_id],
            ResourceType="VPC",
            TrafficType="ALL",
            LogDestinationType="cloud-watch-logs",
            LogFormat="${account-id} ${action} ${az-id} ${bytes} ${dstaddr} ${dstport} ${end} ${flow-direction} ${instance-id} ${interface-id} ${log-status} ${packets} ${pkt-dst-aws-service} ${pkt-dstaddr} ${pkt-src-aws-service} ${pkt-srcaddr} ${protocol} ${region} ${srcaddr} ${srcport} ${start} ${sublocation-id} ${sublocation-type} ${subnet-id} ${tcp-flags} ${traffic-path} ${type} ${version} ${vpc-id}"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "FlowLogAlreadyExists":
            print(f"Flow logs is already enabled for {vpc_id}\n")
    else:
        print(f"Flow logs is successfully enabled for {vpc_id}\n")

# establish client with each aws account
for profile in profile_list:
    session = boto3.Session(profile_name=profile,region_name=script_region)
    account_id = session.client('sts').get_caller_identity().get('Account')
    ec2_resource = session.resource("ec2")
    ec2_client = session.client("ec2")
    log_client = session.client("logs")
    iam_client = session.client("iam")
    vpc_flow_role_arn = "arn:aws:iam::"+account_id+":role/VPCFlowLogsRole"
    # for each aws account, get all vpcs, check for flow logs, and enable where missing
    try:
        vpc_ids = get_all_vpcs()
        for vpc_id in vpc_ids:
            enable_flow_logs(vpc_id,vpc_flow_role_arn,"CSLSVPCFlow")
        del session
    except botocore.exceptions.ClientError as error:
        print("Access Denied to profile '" + profile + "', moving on to next profile ...")
    except botocore.exceptions.ParamValidationError as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))