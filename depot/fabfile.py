#!/usr/bin/env python

""" 
Depot module for Parallel Spider 

Contains tools to develop, test, and deploy the system.
For ease of use set spider as alias in .bashrc.
Assumes boto is installed and AWS keys are in .bashrc.
Assumes Redis.
TODO: remove assumptions by automatically installing
all requirements with a build.depot command
"""

from fabric.api import *

# data handles redis initialization
import data

# engine handles cluster initialization
import engine



  
