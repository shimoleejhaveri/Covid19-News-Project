# from django.db import models
# from django.models import Model
# from elasticutils.contrib.django import Indexable, MappingType

# class MyModel(Model):
#     # Django model ...


# class MyMappingType(MappingType):
#     @classmethod
#     def get_model(cls):
#         return MyModel


#     @classmethod
#     def get_mapping(cls):
#         """Returns an Elasticsearch mapping for this MappingType"""
#         return {
#             'properties': {
#                 # The id is an integer, so store it as such. Elasticsearch
#                 # would have inferred this just fine.
#                 'id': {'type': 'string'},

#                 'sourceName': {'type': 'string'},

#                 'description': {'type': 'string'},

#                 'author': {'type': 'string'},

#                 'title':{'type': 'string'},

#                 'url': {'type': 'string'},

#                 'publishedAt': {'type': 'string'},

#                 'createdAt':{'type': 'string'},

#                 'fetchedAt': {'type': 'string'},
#             }
#         }

#     @classmethod
#     def extract_document(cls, obj_id, obj=None):
#         """Converts this instance into an Elasticsearch document"""
#         if obj is None:
#             obj = cls.get_model().objects.get(pk=obj_id)

#         return {
#             'id': obj.id,
#             'sourceName': obj.sourceName,
#             'description': obj.description,
#             'author': obj.author,
#             'title': obj.title,
#             'url': obj.url,
#             'publishedAt': obj.publishedAt,
#             'createdAt': obj.createdAt,
#             'fetchedAt': obj.fetshedAt
#             }

# searcher = MyMappingType.search()
