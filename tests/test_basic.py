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


def test_load_multiple(tag_schema, tags_jsonapi):
    tags, errors = tag_schema().load(tags_jsonapi, many=True)
    assert errors == {}
    assert len(tags) == 3
    for tag in tags:
        assert 'tag' in tag


def test_load_multiple_set_on_schema(tag_schema, tags_jsonapi):
    tags, errors = tag_schema(many=True).load(tags_jsonapi)
    assert errors == {}
    assert len(tags) == 3
    for tag in tags:
        assert 'tag' in tag
