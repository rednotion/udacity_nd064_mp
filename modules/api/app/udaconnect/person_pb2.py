# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: person.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cperson.proto\"L\n\rPersonDetails\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x03 \x01(\t\"\x16\n\x08PersonID\x12\n\n\x02id\x18\x01 \x01(\x05\"T\n\tPersonRow\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\x05\")\n\nAllPersons\x12\x1b\n\x07results\x18\x01 \x03(\x0b\x32\n.PersonRow\"\x07\n\x05\x45mpty2s\n\x0ePersonEndpoint\x12$\n\x06\x43reate\x12\x0e.PersonDetails\x1a\n.PersonRow\x12\x1c\n\x03Get\x12\t.PersonID\x1a\n.PersonRow\x12\x1d\n\x06GetAll\x12\x06.Empty\x1a\x0b.AllPersonsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'person_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PERSONDETAILS._serialized_start=16
  _PERSONDETAILS._serialized_end=92
  _PERSONID._serialized_start=94
  _PERSONID._serialized_end=116
  _PERSONROW._serialized_start=118
  _PERSONROW._serialized_end=202
  _ALLPERSONS._serialized_start=204
  _ALLPERSONS._serialized_end=245
  _EMPTY._serialized_start=247
  _EMPTY._serialized_end=254
  _PERSONENDPOINT._serialized_start=256
  _PERSONENDPOINT._serialized_end=371
# @@protoc_insertion_point(module_scope)
