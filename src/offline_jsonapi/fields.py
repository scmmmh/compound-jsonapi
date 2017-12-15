import marshmallow as ma

_RECURSIVE_NESTED = 'self'


class Relationship(ma.fields.Field):

    def __init__(self, schema, type_, many=False, **kwargs):
        super(Relationship, self).__init__(**kwargs)
        self.many = many
        self.__schema = schema
        self.type_ = type_

    @property
    def schema(self):
        if isinstance(self.__schema, ma.base.SchemaABC):
            return self.__schema
        if isinstance(self.__schema, type) and issubclass(self.__schema, ma.base.SchemaABC):
            self.__schema = self.__schema()
            return self.__schema
        if isinstance(self.__schema, ma.compat.basestring):
            if self.__schema == _RECURSIVE_NESTED:
                parent_class = self.parent.__class__
                self.__schema = parent_class()
            else:
                schema_class = ma.class_registry.get_class(self.__schema)
                self.__schema = schema_class()
            return self.__schema
        else:
            raise ValueError(('A Schema is required to serialize a nested '
                              'relationship with include_data'))

    def _deserialize(self, value, attr=None, data=None):
        if value is None:
            return None
        else:
            if self.many:
                return [(v['type'], v['id']) for v in value]
            else:
                return (value['type'], value['id'])

    def _serialize(self, value, attr=None, data=None):
        included, errors = self.schema.dump(value, many=self.many)
        if self.many:
            self.root.include_data.extend(included['data'])
            return [{'type': self.type_, 'id': str(part['id'])} for part in value]
        else:
            self.root.include_data.append(included['data'])
            return {'type': self.type_, 'id': str(value['id'])}
