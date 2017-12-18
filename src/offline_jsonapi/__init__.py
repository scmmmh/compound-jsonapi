"""
:mod:`offline_jsonapi`
======================

The :mod:`offline_jsonapi` provides two main classes:

* The :class:`~offline_jsonapi.schema.Schema` acts as the base-class for all
  specific schemas that are then used to serialise / deserialise data. Details
  of its public interface can be found at :class:`~marshmallow.Schema`.
* The :class:`~offline_jsonapi.fields.Relationship` is a custom field to define
  relationships between :class:`~offline_jsonapi.schema.Schema`.
"""
from .schema import Schema  # noqa:
from .fields import Relationship  # noqa:
