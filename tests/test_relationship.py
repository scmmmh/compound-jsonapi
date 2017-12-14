def test_load_single_parent_child_relationship(author_schema, tag_schema, author_with_interests_jsonapi):
    '''Tests that loading a basic schema with a one-to-many relationships works'''
    author, errors = author_schema(include_schemas=(tag_schema,)).load(author_with_interests_jsonapi)
    assert errors == {}
    assert author['id'] == int(author_with_interests_jsonapi['data']['id'])
    assert author['name'] == author_with_interests_jsonapi['data']['attributes']['name']
    assert len(author['interests']) == 3
    assert author['interests'][0]['tag'] == author_with_interests_jsonapi['included'][0]['attributes']['tag']
    assert author['interests'][1]['tag'] == author_with_interests_jsonapi['included'][1]['attributes']['tag']
    assert author['interests'][2]['tag'] == author_with_interests_jsonapi['included'][2]['attributes']['tag']


#def test_ignore_non_included_relationship(author_schema, author_with_interests_jsonapi):
#    '''Tests that loading a basic schema with a one-to-many relationships works'''
#    author, errors = author_schema().load(author_with_interests_jsonapi)
#    assert errors == {}
#    assert author['id'] == int(author_with_interests_jsonapi['data']['id'])
#    assert author['name'] == author_with_interests_jsonapi['data']['attributes']['name']
#    assert len(author['interests']) == 3
#    assert author['interests'][0]['tag'] == author_with_interests_jsonapi['included'][0]['attributes']['tag']
#    assert author['interests'][1]['tag'] == author_with_interests_jsonapi['included'][1]['attributes']['tag']
#    assert author['interests'][2]['tag'] == author_with_interests_jsonapi['included'][2]['attributes']['tag']


def test_circular_relationship(page_schema, comment_schema, author_schema, tag_schema, full_jsonapi):
    page, errors = page_schema(include_schemas=(comment_schema, author_schema, tag_schema)).\
        load(full_jsonapi)
    assert errors == {}
    assert page['title'] == full_jsonapi['data']['attributes']['title']
    assert not isinstance(page['author'], tuple)
    assert len(page['comments']) == 3
    assert not isinstance(page['comments'][0], tuple)
    assert not isinstance(page['comments'][1], tuple)
    assert not isinstance(page['comments'][2], tuple)
