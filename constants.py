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

from configuration import *

SOURCE_FOLDER = 'SUPPORT/'
AUTHORITY_RESOURCE_FOLDER = 'auth/'

LOG_FOLDER = 'logs/'
RESULTS_FOLDER = 'results/'

NGINX_SETUP_FILE_NAME = 'nginx-setup.sh'
TOR_SETUP_FILE_NAME = 'tor-%s.sh'
TOR_LOG_FILE_NAME = 'tor-%s.log'
NGINX_INSTALL_LOG_FILE_NAME = 'nginx-install.log'
NGINX_LOG_FILE_NAME = 'nginx.log'

NGINX_CONF_FILE_NAME = 'nginx.conf'
NGINX_SOURCE_NAME = 'nginx-1.8.0.tar.gz'
PCRE_SOURCE_NAME = 'pcre-8.37.tar.gz'
ZLIB_SOURCE_NAME = 'zlib-1.2.8.tar.gz'
CURL_SOURCE_NAME = 'curl-7.43.0.tar.gz'
TOR_EXECUTABLE_NAME = 'tor'
GEOIP_FILE_NAME = 'geoip'
FINGERPRINT_FILE = '/fingerprint'
AUTHORITY_CERTIFICATE = '/keys/authority_certificate'

COMMON_TORRC_FILE_NAME = 'tor.common.torrc'
AUTHORITY_TORRC_FILE_NAME = 'tor.authority.torrc'
RELAY_TORRC_FILE_NAME = 'tor.relay.torrc'
EXIT_TORRC_FILE_NAME = 'tor.exit.torrc'
CLIENT_TORRC_FILE_NAME = 'tor.client.torrc'

NS_FILE_NAME = 'simulator.ns'

SERVER_NAME = 'server%i'
CLIENT_NAME = 'client%i'
AUTHORITY_NAME = 'torthority%i'
RELAY_NAME = 'relay%i'
EXIT_NAME = 'exit%i'
INTERPOSER_NAME = 'interposer%s'

DUMMY_AUTHORITY_IP = 'AUTHIP%i'

LAN_NAME = 'centralan'
LOSSY_LINK_NAME = 'lossylink%s'

SERVER_PROGRAM_NAME = 'server%iprog'
TOR_NODE_PROGRAM_NAME = 'tor%sprog'
CLIENT_PROGRAM_NAME = 'setupclient%iprog'

USER_SETUP_PROGRAM_NAME = 'usersetup%sprog'
USER_EXPERIMENTAL_PROGRAM_NAME = 'userexp%sprog'
USER_CLEANUP_PROGRAM_NAME = 'usercleanup%sprog'
USER_CUSTOM_PROGRAM_NAME = 'uc%s%sp' # made shorter to avoid long name errors

MAX_SAFE_SCRIPT_NAME_LENGTH = 12 # this is hopefully conservative enough

ALL_TARGET = 'all'
CLIENT_TARGET = 'clients'
SERVER_TARGET = 'servers'
AUTHORITY_TARGET = 'authorities'
EXIT_TARGET = 'exits'
RELAY_TARGET = 'relays'
NON_EXIT_RELAYS_TARGET = 'non-exit-relays'

DEFAULT_OS = 'UBUNTU12-64-STD'

INFRASTRUCTURE_START_TIME = 0
TOR_START_TIME = 180
CLIENT_START_TIME = 360

DEFAULT_USER_SETUP_START_TIME = 600
DEFAULT_USER_SETUP_STOP_TIME = 900
DEFAULT_USER_EXPERIMENTAL_START_TIME = 1800
DEFAULT_USER_EXPERIMENTAL_STOP_TIME = 10800
DEFAULT_USER_CLEANUP_START_TIME = DEFAULT_USER_EXPERIMENTAL_STOP_TIME + 60
DEFAULT_USER_CLEANUP_STOP_TIME = DEFAULT_USER_CLEANUP_START_TIME + 300

NO_STOP_TIME = -1

MAX_AUTHORITIES = 20

DEPLOYMENT_PREFIX_BASE = '/proj/%s/'