""" Manges settings within the unifi API.
"""

from .site import Site

class Settings:
    """ Top level settings management.
    """
    # Current setting "keys"
    _setting_keys = [
        'super_identity',
        'super_mgmt',
        'super_cloudaccess',
        'super_smtp',
        'connectivity',
        'guest_access',
        'ntp',
        'mgmt',
        'dpi',
        'usg',
        'country',
        'locale',
        'rsyslogd',
        'provider_capabilities',
        'auto_speedtest',
        'network_optimization',
    ]

    def __init__(self, client, site, section=None):
        self._client = client
        self.site = site
        if section in self._setting_keys:
            self._url = "s/{}/get/setting/{}".format(site.name, section)
        else:
            self._url = "s/{}/get/setting".format(site.name)

        # settings = list(
        #     map(
        #         lambda s:
        #         Section(self._client, s),
        #         self._client.get_api_resource(self._url)
        #     )
        # )
        for s in self._client.get_api_resource(self._url):
            setattr(self, s['key'], Section(self._client, s))

    def __repr__(self):
        return "%s(site=%s)" % (
            type(self).__name__,
            self.site.name,
        )

class Section:
    """ Unifi Configuration Sections, in the API they are called "keys".
        This term is a bit misleading so renaming to sections which contain
        groupings of key/value pairs related to each section.
    """
    def __init__(self, client, params):
        self._client = client
        self.key = params.pop('key')
        self._id = params.pop('_id')
        self.__set_kv(params)

    def __repr__(self):
        return "%s(%s)" % (
            type(self).__name__,
            self.key,
        )

    def __set_kv(self, kv):
        for k,v in kv.items():
            setattr(self, k, v)
