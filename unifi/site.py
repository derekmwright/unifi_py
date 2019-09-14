class Site(dict):

    def __init__(self, params):
        dict.__init__(
            self,
            _id=params['_id'],
            name=params['name'],
            desc=params['desc'],
            role=params['role'],
        )

    def __repr__(self):
        return "%s(name='%s', desc='%s', role='%s')" % (
            type(self).__name__,
            self['name'],
            self['desc'],
            self['role'],
        )
