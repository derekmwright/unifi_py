class Network:
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
        self._id = params['_id']
        self.name = params['name']
        self.site_id = params['site_id']
        self.purpose = params['purpose']

    def __repr__(self):
        return "%s(name='%s', purpose='%s')" % (
            type(self).__name__,
            self.name,
            self.purpose,
        )

class WAN(Network):
    """ WAN resource that has properties for wan connection settings.
    """
    def __init__(self, params):
        """ Returns a WAN network resource.
        """
        super().__init__(params)
        self.wan_ip = params['wan_ip']
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
        self.vlan_enabled = params['vlan_enabled']

class SiteVPN(Network):
    """ SiteVPN resource that has properties for VPN connections.
        TODO: Different VPN types might need to inherit from this...
    """
    def __init__(self, params):
        """ Returns a site vpn network resource.
        """
        super().__init__(params)
        self.enabled = params['enabled']
        self.ifname = params['ifname']
        self.vpn_type = params['vpn_type']
