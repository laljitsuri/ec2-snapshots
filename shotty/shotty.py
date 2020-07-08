import boto3
import botocore
import click

session=boto3.Session(profile_name='shotty')
ec2=session.resource('ec2')

def filter_instances(project):
    instances=[]
    if project:
        filters=[{'Name':'tag:project','Values':[project]}]
        instances=ec2.instances.filter(Filters=filters)
    else:
        instances=ec2.instances.all()

    return instances

@click.group()
def cli():
    "CLI for managing aws ec2 automation"

@cli.group('instances')
def ec2_instances():
    "Commands for ec2 instances automation"

@cli.group('volumes')
def ec2_volumes():
    "Commands for ec2 volumes automation"

@cli.group('snapshots')
def ec2_snapshots():
    "Commands for ec2 snapshots automation"

@ec2_instances.command('list')
@click.option('--project',default=None,
                help="Only instances for project with tag project:<project_name>")
def list_instances(project):
    "List EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        tags = { t['Key']:t['Value'] for t in i.tags or []}
        print(' ,'.join((i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project','no_project'))))


@ec2_instances.command('stop')
@click.option('--project',default=None,
                help="Only stop instances for project with tag project:<project_name>")
def stop_instances(project):
    "Stop EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        print("Stopping instance {0}....".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as bce:
            print("Couldn't stop instance {0} due to error {1}. ".format(i.id,str(bce)))
            continue


@ec2_instances.command('start')
@click.option('--project',default=None,
                help="Only start instances for project with tag project:<project_name>")
def start_instances(project):
    "Start EC2 instances"

    instances=filter_instances(project)

    for i in instances:
        print("Starting instance {0}....".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as bce:
            print("Couldn't start instance {0} due to error {1}. ".format(i.id,str(bce)))
            continue

@ec2_volumes.command('list')
@click.option('--project',default=None,
                help="Only volumes for project with tag project:<project_name>")
def list_volumes(project):
    "List EC2 volumes"

    instances=filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(' ,'.join((
            v.id,
            i.id,
            v.state,
            str(v.size)+'GiB',
            v.encrypted and 'Encrypted' or 'Not Encrypted'
            )))


@ec2_snapshots.command('list')
@click.option('--project',default=None,
                help="Only snapshots for project with tag project:<project_name>")
def list_snapshots(project):
    "List EC2 snapshots"

    instances=filter_instances(project)
    snapshots_exist=False

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                snapshots_exist=True
                print(' ,'.join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
    if not snapshots_exist:
        print("No snapshots found")

@ec2_snapshots.command('create_snapshot')
@click.option('--project',default=None,
                help="Create snapshots for project with tag project:<project_name>")
def create_snapshot(project):
    "Create EC2 snapshots"

    instances=filter_instances(project)

    for i in instances:
        print("Stopping instance {0} for volume snapshotting".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshot for volume {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshot automation")
        print("Starting instance {0} after taking volume snapshots".format(i.id))
        i.start()
        i.wait_until_running

    print("Job Done! Snapshots created")
    return

if __name__=='__main__':
    cli()
