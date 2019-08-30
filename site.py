class Site:

    def __init__(
        self,
        params,
    ):
        self._id = params['_id']
        self.name = params['name']
        self.desc = params['desc']
        self.role = params['role']

    def __repr__(self):
        return "Site(name='%s', desc='%s', role='%s')" % (self.name, self.desc, self.role)
