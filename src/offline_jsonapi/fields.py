import marshmallow as ma

_RECURSIVE_NESTED = 'self'


class Relationship(ma.fields.Field):

    def __init__(self, schema, type_, many=False, **kwargs):
        super(Relationship, self).__init__(**kwargs)
        self.many = many
        self.__schema = schema
        self.type_ = type_

    def _schema_inherited_property(self, schema, name, default=None):
        try:
            return getattr(schema, name)
        except AttributeError:
            setattr(schema, name, getattr(self.root, name))
        return getattr(schema, name)

    @property
    def schema(self):
        if isinstance(self.__schema, ma.base.SchemaABC):
            pass
        elif isinstance(self.__schema, type) and issubclass(self.__schema, ma.base.SchemaABC):
            self.__schema = self.__schema()
        elif isinstance(self.__schema, ma.compat.basestring):
            if self.__schema == _RECURSIVE_NESTED:
                parent_class = self.parent.__class__
                self.__schema = parent_class()
            else:
                schema_class = ma.class_registry.get_class(self.__schema)
                self.__schema = schema_class()
        self._schema_inherited_property(self.__schema, '_visited', [])
        self._schema_inherited_property(self.__schema, '_included_data', {})
        self.__schema._parent = self.root
        return self.__schema

    def _deserialize(self, value, attr=None, data=None):
        if self.many:
            return [(v['type'], v['id']) for v in value]
        else:
            return (value['type'], value['id'])

    def _serialize(self, value, attr=None, data=None):
        visited = getattr(self.schema, '_visited')
        included_data = getattr(self.schema, '_included_data')
        if self.many:
            result = []
            for part in value:
                if (self.type_, str(part['id'])) not in visited:
                    visited.append((self.type_, str(part['id'])))
                    included, errors = self.schema.dump(part, many=False)
                    included_data[(self.type_, str(part['id']))] = included['data']
                result.append({'type': self.type_, 'id': str(part['id'])})
            return result
        else:
            if (self.type_, str(value['id'])) not in visited:
                visited.append((self.type_, str(value['id'])))
                included, errors = self.schema.dump(value, many=False)
                included_data[(self.type_, str(value['id']))] = included['data']
            return {'type': self.type_, 'id': str(value['id'])}
