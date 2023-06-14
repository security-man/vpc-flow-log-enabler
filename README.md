# AWS VPC Flow Log Enabler

## Description

This simple python script automatically enables VPC Flow logging to any VPCs within a specified AWS Account ID. A log group name is specified at runtime to provide a destination for VPC Flow logging. Any VPCs that already have VPC Flow logging enabled are excluded.

## Requirements and Installation

To run this script you'll need to have valid [python3](https://www.python.org/downloads/), [pip](https://python.land/virtual-environments/installing-packages-with-pip) and [boto3](https://pypi.org/project/boto3/) installations. 

Next, simply clone the repository and execute the python script through a terminal session.

## Running a scan

To run, execute the script through a terminal session:

        $ python3 vpc-flow-log-enabler.py

There are two options provided for scanning:

### Option 1 (comma-separated list of profiles)

For this option simply provide a comma-separated list of AWS profiles to scan. Profiles should correspond with the listed profile names within your .aws/.config file. E.g., for a scan against 3 profiles named **PROFILE1**,**PROFILE2**,**PROFILE3**:

        $ python3 vpc-flow-log-enablerr.py
        $ Choose input type: 1 = comma-separated list of profiles, 2 = path to aws .config file: 1
        $ Specify AWS Profile List: PROFILE1,PROFILE2,PROFILE3

### Option 2 (path to aws .config file)

For this option simply provide a path to your .aws/.config file. **NOTE**: This will scan against **ALL** of the AWS profiles listed within your .aws/.config file. Depending on the number of buckets/objects in each AWS Account represented by a profile, this could take several seconds/minutes per account.

        $ python3 vpc-flow-log-enabler.py
        $ Choose input type: 1 = comma-separated list of profiles, 2 = path to aws .config file: 2
        $ Specify .aws config file path: /path/to/.aws/.config


## License

vpc-flow-log-enabler is licensed as GNU GLPv3. You may obtain a copy of the License at https://www.gnu.org/licenses/gpl-3.0.en.html