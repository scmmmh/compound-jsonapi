"""
:mod:`offline_jsonapi.fields`
=============================

Provides the :class:`~offline_jsonapi.fields.Relationship` custom field for
defining relationships between :class:`~offline_jsonapi.schema.Schema`\ s.

.. moduleauthor:: Mark Hall <mark.hall@work.room3b.eu>
"""
import marshmallow as ma

_RECURSIVE_NESTED = 'self'


class Relationship(ma.fields.Field):
    """The :class:`~offline_jsonapi.fields.Relationship` creates a link between
    two :class:`~offline_jsonapi.schema.Schema`. The linked
    :class:`~offline_jsonapi.schema.Schema` can either be provided as a class
    or a dotted classname string.
    """

    def __init__(self, schema, many=False, **kwargs):
        """
        :param schema: The :class:`~offline_jsonapi.schema.Schema` that defines
                       how to handle the linked data.
        :param many: By default the relationship is one-to-one. Set this to
                     ``true`` to create a one-to-many relationship
        :type many: ``bool``
        """
        super(Relationship, self).__init__(**kwargs)
        self.many = many
        self.__schema = schema
        self.follow = False

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
        self.__schema.include_schemas = self.root.include_schemas
        self.__schema._parent = self.root
        return self.__schema

    def _deserialize(self, value, attr=None, data=None):
        if self.many:
            return [(v['type'], v['id']) for v in value]
        else:
            return (value['type'], value['id'])

    def _serialize(self, value, attr=None, data=None):
        if self.schema.Meta.type_ in self.schema.include_schemas:
            visited = getattr(self.schema, '_visited')
            included_data = getattr(self.schema, '_included_data')
            if self.many:
                result = []
                for part in value:
                    if (self.schema.Meta.type_, str(part['id'])) not in visited:
                        visited.append((self.schema.Meta.type_, str(part['id'])))
                        included, errors = self.schema.dump(part, many=False)
                        included_data[(self.schema.Meta.type_, str(part['id']))] = included['data']
                    result.append({'type': self.schema.Meta.type_, 'id': str(part['id'])})
                return result
            else:
                if (self.schema.Meta.type_, str(value['id'])) not in visited:
                    visited.append((self.schema.Meta.type_, str(value['id'])))
                    included, errors = self.schema.dump(value, many=False)
                    included_data[(self.schema.Meta.type_, str(value['id']))] = included['data']
                return {'type': self.schema.Meta.type_, 'id': str(value['id'])}
        else:
            return None
