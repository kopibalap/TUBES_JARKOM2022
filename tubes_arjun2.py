#!/usr/bin/env python
#arjun 1301204219
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
import time
import os
if '__main__' == __name__:
	os.system('mn -c')
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)
	#arjun 1301204219
	#Add Host
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')

	#Add Router
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	#konfigurasi 1Mbps dan 500Kb
	
	bw1={'bw':1}
	bw2={'bw':0.5}

	#Add link 
	net.addLink(r1, h1, intfName1 = 'r1-eth0', intfName2 = 'h1-eth0', cls=TCLink, **bw1)
	net.addLink(r2, h1, intfName1 = 'r2-eth0', intfName2 = 'h1-eth1', cls=TCLink, **bw1)
	net.addLink(r3, h2, intfName1 = 'r3-eth0', intfName2 = 'h2-eth0', cls=TCLink, **bw1)
	net.addLink(r4, h2, intfName1 = 'r4-eth0', intfName2 = 'h2-eth1', cls=TCLink, **bw1)
	net.addLink(r1, r3, intfName1 = 'r1-eth2', intfName2 = 'r3-eth2', cls=TCLink, **bw2)
	net.addLink(r1, r4, intfName1 = 'r1-eth1', intfName2 = 'r4-eth1', cls=TCLink, **bw1)
	net.addLink(r2, r4, intfName1 = 'r2-eth2', intfName2 = 'r4-eth2', cls=TCLink, **bw2)
	net.addLink(r2, r3, intfName1 = 'r2-eth1', intfName2 = 'r3-eth1', cls=TCLink, **bw1)
	net.build()

	#Konfigurasi Host
	#host 1
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eht1 0")
	
	#host 2
	h1.cmd("ifconfig h1-eth0 192.168.0.2 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.1.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth0 192.168.6.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.7.2 netmask 255.255.255.0") 
	
	#Konfigurasi Router
	
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
	
	#router 1
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.0.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.4.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.2.1 netmask 255.255.255.0")

	#router 2
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.1.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.5.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.3.1 netmask 255.255.255.0")
	
	#router 3
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.6.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.5.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.2.2 netmask 255.255.255.0")

	#router 4
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.7.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.4.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.3.2 netmask 255.255.255.0")
	
	#Routing Host
	h1.cmd("ip rule add from 192.168.0.2 table 1")
	h1.cmd("ip rule add from 192.168.1.2 table 2")
	h1.cmd("ip route add 192.168.0.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.0.1 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.1.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.1.1 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.0.1 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev h1-eth1")
	
	h2.cmd("ip rule add from 192.168.6.2 table 1")
	h2.cmd("ip rule add from 192.168.7.2 table 2")
	h2.cmd("ip route add 192.168.6.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.6.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.7.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 192.168.7.1 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 192.168.6.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.7.1 dev h2-eth1")
	
	#Routing Router
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.4.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.6.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.7.0/24 gw 192.168.4.2")
	r1.cmd("route add -net 192.168.1.0/24 gw 192.168.2.2")

	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.5.2")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.5.2")
	r2.cmd("route add -net 192.168.6.0/24 gw 192.168.5.2")
	r2.cmd("route add -net 192.168.7.0/24 gw 192.168.3.2")
	r2.cmd("route add -net 192.168.4.0/24 gw 192.168.3.2")

	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.2.1")
	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.5.1")
	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.5.1")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.2.1")
	r3.cmd("route add -net 192.168.7.0/24 gw 192.168.5.1")

	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.4.1")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.3.1")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.4.1")
	r4.cmd("route add -net 192.168.5.0/24 gw 192.168.3.1")
	r4.cmd("route add -net 192.168.6.0/24 gw 192.168.4.1")
	
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 60ms")
	time.sleep(2)
	#arjun 1301204219
	# run background traffic
	#h2.cmd("iperf -s &") 
	#h1.cmd('iperf -t 20 -c 192.168.6.2 &')
	time.sleep(2)
	#h1.cmd("iperf -c 192.168.6.2") 
	#h2.cmd("tcpdump -w 1301204219.pcap &") 
	#h1.cmd("iperf -c 192.168.6.2 -t 100 &") 
	
	
	
	CLI(net)
	net.stop()
