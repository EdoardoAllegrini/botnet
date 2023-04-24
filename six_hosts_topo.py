"""Custom topology example

six hosts network topology

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):

    def build( self ):
        "Create custom topo."

        hosts = []
        switches = []
        # Add hosts and switches
        for host in range(6):
            hosts.append(self.addHost(f"h{host+1}"))

        for switch in range(2):
            switches.append(self.addSwitch(f"s{switch+1}"))

        # Connect h1,h2,h3 to s1
        self.addLink(hosts[0], switches[0])
        self.addLink(hosts[1], switches[0])
        self.addLink(hosts[2], switches[0])

        # Connect h4,h5,h6 to s2
        self.addLink(hosts[3], switches[1])
        self.addLink(hosts[4], switches[1])
        self.addLink(hosts[5], switches[1])

        # Connect s1 to s2
        self.addLink(switches[0], switches[1])




topos = { 'mytopo': ( lambda: MyTopo() ) }