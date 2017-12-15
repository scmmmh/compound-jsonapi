def test_basic_export(author_schema, author_plain):
    author, errors = author_schema().dump(author_plain)
    assert errors == {}
    assert 'data' in author
    assert 'type' in author['data']
    assert author['data']['type'] == 'authors'
    assert 'id' in author['data']
    assert author['data']['id'] == str(author_plain['id'])
    assert 'attributes' in author['data']
    assert 'name' in author['data']['attributes']
    assert author['data']['attributes']['name'] == author_plain['name']

def test_basic_export_many(tag_schema, tags_plain):
    tags, errors = tag_schema(many=True).dump(tags_plain)
    assert errors == {}
    assert 'data' in tags
    assert len(tags['data']) == 3
    for tag in tags['data']:
        assert 'type' in tag
        assert tag['type'] == 'tags'
        assert 'id' in tag
        assert 'attributes' in tag
        assert 'tag' in tag['attributes']


def test_one_to_many_relationship(author_schema, author_with_interests_plain):
    author, errors = author_schema().dump(author_with_interests_plain)
    assert errors == {}
    assert 'data' in author
    assert 'type' in author['data']
    assert author['data']['type'] == 'authors'
    assert 'id' in author['data']
    assert author['data']['id'] == str(author_with_interests_plain['id'])
    assert 'attributes' in author['data']
    assert 'name' in author['data']['attributes']
    assert author['data']['attributes']['name'] == author_with_interests_plain['name']
    assert 'interests' not in author['data']['attributes']
    assert 'relationships' in author['data']
    assert 'interests' in author['data']['relationships']
    for interest in author['data']['relationships']['interests']:
        assert 'type' in interest
        assert 'id' in interest
        assert len(interest) == 2
    assert 'included' in author
    for included in author['included']:
        assert 'type' in included
        assert included['type'] == 'tags'
        assert 'id' in included
        assert 'attributes' in included
        assert 'tag' in included['attributes']
