""" Client module instantiates a unifi client object for managing API calls
    to the unifi controller.
"""
import requests
import urllib3

from unifi.error import Error
from unifi.error import ApiError
from unifi.site import Site
from unifi.settings import Settings
from unifi.network import Network

class Client:
    """ Manages client connection and API calls to unifi controller.
    """
    def __init__(self, username, password, hostname, options=None):
        """ Returns a unifi API client.
        """
        valid_options = ['port', 'ssl', 'verify_ssl', 'remember', 'strict']
        option_defaults = {
            'port': 8443,
            'ssl': True,
            'verify_ssl': False,
            'remember': True,
            'strict': True,
        }

        # Set defaults or value provided via params
        if options:
            self.options = {key: (options[key] | option_defaults[key]) for key in valid_options}
        else:
            self.options = option_defaults

        self._controller = ''
        self.credentials = {
            'username': username,
            'password': password,
            'remember': self.options['remember'],
            'strict': self.options['strict'],
        }
        if not self.options['verify_ssl']:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.controller = (hostname, self.options['port'], self.options['ssl'])
        self.session = requests.Session()
        self.login()

    def __repr__(self):
        return "Client(%s)" % (self.controller)

    def login(self):
        """ Login to the unifi API and set cookies for the session.
        """
        url = "{}/api/login".format(self.controller)
        req = self.session.post(url, json=self.credentials, verify=self.options['verify_ssl'])
        if req.status_code > 399:
            raise ApiError(req)
        return req.json()

    def get_api_resource(self, suffix):
        """ Do a generic call to the API, must provide the url suffix
            for data you are expecting. Returns a list containing the
            resulting data.
        """
        url = "{}/api/{}".format(self.controller, suffix)
        req = self.session.get(url).json()
        if req['meta']['rc'] == 'ok':
            return req['data']
        raise ApiError(req['meta']['msg'])

    @staticmethod
    def __get_class(name):
        klass = getattr(__import__('unifi'), 'network')
        return getattr(klass, name)

    # Sites
    def get_sites(self):
        """ Returns a collection of sites from the API.
        """
        url = "{}/api/self/sites".format(self.controller)
        return [Site(site) for site in self.session.get(url).json()['data']]

    def get_site(self, name):
        return list(filter(lambda site: site.name == name, self.get_sites()))[0]

    # System
    def get_system(self, site):
        """ Returns system properties from the API.
        """
        url = "{}/api/s/{}/stat/sysinfo".format(self.controller, site.name)
        return self.session.get(url).json()['data'][0]

    # Settings
    def get_settings(self, site):
        url = "{}/api/s/{}/get/setting".format(self.controller, site.name)
        return self.session.get(url).json()['data']

    def get_setting(self, site, key):
        if key in self.setting_keys:
            url = "{}/api/s/{}/get/setting/{}".format(self.controller, site.name, key)
            return self.session.get(url).json()['data'][0]
        raise ApiError('Invalid Setting Key')

    # Networks
    def get_networks(self):
        """ Returns a collection of network resources from the API.
        """
        url = "{}/api/s/default/rest/networkconf".format(self.controller)
        nets = self.session.get(url).json()['data']
        return [self.__get_class(Network.TYPES[net['purpose']])(net) for net in nets]

    def get_network(self, _id):
        """ Returns a network resource from the API.
        """
        url = "{}/api/s/default/rest/networkconf/{}".format(self.controller, _id)
        net = self.session.get(url)
        print(net.json())
        if net.status_code > 399:
            raise ApiError(net)
        if not net.json()['data']: # API returns empty data when no resource exists
            raise Error("network object {} not found".format(_id))
        net = net.json()['data'][0]
        return self.__get_class(Network.TYPES[net['purpose']])(net)

    def delete_network(self, _id):
        """ Delete a network resource from the API.
        """
        self.get_network(_id)
        url = "{}/api/s/default/rest/networkconf/{}".format(self.controller, _id)
        headers = {'X-Csrf-Token': self.session.cookies['csrf_token']}
        net = self.session.delete(url, headers=headers)
        if net.status_code > 399:
            print(net.status_code)
            raise ApiError(net)
        return True

    # Set Unifi Controller
    @property
    def controller(self):
        """ Getter for custom setter.
        """
        return self._controller

    @controller.setter
    def controller(self, value):
        hostname, port, ssl = value
        scheme = 'https://' if ssl else 'http://'
        self._controller = "{}{}:{}".format(scheme, hostname, port)
