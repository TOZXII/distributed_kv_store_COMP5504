# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kvstore.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rkvstore.proto\x12\x07kvstore\"@\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x16\n\x0esource_node_id\x18\x03 \x01(\x05\"\x1e\n\x0bPutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"+\n\x0bGetResponse\x12\r\n\x05value\x18\x01 \x01(\t\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\"\x1c\n\rDeleteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"!\n\x0e\x44\x65leteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xae\x01\n\rKeyValueStore\x12\x30\n\x03Put\x12\x13.kvstore.PutRequest\x1a\x14.kvstore.PutResponse\x12\x30\n\x03Get\x12\x13.kvstore.GetRequest\x1a\x14.kvstore.GetResponse\x12\x39\n\x06\x44\x65lete\x12\x16.kvstore.DeleteRequest\x1a\x17.kvstore.DeleteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kvstore_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PUTREQUEST']._serialized_start=26
  _globals['_PUTREQUEST']._serialized_end=90
  _globals['_PUTRESPONSE']._serialized_start=92
  _globals['_PUTRESPONSE']._serialized_end=122
  _globals['_GETREQUEST']._serialized_start=124
  _globals['_GETREQUEST']._serialized_end=149
  _globals['_GETRESPONSE']._serialized_start=151
  _globals['_GETRESPONSE']._serialized_end=194
  _globals['_DELETEREQUEST']._serialized_start=196
  _globals['_DELETEREQUEST']._serialized_end=224
  _globals['_DELETERESPONSE']._serialized_start=226
  _globals['_DELETERESPONSE']._serialized_end=259
  _globals['_KEYVALUESTORE']._serialized_start=262
  _globals['_KEYVALUESTORE']._serialized_end=436
# @@protoc_insertion_point(module_scope)
