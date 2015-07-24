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

#######################################################################
# This file contains constants that you may adjust to                 #
# alter the behavior of the generated experiment.                     #
#                                                                     #
# NB: You *MUST* set PROJECT_NAME to the name of the project          #
#  in EmuLab that this experiment will be run under or use -j!        #
#######################################################################

# The name of the EmuLab project under which the generated experiment will be run.
# Default value: none
# WARNING: you MUST either set this value or provide a value for -j
DEFAULT_PROJECT_NAME = 'PROJECT'

# The amount of bandwidth available to the LAN connecting all the nodes
# Default value: '10Mb'
# WARNING: large values (> 100Mb) may cause EmuLab issues when swapping in
DEFAULT_LAN_BANDWIDTH = '10Mb'

# The amount of bandwidth for the links connecting lossy nodes to the main LAN
# Default value: '10Mb'
DEFAULT_LINK_BANDWIDTH = '10Mb'

# The amount of bandwidth each Tor node considers itself to have, in BYTES
# Default value: 1000000
# WARNING: exceeding 10MB (10000000) will, due to the absence of a v3bw file, cause Directory Authorities to
#          disbelieve the bandwidth self-reporting from Tor relays in the experiment,
#          which may compromise your experiments
DEFAULT_TOR_NODE_BANDWIDTH = 1000000

# The queue type used by the Links and LAN connecting the nodes (for acceptable values, see EmuLab documentation)
# eg, for a Random Early Drop queue, set to 'RED'
# Default value: 'DropTail'
DEFAULT_QUEUE_TYPE = 'DropTail'

# The latency applied to packets traversing the LAN between all nodes, in milliseconds
# Default value: 50
DEFAULT_LAN_LATENCY = 50

# The additional latency applied to lossy nodes, in milliseconds
# This value should not need to be changed
# Default value: 0
DEFAULT_LINK_LATENCY = 0

# The default packet loss rate applied to ALL traffic
# eg '0' -> 0% packet loss; '02' -> 2% packet loss; '15' -> 15% packet loss
# Default value: 0
# WARNING: If nodes are marked as lossy with -l, the loss rate at those nodes will effectively be the SUM of this
#          loss rate and the loss rate indicated with -r, due to the generated network topology
DEFAULT_LOSS_RATE = '0'

# The ORPort used by all relevant Tor instances in the network
# Default value: 9111
# WARNING: setting this value to 0 will break Tor
OR_PORT = 9111

# The DirPort used by all relevant Tor instance in the network
# Default value: 9112
# WARNING: setting this value to 0 will break Tor
DIR_PORT = 9112

# The SocksPort used by the Tor clients
# Default value: 9050
# WARNING: must be non-zero to allow other applications to use Tor
SOCKS_PORT = 9000