import faker
import pytest

from marshmallow import fields

from offline_jsonapi import Schema, Relationship

from faker import Factory

fake = Factory.create()


class PageSchema(Schema):

    id = fields.Int()
    title = fields.Str(required=True)
    text = fields.Str()
    author = Relationship(type_='authors',
                          schema='TagSchema',
                          required=True)
    comments = Relationship(type_='comments',
                            schema='CommentSchema',
                            required=True)

    class Meta():
        type_ = 'pages'


class CommentSchema(Schema):

    id = fields.Int()
    title = fields.Str(required=True)
    text = fields.Str()
    author = Relationship(type_='authors',
                          schema='TagSchema',
                          required=True)
    page = Relationship(type_='pages',
                        schema='PageSchema',
                        required=True)

    class Meta():
        type_ = 'comments'


class AuthorSchema(Schema):

    id = fields.Int()
    name = fields.Str(required=True)
    interests = Relationship(type_='tags',
                             schema='TagSchema',
                             many=True,
                             allow_none=True)

    class Meta():
        type_ = 'authors'


class TagSchema(Schema):

    id = fields.Int()
    tag = fields.Str(required=True)

    class Meta():
        type_ = 'tags'


@pytest.yield_fixture
def author_schema():
    yield AuthorSchema


@pytest.yield_fixture
def author_jsonapi():
    yield {'data': {'type': 'authors',
                    'id': str(fake.random_int()),
                    'attributes': {'name': fake.name()}}}


@pytest.yield_fixture
def tag_schema():
    yield TagSchema


@pytest.yield_fixture
def tag_jsonapi():
    yield {'data': {'type': 'tags',
                    'id': str(fake.random_int()),
                    'attributes': {'tag': fake.word()}}}


@pytest.yield_fixture
def tags_jsonapi():
    yield {'data': [{'type': 'tags',
                     'id': str(fake.random_int()),
                     'attributes': {'tag': fake.word()}} for _ in range(0, 3)]}


@pytest.yield_fixture
def author_with_interests_jsonapi(author_jsonapi, tags_jsonapi):
    author_jsonapi['data']['relationships'] = {'interests': {'data': [{'type': part['type'], 'id': part['id']} for part in tags_jsonapi['data']]}}
    author_jsonapi['included'] = tags_jsonapi['data']
    yield author_jsonapi


@pytest.yield_fixture
def comment_schema():
    yield CommentSchema


@pytest.yield_fixture
def comments_jsonapi(author_with_interests_jsonapi):
    pass


@pytest.yield_fixture
def page_schema():
    yield PageSchema
