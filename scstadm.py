
import sys
import argparse
import subprocess
import pdb
#populate this map as key value pairs based on options sent in the user
add_lun_options_set = {}

class CmndAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(CmndAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)
        setattr(namespace, self.dest, values)
        add_lun_options_set[option_string] = {}
        add_lun_options_set[option_string]['isset'] = True
        add_lun_options_set[option_string]['value'] = values

def default_exec(cmnd_opts):
    try:
	    print "Doing some commands"
	    path = '/sys/kernel/scst_tgt/targets/iscsi/iqn.2017-08.net.vlnb\:tgt/luns/mgmt'
	    com = 'add '  +cmnd_opts.D+ ' ' +cmnd_opts.l+ ' ">'
	    cmd = 'echo "' + com + path
	    pdb.set_trace();
	    subprocess.check_output(cmd, shell=True )
    except subprocess.CalledProcessError:
            print "error Executing the command"   
    #subprocess.run("ps", shell=True, check=True)

def del_default_exec(cmnd_opts):
    try:
        print "Enter into del_lun"
        path = '/sys/kernel/scst_tgt/targets/iscsi/iqn.2017-08.net.vlnb\:tgt/luns/mgmt'
        com = 'del_lun '  +cmnd_opts.l+ ' ">'
        cmd = 'echo "' + com +path
        #pdb.set_trace();
        print "=====Doing delete device====="
        subprocess.check_output(cmd, shell=True )
        print "=====Successfully deleted device====="
        print "=====leaving del_device====="

    except subprocess.CalledProcessError:
        print "error Executing the del_device command"

#set of commands to run for the options set
add_lun_exec = {"default"  : default_exec
#                   "-d"    : driver_name,
                   }

del_lun_exec = {"default"  : del_default_exec
                   }


def exec_commands(cmnd_opts):
    #execute commands
    print "Executing Arguments"
    if sys.argv[1] == "add_lun":
        add_lun_exec["default"](cmnd_opts);
        for i in add_lun_options_set.iterkeys():
            if add_lun_options_set[i]['isset'] == True:
                add_lun_exec[i](cmnd_opts, add_lun_options_set[i]['value'])
    if sys.argv[1] == "del_lun":
        delete_lun_exec["default"](cmnd_opts);


def parse_Arguments(parser):
    #parse arguments
    print "Parsing Arguments"
    arg1 = parser.parse_args()
    #print arg1.dirname
    #print arg1.P

def setup_SubCommands():
    #need to setup subCommands

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands')

    # A list command
    addLun_parser = subparsers.add_parser('add_lun', help='Add lun to the target')
    addLun_parser.add_argument('-d', action='store', help='driver name', required=True)
    addLun_parser.add_argument('-t', action='store', help='target name', required=True)
    addLun_parser.add_argument('-D', action='store', help='device name create by add_device', required=True)
    addLun_parser.add_argument('-l', action='store', help='LUN', required=True)

    # A delete command
    delLun_parser = subparsers.add_parser('del_lun', help='Add lun to the target')
    delLun_parser.add_argument('-l', action='store', help='driver name', required=True)

    # A create command
    create_parser = subparsers.add_parser('create', help='Create a directory')
    create_parser.add_argument('--dirname', action=CmndAction, help='New directory to create', required=True)
    create_parser.add_argument('--P', action=CmndAction, help='New directory to create', required=True)

    create_parser.add_argument('--read-only', action='store_true',
                               help='Set permissions to prevent writing to the directory',
                               )

    # A delete command
    delete_parser = subparsers.add_parser('del_lun', help='Remove a directory')
    delete_parser.add_argument('dirname', action='store', help='The directory to remove')
    delete_parser.add_argument('--recursive', '-r', default=False, action='store_true',
                               help='Remove the contents of the directory, too',
                               )

    return parser
    print "Setting up SubCommands"

def main():
    print "Starting main"
    parser = setup_SubCommands()
    parse_Arguments(parser)
    exec_commands(parser.parse_args())

if __name__ == "__main__":
    main()
