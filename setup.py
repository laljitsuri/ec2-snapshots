from setuptools import setup

setup(
    name="ec2-snapshots",
    version="0.1",
    author="Laljit Suri",
    author_email="laljitssuri@yahoo.com",
    description="ec2-snapshots is command line tool to manage ec2 snapshots",
    packages=['shotty'],
    url="https://github.com/laljitsuri/ec2-snapshots",
    install_requires=['click','boto3'],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',

)
