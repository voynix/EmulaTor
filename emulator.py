"""

EmulaTor

Copyright (c) 2015, Adam Jacobson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

##########################################################
# AS THE END-USER, YOU SHOULD NOT NEED TO EDIT THIS FILE #
##########################################################

import argparse

from os import mkdir, path, remove, system
from shutil import copyfile, copytree, rmtree

from constants import *


# build the parser, get the args
parser = argparse.ArgumentParser(description = 'Generate experimental configurations for investigating Tor with EmuLab')
parser.add_argument('name', metavar = 'NAME', help = 'the name of the simulation')
parser.add_argument('-v', '--overwrite', action = 'store_true', help = 'if a file or folder called NAME already exists, overwrite it with the generated configuration')
parser.add_argument('-o', '--os', metavar = 'OS', default = DEFAULT_OS, help = 'the operating system to deploy on all nodes; for acceptable values see list at https://www.emulab.net/showosid_list.php3 [default: %s]' % DEFAULT_OS)
parser.add_argument('-t', '--tor', metavar = 'TOR', help = 'the path to the statically-compiled version of tor to deploy. This option is mandatory if -o is given. [default: tor-0.2.6.10]')
parser.add_argument('-j', '--project-name', metavar = 'PROJECT_NAME', default = DEFAULT_PROJECT_NAME, help = 'the name of the EmuLab project this experiment will be run under [default: %s]' % DEFAULT_PROJECT_NAME)
parser.add_argument('-y','--relays', metavar = 'RELAYS', type = int, required = True, help = 'the number of Tor relays (non-exit nodes) to create')
parser.add_argument('-e', '--exits', metavar = 'EXITS', type = int, required = True, help = 'the number of Tor exit nodes to create')
parser.add_argument('-c', '--clients', metavar = 'CLIENTS', type = int, default = -1, help = 'the number of Tor clients to create [default: RELAYS*RELAYS*EXITS]')
parser.add_argument('-s', '--servers', metavar = 'SERVERS', type = int, default = 1, help = 'the number of nginx servers to create [default: 1]')
parser.add_argument('-a', '--authorities', metavar = 'AUTHORITIES', type = int, default = 1, help = 'the number of Tor Directory Authorities to create [default: 1]')
parser.add_argument('-l', '--lossy-nodes', metavar = 'NODE_NAME', default = [], nargs = '*', help = 'the names of the nodes or groups of nodes to be made lossy (eg \'relay1\', \'exit2\', \'torthority3\', \'client10\', \'server4\', \'clients\')')
parser.add_argument('-r', '--loss-rates', metavar = 'RATE', default = [], nargs = '*', help = 'what percent of packets the lossy nodes or groups of nodes should drop (eg 30, 001). This option is manadatory if -l is given.\n \
                                                                                               To give all lossy nodes the same loss rate pass one value with -r. \
                                                                                               To give each lossy node its own loss rate pass one rate per node or group of nodes in corresponding order.')
parser.add_argument('-f', '--script-file', metavar = 'FILE', help = 'configure scripts based on the specification given in this file')
parser.add_argument('-i', '--include-files', metavar = 'FILES', default = [], nargs = '*', help = 'a list of files or folders to copy into the output folder')
parser.add_argument('--setup-script', metavar = 'SETUP-SCRIPT', help = 'a setup script to run on all nodes.\nIf the name of the script contains \'##\', \
                                                                 a copy of the script will be made for each node with \'##\' replaced with the name of the node \
                                                                 in the name and body of the script.\n \
                                                                 Since EmuLab executes all scripts with csh this script MUST include a valid shebang (\'#!\') line \
                                                                 if it is not a csh-compatible shell script.\n \
                                                                 Note also that EmuLab swallows all script output by default, so redirecting relevant output to a \
                                                                 log file (eg, in /proj) is recommended.')
parser.add_argument('--setup-script-start', metavar = 'TIME', default = DEFAULT_USER_SETUP_START_TIME, type = int, help = 'when to run SETUP-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ignored if --setup-script is not given.' % DEFAULT_USER_SETUP_START_TIME)
parser.add_argument('--setup-script-stop', metavar = 'TIME', default = DEFAULT_USER_SETUP_STOP_TIME, type = int, help = 'when to terminate SETUP-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ingnored if --setup-script is not given.' % DEFAULT_USER_SETUP_STOP_TIME)
parser.add_argument('--setup-script-client-only', action = 'store_true', help = 'run SETUP-SCRIPT on the client nodes only.\nThis option is ignored if --setup-script is not given.')
parser.add_argument('--experimental-script', metavar = 'EXPERIMENTAL-SCRIPT', help = 'an experimental script to run on all nodes.\nIf the name of the script contains \'##\', \
                                                                                     a copy of the script will be made for each node with \'##\' replaced with the name of the node \
                                                                                     in the name and body of the script.\n \
                                                                                     The various warnings on --setup-script also apply here.')
parser.add_argument('--experimental-script-start', metavar = 'TIME', default = DEFAULT_USER_EXPERIMENTAL_START_TIME, type = int, help = 'when to run EXPERIMENTAL-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ignored if --experimental-script is not given.' % DEFAULT_USER_EXPERIMENTAL_START_TIME)
parser.add_argument('--experimental-script-stop', metavar = 'TIME', default = DEFAULT_USER_EXPERIMENTAL_STOP_TIME, type = int, help = 'when to terminate EXPERIMENTAL-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ignored if --experimental-script is not given.' % DEFAULT_USER_EXPERIMENTAL_STOP_TIME)
parser.add_argument('--experimental-script-client-only', action = 'store_true', help = 'run EXPERIMENTAL-SCRIPT on the client nodes only.\nThis option is ignored if --experimental-script is not given.')
parser.add_argument('--cleanup-script', metavar = 'CLEANUP-SCRIPT', help = 'a cleanup script to run on all nodes.\nIf the name of the script contain \'##\', \
                                                                           a copy of the script will be made for each node with \'##\' replaced with the name of the node \
                                                                           in the name and body of the script.\n \
                                                                           The various warnings on --setup-script also apply here.')
parser.add_argument('--cleanup-script-start', metavar = 'TIME', default = DEFAULT_USER_CLEANUP_START_TIME, type = int, help = 'when to run CLEANUP-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ignored if --cleanup-script is not given.' % DEFAULT_USER_CLEANUP_START_TIME)
parser.add_argument('--cleanup-script-stop', metavar = 'TIME', default = DEFAULT_USER_CLEANUP_STOP_TIME, type = int, help = 'when to terminate CLEANUP-SCRIPT, in seconds since simulation start [default: %i].\nThis option is ignored if --cleanup-script is not given.' % DEFAULT_USER_CLEANUP_STOP_TIME)
parser.add_argument('--cleanup-script-client-only', action = 'store_true', help = 'run CLEANUP-SCRIPT on the client nodes only.\nThis option is ignored if --cleanup-script is not given.')

args = parser.parse_args()

def raise_error(message, is_warning = False):
    if is_warning:
        print 'WARNING: %s' % message
    else:
        print 'ERROR: %s' % message
        print 'Exiting!'
        if path.exists(build_path):
            rmtree(build_path)
        raise SystemExit

build_path = args.name
if build_path[-1] != path.sep:
    build_path += path.sep

# build a full path to the SOURCE_FOLDER
SOURCE_FOLDER = path.dirname(path.realpath(__file__)) + path.sep + SOURCE_FOLDER
if not path.exists(SOURCE_FOLDER):
    raise_error('The \'SUPPORT\' folder could not be located!\n\t\tPlease locate it at \'%s\'!' % SOURCE_FOLDER)

if args.project_name != None:
    deployment_prefix = DEPLOYMENT_PREFIX_BASE % args.project_name
else:
    deployment_prefix = DEPLOYMENT_PREFIX_BASE % DEFAULT_PROJECT_NAME

os_name = args.os
tor_path = args.tor if args.tor != None else SOURCE_FOLDER + TOR_EXECUTABLE_NAME

# sanity check OS and Tor specification

if os_name != DEFAULT_OS:
    print 'WARNING: OS other than %s selected; functionality not guaranteed' % DEFAULT_OS
    if tor_path == SOURCE_FOLDER + TOR_EXECUTABLE_NAME:
        print 'WARNING: Default Tor and non-default OS selected'
        print 'WARNING: As Tor is compiled against %s it may fail to work with %s' % (DEFAULT_OS, os_name)
        print 'WARNING: Proceed with caution; Tor functionality not guaranteed'

lossy_nodes = args.lossy_nodes
loss_rates = args.loss_rates

# sanity check lossy nodes and loss rates

if len(lossy_nodes) > 0 and len(loss_rates) == 0:
    raise_error('Lossy nodes specified but no loss rates given.')
elif len(loss_rates) < len(lossy_nodes):
    if len(loss_rates) > 1:
        raise_error('Too few loss rates given; you must specify one rate for all nodes/node groups or one per node/node group.')
    loss_rates = [loss_rates[0] for x in xrange(0, len(lossy_nodes))]

include_files = args.include_files

num_relays = args.relays
num_exits = args.exits

if args.clients == -1:
    num_clients = num_relays * num_relays * num_exits
else:
    num_clients = args.clients

num_servers = args.servers
num_authorities = args.authorities

# sanity check numbers of Tor nodes

if num_relays < 0 or num_exits < 0 or num_clients < 0 or num_authorities < 0 or num_servers < 0:
    raise_error('Cannot create negative number of nodes!')

if num_exits == 0:
    raise_error('Tor network contains 0 exit nodes, preventing circuit building!', True)

if num_authorities == 0:
    raise_error('Tor network has 0 Directory Authorities, preventing Tor bootstrapping!', True)

if num_authorities > MAX_AUTHORITIES:
    raise_error('Cannot create more than %i authorities' % MAX_AUTHORITIES)

print 'WARNING: %s must be deployed to %s!' % (build_path, deployment_prefix)

if path.exists(build_path[:-1]):
    if args.overwrite:
        print 'Overwriting %s' % build_path[:-1]
        if path.isdir(build_path[:-1]):
            rmtree(build_path)
        else:
            remove(build_path)
    else:
        raise_error('%s already exists!' % build_path)

print 'Creating directories...'

mkdir(build_path)
mkdir(build_path + LOG_FOLDER)
mkdir(build_path + RESULTS_FOLDER)

# load script file
custom_scripts = []
if args.script_file != None:
    if not path.exists(args.script_file):
        raise_error('Could not find script file %s' % args.script_file)
    print 'Reading custom script file %s' % args.script_file
    with open(args.script_file, 'r') as script_file:
        current_script = {}
        next_line = None
        for line in script_file:
            if line[:6] == 'SCRIPT':
                current_script = {}
                next_line = 'source'
            elif next_line == 'source':
                current_script['source'] = line[:-1] # cull trailing newline
                next_line = 'targets'
            elif next_line == 'targets':
                pending_targets = line[:-1].split(' ')
                list_targets = filter(lambda x: False if x[-1] in [str(y) for y in xrange(0, 10)] else True, pending_targets)
                individual_targets = filter(lambda x: True if x[-1] in [str(y) for y in xrange(0, 10)] else False, pending_targets)
                current_script['targets'] = list_targets
                if len(individual_targets) > 0:
                    current_script['targets'].append(individual_targets)
                next_line = 'start'
            elif next_line == 'start':
                current_script['start'] = int(line[:-1])
                next_line = 'stop'
            elif next_line == 'stop':
                current_script['stop'] = int(line[:-1])
                next_line = None
            elif line[:10] == 'END_SCRIPT':
                custom_scripts.append(current_script.copy())

print 'Creating simulation file...'

with open(build_path + NS_FILE_NAME, 'w') as ns_file:
    # prelude
    ns_file.write('set ns [new Simulator]\n')
    ns_file.write('source tb_compat.tcl\n')

    def write_node(node_name, os_name = os_name):
        ns_file.write('set %s [$ns node]\n' % node_name)
        ns_file.write('tb-set-node-os $%s %s\n' % (node_name, os_name))

    def write_LAN(lan_name, bandwidth = DEFAULT_LAN_BANDWIDTH, latency = DEFAULT_LAN_LATENCY, loss_rate = DEFAULT_LOSS_RATE, *node_names):
        nodes = ('$%s ' * len(node_names)) % tuple(node_names)
        ns_file.write('set %s [$ns make-lan "%s" %s %ims]\n' % (lan_name, nodes, bandwidth, latency))
        ns_file.write('tb-set-lan-loss $%s 0.%s\n' % (lan_name, loss_rate))

    def write_link(link_name, node_a, node_b, bandwidth = DEFAULT_LINK_BANDWIDTH, latency = DEFAULT_LINK_LATENCY, queue_type = DEFAULT_QUEUE_TYPE, loss_rate = DEFAULT_LOSS_RATE):
        ns_file.write('set %s [$ns duplex-link $%s $%s %s %ims %s]\n' % (link_name, node_a, node_b, bandwidth, latency, queue_type))
        ns_file.write('tb-set-link-loss $%s 0.%s\n' % (link_name, loss_rate))

    def write_script_program(program_name, node_name, program, start_time, stop_time = NO_STOP_TIME, prefix = deployment_prefix):
        ns_file.write('set %s [$%s program-agent -command "%s%s%s"]\n' % (program_name, node_name, prefix, build_path, program))
        ns_file.write('$ns at %i "$%s start"\n' % (start_time, program_name))
        if stop_time != -1:
            ns_file.write('$ns at %i "$%s stop"\n' % (stop_time, program_name))

    def write_custom_script(script_name, script_program_name, start_time, stop_time, node_list):
        for node_name in node_list:
            write_script_program(script_program_name % node_name, node_name, script_name.replace('##', node_name), start_time, stop_time)

    lan_nodes = []
    tor_nodes = []
    all_nodes = []
    client_nodes = [CLIENT_NAME % x for x in xrange(0, num_clients)]
    exit_nodes = [EXIT_NAME % x for x in xrange(0, num_exits)]
    relay_nodes = [RELAY_NAME % x for x in xrange(0, num_relays)]
    authority_nodes = [AUTHORITY_NAME % x for x in xrange(0, num_authorities)]
    server_nodes = [SERVER_NAME % x for x in xrange(0, num_servers)]

    targets_to_node_lists = {ALL_TARGET: all_nodes, RELAY_TARGET: tor_nodes, EXIT_TARGET: exit_nodes, NON_EXIT_RELAYS_TARGET: relay_nodes, AUTHORITY_TARGET: authority_nodes, CLIENT_TARGET: client_nodes, SERVER_TARGET: server_nodes}

    # expand out lossy node, now that we have node lists
    expanded_lossy_nodes = []
    expanded_loss_rates = []
    for node, loss_rate in zip(lossy_nodes, loss_rates):
        if node[-1] in [str(x) for x in xrange(0, 9)]:
            expanded_lossy_nodes.append(node)
            expanded_loss_rates.append(loss_rate)
        else: # node is actually a target!
            for node_name in targets_to_node_lists[node]:
                expanded_lossy_nodes.append(node_name)
                expanded_loss_rates.append(loss_rate)
    lossy_nodes = expanded_lossy_nodes
    loss_rates = expanded_loss_rates

    def write_nodes(max, node_name_pattern, tor_node = True):
        for x in xrange(0, max):
            node_name = node_name_pattern % x
            write_node(node_name)
            all_nodes.append(node_name)
            if tor_node:
                tor_nodes.append(node_name)
            if node_name in lossy_nodes:
                write_node(INTERPOSER_NAME % node_name)
                lan_nodes.append(INTERPOSER_NAME % node_name)
            else:
                lan_nodes.append(node_name)

    print '\tWriting nodes...'

    # relays
    write_nodes(num_relays, RELAY_NAME)

    # exits
    write_nodes(num_exits, EXIT_NAME)

    # authorities
    write_nodes(num_authorities, AUTHORITY_NAME, False)

    # servers
    write_nodes(num_servers, SERVER_NAME, False)

    # clients
    write_nodes(num_clients, CLIENT_NAME, False)

    # LAN for everyone
    write_LAN(LAN_NAME, DEFAULT_LAN_BANDWIDTH, DEFAULT_LAN_LATENCY, DEFAULT_LOSS_RATE, *lan_nodes)

    # Links from interposers to lossy nodes
    for node_name, loss_rate in zip(lossy_nodes, loss_rates):
        write_link(LOSSY_LINK_NAME % node_name, INTERPOSER_NAME % node_name, node_name, loss_rate = loss_rate)

    # set up default routing
    ns_file.write('$ns rtproto Static\n')

    print '\tWriting setup scripts...'

    # set up servers
    for x in xrange(0, num_servers):
        write_script_program(SERVER_PROGRAM_NAME % x, SERVER_NAME % x, NGINX_SETUP_FILE_NAME, INFRASTRUCTURE_START_TIME)

    # set up tor on the authority nodes
    for node_name in authority_nodes:
        write_script_program(TOR_NODE_PROGRAM_NAME % node_name, node_name, TOR_SETUP_FILE_NAME % node_name, INFRASTRUCTURE_START_TIME)

    # set up tor on all other tor network nodes
    for node_name in tor_nodes:
        write_script_program(TOR_NODE_PROGRAM_NAME % node_name, node_name, TOR_SETUP_FILE_NAME % node_name, TOR_START_TIME)

    # set up tor on client nodes
    for node_name in client_nodes:
        write_script_program(TOR_NODE_PROGRAM_NAME % node_name, node_name, TOR_SETUP_FILE_NAME % node_name, CLIENT_START_TIME)

    print '\tWriting user scripts...'

    def setup_script_from_flags(script, client_only, program, start, stop):
        script_name = path.basename(script)
        node_list = all_nodes if not client_only else client_nodes
        write_custom_script(script_name, program, start, stop, node_list)

    # set up custom user setup scripts
    if args.setup_script != None:
        setup_script_from_flags(args.setup_script, args.setup_script_client_only, USER_SETUP_PROGRAM_NAME, args.setup_script_start, args.setup_script_stop)

    # set up custom experimental scripts
    if args.experimental_script != None:
        setup_script_from_flags(args.experimental_script, args.experimental_script_client_only, USER_EXPERIMENTAL_PROGRAM_NAME, args.experimental_script_start, args.experimental_script_stop)

    # set up custom cleanup scripts
    if args.cleanup_script != None:
        setup_script_from_flags(args.cleanup_script, args.cleanup_script_client_only, USER_CLEANUP_PROGRAM_NAME, args.cleanup_script_start, args.cleanup_script_stop)

    # set up custom user scripts from file
    if len(custom_scripts) > 0:
        for script in custom_scripts:
            # replace bad symbols that emulab can't handle
            script_name = path.basename(script['source'])
            cleaned_script_name = script_name.replace('.', 'O').replace('-', 'D').replace('#', 'H').replace('_', 'U')
            if len(cleaned_script_name) > MAX_SAFE_SCRIPT_NAME_LENGTH:
                raise_error('Script name %s is long and may cause issues with EmuLab!\n\t\tConsider shortening it.' % script_name)
            for target in script['targets']:
                write_custom_script(script_name, USER_CUSTOM_PROGRAM_NAME % (cleaned_script_name, '%s'), script['start'], script['stop'],
                                    targets_to_node_lists[target] if isinstance(target, str) else target)

    # actually run the simulation
    ns_file.write('$ns run\n')

print 'Moving resources...'

copyfile(SOURCE_FOLDER + NGINX_CONF_FILE_NAME, build_path + NGINX_CONF_FILE_NAME)
copyfile(tor_path, build_path + TOR_EXECUTABLE_NAME)
copyfile(SOURCE_FOLDER + NGINX_SOURCE_NAME, build_path + NGINX_SOURCE_NAME)
copyfile(SOURCE_FOLDER + PCRE_SOURCE_NAME, build_path + PCRE_SOURCE_NAME)
copyfile(SOURCE_FOLDER + ZLIB_SOURCE_NAME, build_path + ZLIB_SOURCE_NAME)
copyfile(SOURCE_FOLDER + CURL_SOURCE_NAME, build_path + CURL_SOURCE_NAME)

copyfile(SOURCE_FOLDER + GEOIP_FILE_NAME, build_path + GEOIP_FILE_NAME)

system('chmod +x %s%s' % (build_path, TOR_EXECUTABLE_NAME))

print '\tLoading authority data...'

authority_fingerprints = [] # for each authority_node [v3ident, fingerprint]
for x in xrange(0, num_authorities):
    node_name = AUTHORITY_NAME % x
    copytree(SOURCE_FOLDER + AUTHORITY_RESOURCE_FOLDER + str(x), build_path + node_name)
    authority_fingerprints.append([])
    # grab the v3ident
    with open(build_path + node_name + AUTHORITY_CERTIFICATE, 'r') as cert_file:
        cert_file.readline() # ignore the first line
        authority_fingerprints[x].append(cert_file.readline().split(' ')[1][:-1])
    # grab the fingerprint
    with open(build_path + node_name + FINGERPRINT_FILE, 'r') as in_file:
        authority_fingerprints[x].append(in_file.readline().split(' ')[1][:-1])
    # grab the fingerprint
    with open(build_path + node_name + FINGERPRINT_FILE, 'w') as out_file:
        out_file.write('%s %s\n' % (node_name, authority_fingerprints[x][1]))

print '\tCopying user-specified files...'

for object in include_files:
    if not path.exists(object):
        raise_error('Object \'%s\' does not exist and could not be copied!' % object)
    if path.isdir(object):
        if object[-1] == path.sep:
            object = object[:-1]
        copytree(object, build_path + path.basename(object))
    elif path.isfile(object):
        copyfile(object, build_path + path.basename(object))

print '\tCopying user-specified scripts...'

# copy over user scripts, if present
def copyscript(script_name, node_list):
    if not path.exists(script_name):
        raise_error('Script \'%s\' does not exist and could not be copied!' % script_name)
    script_base = path.basename(script_name)
    if '##' not in script_base:
        copyfile(script_name, build_path + script_base)
        system('chmod +x %s%s' % (build_path, script_base))
    else:
        with open(script_name, 'r') as original_script:
            original_script_lines = original_script.readlines()
        for node_name in node_list:
            with open('%s%s' % (build_path, script_base.replace('##', node_name)), 'w') as script_file:
                for line in original_script_lines:
                    script_file.write(line.replace('##', node_name))
            system('chmod +x %s%s' % (build_path, script_base.replace('##', node_name)))

if args.setup_script != None:
    node_list = all_nodes if not args.setup_script_client_only else client_nodes
    copyscript(args.setup_script, node_list)
if args.experimental_script != None:
    node_list = all_nodes if not args.experimental_script_client_only else client_nodes
    copyscript(args.experimental_script, node_list)
if args.cleanup_script != None:
    node_list = all_nodes if not args.cleanup_script_client_only else client_nodes
    copyscript(args.cleanup_script, node_list)

if len(custom_scripts) > 0:
    for script in custom_scripts:
        for target in script['targets']:
            copyscript(script['source'], targets_to_node_lists[target] if isinstance(target, str) else target)

print 'Writing .torrc files...'

with open(build_path + COMMON_TORRC_FILE_NAME, 'w') as common_file:
    common_file.write('TestingTorNetwork 1\nAllowInvalidNodes "entry,middle,exit,introduction,rendezvous"\n')
    common_file.write('ServerDNSAllowBrokenConfig 1\nServerDNSDetectHijacking 0\nNumCPUs 1\nSafeLogging 0\n')
    common_file.write('WarnUnsafeSocks 0\nContactInfo example@example.com\nDynamicDHGroups 0\n')
    common_file.write('DisableDebuggerAttachment 0\nCellStatistics 1\nDirReqStatistics 1\nEntryStatistics 1\n')
    common_file.write('ExitPortStatistics 1\nExtraInfoStatistics 1\nControlPort 9051\nCircuitPriorityHalflife 30\n')
    common_file.write('EnforceDistinctSubnets 0\nAssumeReachable 1\n')
    for x in xrange(0, num_authorities):
        split_fingerprint = ' '.join([authority_fingerprints[x][1][4 * y : 4 * y + 4] for y in xrange(0, len(authority_fingerprints[x][1]) / 4)])
        common_file.write('DirServer %s bridge v3ident=%s orport=9111 %s:9112 %s\n' % (AUTHORITY_NAME % x, authority_fingerprints[x][0], DUMMY_AUTHORITY_IP % x, split_fingerprint))

with open(build_path + RELAY_TORRC_FILE_NAME, 'w') as relay_file:
    relay_file.write('ORPort %i\nDirPort %i\nSocksPort 0\nExitPolicy "reject *:*"\n' % (OR_PORT, DIR_PORT))

with open(build_path + EXIT_TORRC_FILE_NAME, 'w') as exit_file:
    exit_file.write('ORPort %i\nDirPort %i\nSocksPort 0\nExitPolicy "accept *:*"\n' % (OR_PORT, DIR_PORT))

with open(build_path + AUTHORITY_TORRC_FILE_NAME, 'w') as auth_file:
    auth_file.write('AuthoritativeDirectory 1\nV2AuthoritativeDirectory 1\nV3AuthoritativeDirectory 1\n')
    auth_file.write('ORPort %i\nDirPort %i\nSocksPort 0\nExitPolicy "reject *:*"\n' % (OR_PORT, DIR_PORT))

with open(build_path + CLIENT_TORRC_FILE_NAME, 'w') as client_file:
    client_file.write('ORPort 0\nDirPort 0\nClientOnly 1\nSocksPort %i\nSocksListenAddress 127.0.0.1\n' % SOCKS_PORT)


print 'Writing scripts...'

print '\tWriting nginx setup script...'

with open(build_path + NGINX_SETUP_FILE_NAME, 'w') as nginx_file:
    nginx_file.write('sudo mkdir /experiment\n')
    nginx_file.write('sudo mkdir -p /etc/nginx/sites/default\n')
    nginx_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, NGINX_SOURCE_NAME))
    nginx_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, PCRE_SOURCE_NAME))
    nginx_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, ZLIB_SOURCE_NAME))
    nginx_file.write('cd /experiment\n')
    nginx_file.write('sudo tar xzf %s\n' % NGINX_SOURCE_NAME)
    nginx_file.write('sudo tar xzf %s\n' % PCRE_SOURCE_NAME)
    nginx_file.write('sudo tar xzf %s\n' % ZLIB_SOURCE_NAME)
    nginx_file.write('cd /experiment/nginx-1.8.0\n')
    nginx_file.write('sudo ./configure --with-pcre=../pcre-8.37 --with-zlib=../zlib-1.2.8\n')
    nginx_file.write('sudo make\n')
    nginx_file.write('sudo make install\n')
    nginx_file.write('cd /experiment\n')
    nginx_file.write('sudo rm -r nginx-1.8.0 pcre-8.37 zlib-1.2.8\n')
    nginx_file.write('sudo cp %s%s%s /usr/local/nginx/conf/nginx.conf\n' % (deployment_prefix, build_path, NGINX_CONF_FILE_NAME))
    nginx_file.write('sudo /usr/local/nginx/sbin/nginx > %s%s%s`hostname | tr . \'\\t\' | awk \'{print $1}\'`-%s\n' % (deployment_prefix, build_path, LOG_FOLDER, NGINX_LOG_FILE_NAME))

system('chmod +x %s%s' % (build_path, NGINX_SETUP_FILE_NAME))

print '\tWriting Tor setup scripts...'

def write_node_file(node_name, client = False):
    with open(build_path + TOR_SETUP_FILE_NAME % node_name, 'w') as node_file:
        node_file.write('sudo mkdir /experiment\n')
        node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, TOR_EXECUTABLE_NAME))
        node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, GEOIP_FILE_NAME))
        custom_torrc_file = COMMON_TORRC_FILE_NAME
        node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, COMMON_TORRC_FILE_NAME))
        if node_name[:10] == AUTHORITY_NAME[:10]:
            node_file.write('sudo cp -r %s%s%s /experiment\n' % (deployment_prefix, build_path, node_name))
            node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, AUTHORITY_TORRC_FILE_NAME))
            # node_file.write('sudo cp /proj/TorPerf/%s%s /experiment\n' % (build_path, V3BW_FILE_NAME))
            custom_torrc_file = AUTHORITY_TORRC_FILE_NAME
        elif node_name[:5] == RELAY_NAME[:5]:
            node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, RELAY_TORRC_FILE_NAME))
            custom_torrc_file = RELAY_TORRC_FILE_NAME
        elif node_name[:4] == EXIT_NAME[:4]:
            node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, EXIT_TORRC_FILE_NAME))
            custom_torrc_file = EXIT_TORRC_FILE_NAME
        elif node_name[:6] == CLIENT_NAME[:6]:
            node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, CLIENT_TORRC_FILE_NAME))
            custom_torrc_file = CLIENT_TORRC_FILE_NAME
        node_file.write('sudo chmod +x /experiment/%s\n' % TOR_EXECUTABLE_NAME)
        if node_name[:10] != AUTHORITY_NAME[:10]:
            node_file.write('sudo mkdir /experiment/%s\n' % node_name) # make a data directory
        for x in xrange(0, num_authorities):
            node_file.write('sudo sed -i s/%s/`cat /etc/hosts | grep %s | awk \'{print $1}\'`/ /experiment/%s\n' % (DUMMY_AUTHORITY_IP % x, AUTHORITY_NAME % x, COMMON_TORRC_FILE_NAME))
        if client:
            node_file.write('sudo cp %s%s%s /experiment\n' % (deployment_prefix, build_path, CURL_SOURCE_NAME))
            node_file.write('cd /experiment\n')
            node_file.write('sudo tar xzf %s\n' % CURL_SOURCE_NAME)
            node_file.write('cd /experiment/curl-7.43.0\n')
            node_file.write('sudo ./configure\n')
            node_file.write('sudo make\n')
            node_file.write('sudo make install\n')
            node_file.write('sudo ln -s /usr/local/lib/libcurl.so.4 /usr/lib/libcurl.so.4\n') # fix issue with curl not being able to find libcurl

        node_file.write('sudo /experiment/%s --Nickname %s --DataDirectory /experiment/%s --GeoIPFile /experiment/%s --defaults-torrc /experiment/%s -f /experiment/%s --BandwidthRate %i --BandwidthBurst %i > %s%s%s%s\n' % (TOR_EXECUTABLE_NAME, node_name, node_name, GEOIP_FILE_NAME, COMMON_TORRC_FILE_NAME, custom_torrc_file, DEFAULT_TOR_NODE_BANDWIDTH, DEFAULT_TOR_NODE_BANDWIDTH, deployment_prefix, build_path, LOG_FOLDER, TOR_LOG_FILE_NAME % node_name))
    system('chmod +x %s%s' % (build_path, TOR_SETUP_FILE_NAME % node_name))

for node in tor_nodes:
    write_node_file(node)

for x in xrange(0, num_authorities):
    write_node_file(AUTHORITY_NAME % x)

for x in xrange(0, num_clients):
    write_node_file(CLIENT_NAME % x, True)

print 'Compressing %s' % build_path

system('tar czf %s.tar.gz %s' % (build_path[:-1], build_path))