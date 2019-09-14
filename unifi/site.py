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
