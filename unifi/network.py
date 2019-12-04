# pylint: disable=E1101
""" Network module contains classes for different Unifi network types
"""
from ipaddress import ip_address, ip_network

class Network(dict):
    """ Generic network resource. This base class sets baseline properties
        and is inherited by the other network types. This class should not
        be directly instantiated. See TYPES constant for available network
        types that inherit from this class.
    """

    TYPES = {
        'wan': 'WAN',
        'corporate': 'Corporate',
        'site-vpn': 'SiteVPN',
    }

    def __init__(self, params):
        """ Returns a generic network resource.
        """
        super(Network, self).__init__(params)
        self._id = params['_id']
        self.name = params['name']
        self.site_id = params['site_id']
        self.purpose = params['purpose']

    def __repr__(self):
        return "%s(name='%s', purpose='%s')" % (
            type(self).__name__,
            self['name'],
            self['purpose'],
        )

class WAN(Network):
    """ WAN resource that has properties for wan connection settings.
    """
    def __init__(self, params):
        """ Returns a WAN network resource.
        """
        super().__init__(params)
        self.wan_ip = ip_address(params['wan_ip'])
        self.wan_networkgroup = params['wan_networkgroup']
        self.wan_type = params['wan_type']

class Corporate(Network):
    """ Corporate network resource that has properties for basic LAN
        settings.
    """
    def __init__(self, params):
        """ Returns a corporate network resource.
        """
        super().__init__(params)
        valid_params = [
            'ip_subnet',
            'ipv6_interface_type',
            'domain_name',
            'is_nat',
            'dhcpd_enabled',
            'dhcpd_start',
            'dhcpd_stop',
            'dhcpdv6_enabled',
            'ipv6_ra_enabled',
            'networkgroup',
            'upnp_lan_enabled',
            'dhcpguard_enabled',
            'dhcp_relay_enabled',
            'igmp_snooping',
            'dhcpd_unifi_controller',
            'dhcpd_leasetime',
            'dhcpd_gateway_enabled',
            'dhcpd_dns_enabled',
        ]

        for key in valid_params:
            if key in params:
                setattr(self, key, params[key])
            else:
                setattr(self, key, None)

    @property
    def gateway(self):
        """ Returns IPv4Address object representing the gateway address.
        """
        return ip_address(self.ip_subnet.split('/')[0])

    @property
    def network(self):
        """ Returns IPv4Network object representing the network.
        """
        return ip_network(self.ip_subnet, False)

class SiteVPN(Network):
    """ SiteVPN resource that has properties for VPN connections.
        TODO: Different VPN types might need to inherit from this...
    """
    def __init__(self, params):
        """ Returns a site vpn network resource.
        """
        super().__init__(params)
        valid_params = [
            'route_distance',
            'ipsec_profile',
            'remote_vpn_subnets',
            'ipsec_key_exchange',
            'ipsec_encryption',
            'ipsec_hash',
            'ipsec_dh_group',
            'ipsec_pfs',
            'ipsec_dynamic_routing',
            'ipsec_peer_ip',
            'ipsec_local_ip',
            'x_ipsec_pre_shared_key',
            'is_nat',
            'ifname',
        ]

        for key in valid_params:
            if key in params:
                setattr(self, key, params[key])
            else:
                setattr(self, key, None)
