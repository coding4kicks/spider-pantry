""" Parallel Spider analysis engine tasks. """

import fabric.api as fab

import os
import sys
import signal
import threading
import subprocess

# Determine path to parallelspider directory.
# Assumes this file is in spiderdepot or subdirectory,
# and spiderdepot is 1 level below parallelspider.
path = os.path.realpath(__file__).partition('depot')[0]

@fab.task
def new(type="develop"):
    """Start a spider engine from scratch, not an AMI."""

    # Initial commands must be synchronous
    # Use micro-develop template - default
    # or micro-deploy template
    cmd = 'starcluster start -c micro-develop spiderdev'
    cluster_name = 'spiderdev';
    nodes = 1;
    if type == "deploy":
        cmd = "starcluster start -c micro-deploy spiderdeploy"
        cluster_name = 'spiderdeploy'
        nodes = 10;
    #p = subprocess.call(cmd, shell=True)
    #if p != 0:
    #    print "Starcluster failed to start."
    #    sys.exit(1)

    # Create list of nodes
    instance_list = []
    #nodes = 1
    i = 1;
    while i <= nodes:
        if i < 10:
            node_name = 'node00' + str(i)
        elif i < 100:
            node_name = 'node0' + str(i)
        elif i < 1000:
            node_name = 'node' + str(i)
        else:
            print "Too many nodes dumbass."
            sys.exit(1)
        instance_list.append(node_name)
        i += 1

    # Launch master and nodes
    t = threading.Thread(target=init_config, args=('master', 'master', cluster_name))
    t.start()
    for instance in instance_list:
        t = threading.Thread(target=init_config, args=('node', instance, cluster_name))
        t.start()
    #print instance_list

def init_config(instance_type=None, instance=None, cluster_name='spiderdev'):
    cmd_list = [
            'sudo apt-get update',
            'sudo apt-get install --yes --force-yes libxml2-dev libxslt1-dev',
            'sudo pip install lxml',
            'sudo pip install beautifulsoup4',
            'sudo pip install cssselect',
            'sudo pip install redis',
            'sudo pip install boto',
            'git clone https://coding4kicks:\!6Graham9@github.com/' + \
            'coding4kicks/spider-pantry.git /home/spideradmin/spiderengine'
            ]
    for cmd in cmd_list:
        print 'cluster name'
        print cluster_name
        if instance_type == 'master':
            full_cmd = 'starcluster sshmaster ' + cluster_name + " '" + cmd + "'"
        elif instance_type == 'node':
            full_cmd = 'starcluster sshnode ' + cluster_name + " node001 '" + cmd + "'"
        else:
            print('Error: Unknown Instance Type')
            sys.exit(1)
        p = subprocess.call(full_cmd, shell=True)
        if p != 0:
            print 'Command failed: ' + cmd
            print 'For instance: ' + instance
            print full_cmd
            sys.exit(1)
        print 'Command: ' + cmd + ' executed on ' + instance + '.'

    # upload bash
    full_cmd = 'starcluster put ' + cluster_name + ' --node ' + instance + \
            '~/projects/bash_profiles/.bashrc-spiderengine /root/.bash_aliases'
    p = subprocess.call(full_cmd, shell=True)
    if p != 0:
        print 'Command failed: upload bashrc'
        print 'For instance: ' + instance
        sys.exit(1)

    # install redis only on master
    cmd_list = [
     'wget -P /home/spideradmin/ http://redis.googlecode.com/files/' + \
             'redis-2.6.11.tar.gz',
     'tar xzf /home/spideradmin/redis-2.6.11.tar.gz -C /home/spideradmin',
     'make -C /home/spideradmin/redis-2.6.11' 
            ]
    if instance_type == 'master':
        for cmd in cmd_list:
            full_cmd = 'starcluster sshmaster ' + cluster_name + " '" + cmd + "'"
            p = subprocess.call(full_cmd, shell=True)
            if p != 0:
                print 'Command failed: ' + cmd
                print 'For instance: ' + instance
                sys.exit(1)
            print 'Command: ' + cmd + ' executed on ' + instance + '.'



@fab.task
def put(f=None, type='develop'):
    """Upload a file to the engine."""
    if file:
        cluster_name = 'spiderdev';
        if type == "deploy":
            cluster_name = 'spiderdeploy'
        source = path + '/src/' + f
        dest = '/home/spideradmin/spiderengine/src/'
        cmd = 'starcluster put ' + cluster_name + ' ' + source + ' ' + dest
        p = subprocess.call(cmd, shell=True)
        if p != 0:
            print 'Command failed: ' + cmd
            sys.exit(1)
    else:
        print "Must specify a file to upload"

@fab.task
def start(type='develop', args=None):
    """Start an analysis engine."""
    
@fab.task
def stop(type='local', args=None):
    """Stop an analysis engine."""


# TODO: FIX to pull from github
@fab.task
def synch(type="develop"):
    """Synch repo on master"""
    cluster_name = 'spiderdev';
    if type == "deploy":
        cluster_name = 'spiderdeploy'
    cmd = "starcluster sshmaster " + cluster_name + \
          " 'cd /home/spideradmin/spiderengine; git pull origin'"
    p = subprocess.call(cmd, shell=True)
    if p != 0:
        print 'Command failed: ' + cmd
        sys.exit(1)

# Fix to just run tests (just pull with deploy)
@fab.task
def run_tests():
    """Test spider engine on remote cluster"""






