import requests
import urllib3

import unifi
from unifi.error import Error
from unifi.error import ApiError
from unifi.site import Site
from unifi.network import Network

class Client:
    def __init__(
            self,
            username,
            password,
            hostname,
            port=8443,
            ssl=True,
            verify_ssl=False,
            remember=True,
            strict=True
        ):
        """ Returns a unifi API client.
        """
        self._controller = ''
        self.credentials = {
            'username': username,
            'password': password,
            'remember': remember,
            'strict': strict,
        }
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.controller = (hostname, port, ssl)
        self.session = requests.Session()
        self.login()

    def __repr__(self):
        return "Client(%s)" % (self.controller)

    def login(self):
        """ Login to the unifi API and set cookies for the session.
        """
        url = "{}/api/login".format(self.controller)
        try:
            req = self.session.post(url, json=self.credentials, verify=self.verify_ssl)
        except:
            return False
        return req.json()

    # Sites
    def get_sites(self):
        """ Returns a collection of sites from the API.
        """
        url = "{}/api/self/sites".format(self.controller)
        return [Site(site) for site in self.session.get(url).json()['data']]

    # System
    def get_system(self):
        """ Returns system properties from the API.
        """
        url = "{}/api/s/"


    # Networks
    def get_networks(self):
        """ Returns a collection of network resources from the API.
        """
        url = "{}/api/s/default/rest/networkconf".format(self.controller)
        nets = self.session.get(url).json()['data']
        return [getattr(unifi.network, Network.TYPES[net['purpose']])(net) for net in nets]

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
        _class = getattr(unifi.network, Network.TYPES[net['purpose']])
        return _class(net)

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
        return self._controller

    @controller.setter
    def controller(self, value):
        hostname, port, ssl = value
        scheme = 'https://' if ssl else 'http://'
        self._controller = "{}{}:{}".format(scheme, hostname, port)
