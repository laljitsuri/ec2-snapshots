# ec2-snapshots
Demo project to automate management of aws ec2 instances


##About
This project is a demo using boto3 module to manage AWS EC2 instance snapshots

## Configuring
shotty uses the config file created by AWS cli using following command:

`aws configure --profile shotty`

## Running

`python3 shotty/shotty.py <command> <--project=project_name>`

##Command
list, stop and start instances for listing, starting or stopping ec2_instances
list volumes for listing volumes across all ec2_instances
list, create_snapshot for listing and creating snapshots for volumes
##project parameter
project parameter is optional. It represents tag 'project' linked with instances. If not provided all the instances are included in command
