class Site(dict):

    def __init__(self, params):
        super(Site, self).__init__(params)
        self._id = params['_id']
        self.name = params['name']
        self.desc = params['desc']
        self.role = params['role']

    def __repr__(self):
        return "%s(name='%s', desc='%s', role='%s')" % (
            type(self).__name__,
            self.name,
            self.desc,
            self.role,
        )

    @staticmethod
    def find_all(client):
        """ Get all sites via the API
        """
        return list(map(lambda s: Site(s), client.get_api_resource("self/sites")))

    @staticmethod
    def find_by(client, criterion, attr_name):
        """ Find a site by an attribute type. Example: _id, or name
        """
        # Just in case 'id' is passed instead of '_id'
        attr_name = '_id' if attr_name == 'id' else attr_name

        # Return a filtered list from the API, cannot find an API route to return a specific site.
        return list(filter(lambda s: getattr(s, attr_name) == criterion, Site.find_all(client)))[0]
