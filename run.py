import os
import sys
from bottle import run

import model
import view
import controller

#-----------------------------------------------------------------------------
# Change this to your IP address or 0.0.0.0 when actually hosting
host = '20.11.24.131'

# Test port, change to the appropriate port to host
port = 80

# Turn this off for production
debug = False

def run_server():    
    '''
        run_server
        Runs a bottle server
    '''
    run(host=host, port=port, debug=debug, server='gunicorn', keyfile='./certs/info2222.test.key', certfile='./certs/info2222.test.crt')

#-----------------------------------------------------------------------------

# What commands can be run with this python file
command_list = {
    'server'       : run_server
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

run_commands(sys.argv)
