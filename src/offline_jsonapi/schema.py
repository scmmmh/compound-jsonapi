import marshmallow as ma

from marshmallow import pre_load, pre_dump, post_dump

from .fields import Relationship


class Schema(ma.Schema):

    def __init__(self, include_schemas=None, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)
        self.include_schemas = dict([(s.Meta.type_, s()) for s in include_schemas]) if include_schemas else {}
        self.load_schemas = dict([(s.Meta.type_, s()) for s in include_schemas]) if include_schemas else {}
        self.load_schemas[self.Meta.type_] = self

    def _unwrap_single(self, data):
        data = data['data']
        result = {'id': data['id']}
        if 'attributes' in data:
            result.update(data['attributes'])
        if 'relationships' in data:
            for key, value in data['relationships'].items():
                if 'data' in value:
                    result[key] = value['data']
        return result

    @pre_load(pass_many=True)
    def _unwrap(self, data, many):
        if many:
            return [self._unwrap_single({'data': part}) for part in data['data']]
        else:
            return self._unwrap_single(data)

    def _do_load(self, data, many=None, partial=None, postprocess=True):
        many = self.many if many is None else bool(many)
        # Load the main data
        loaded, errors = super(Schema, self)._do_load(data, many=many, partial=partial, postprocess=postprocess)
        objs = {}
        if many:
            for part_source, part_loaded in zip(data['data'], loaded):
                objs[(part_source['type'], part_source['id'])] = ({'data': part_source}, part_loaded)
        else:
            objs[(data['data']['type'], data['data']['id'])] = (data, loaded)
        # Load the included data
        for part_source in data['included'] if 'included' in data else []:
            if part_source['type'] in self.load_schemas:
                part_loaded, errors = super(Schema, self.load_schemas[part_source['type']]).\
                    _do_load({'data': part_source}, many=False, partial=None, postprocess=True)
                objs[(part_source['type'], part_source['id'])] = ({'data': part_source}, part_loaded)
        # Fix the relationships
        for part_source, part_loaded in objs.values():
            schema = self.load_schemas[part_source['data']['type']]
            for field_name, validator in schema.fields.items():
                if isinstance(validator, Relationship):
                    links = validator.deserialize(part_source['data']['relationships'][field_name]['data']
                                                  if 'relationships' in part_source['data'] and
                                                  field_name in part_source['data']['relationships'] else None)
                    if links:
                        if isinstance(links, list):
                            if isinstance(part_loaded, dict):
                                part_loaded[field_name] = [objs[link][1] for link in links]
                            else:
                                setattr(part_loaded, field_name, [objs[link][1] for link in links])
                        else:
                            if isinstance(part_loaded, dict):
                                part_loaded[field_name] = objs[links][1]
                            else:
                                setattr(part_loaded, field_name, objs[links][1])
        return ma.UnmarshalResult(loaded, errors)

    @pre_dump(pass_many=True)
    def _init_dump(self, data, many):
        if not hasattr(self, '_visited'):
            setattr(self, '_visited', [])
        if not hasattr(self, '_included_data'):
            setattr(self, '_included_data', {})
        if not hasattr(self, '_parent'):
            if many:
                self._visited.extend([(self.Meta.type_, str(part['id'])) for part in data])
            else:
                self._visited.append((self.Meta.type_, str(data['id'])))

    def _wrap_single(self, data):
        result = {'data': {'type': self.Meta.type_,
                           'id': str(data['id']),
                           'attributes': {},
                           'relationships': {}}}
        for key, value in data.items():
            if key != 'id' and value is not None:
                if isinstance(self.fields[key], Relationship):
                    result['data']['relationships'][key] = value
                else:
                    result['data']['attributes'][key] = value
        if not result['data']['attributes']:
            del result['data']['attributes']
        if not result['data']['relationships']:
            del result['data']['relationships']
        return result

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        if many:
            result = {'data': [self._wrap_single(part)['data'] for part in data]}
        else:
            result = self._wrap_single(data)
        result['included'] = list(getattr(self, '_included_data').values())
        return result
