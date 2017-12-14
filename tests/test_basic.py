def test_load_basic_schema(author_schema, author_jsonapi):
    '''Tests that loading a basic schema with no relationships works'''
    author, errors = author_schema().load(author_jsonapi)
    assert errors == {}
    assert author['id'] == int(author_jsonapi['data']['id'])
    assert author['name'] == author_jsonapi['data']['attributes']['name']


def test_load_basic_missing_field(author_schema, author_jsonapi):
    '''Tests that loading missing data leads to an error'''
    del author_jsonapi['data']['attributes']['name']
    author, errors = author_schema().load(author_jsonapi)
    assert errors == {'name': ['Missing data for required field.']}
