# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: countplugin1.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='countplugin1.proto',
  package='countplugin1',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12\x63ountplugin1.proto\x12\x0c\x63ountplugin1\"\x1e\n\x05\x43ount\x1a\t\n\x07Request\x1a\n\n\x08Response\"0\n\x08GetCount\x1a\t\n\x07Request\x1a\x19\n\x08Response\x12\r\n\x05\x63ount\x18\x01 \x01(\x03\x32\x9a\x01\n\x07\x43ounter\x12\x42\n\x05\x43ount\x12\x1b.countplugin1.Count.Request\x1a\x1c.countplugin1.Count.Response\x12K\n\x08GetCount\x12\x1e.countplugin1.GetCount.Request\x1a\x1f.countplugin1.GetCount.Responseb\x06proto3')
)




_COUNT_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='countplugin1.Count.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=54,
)

_COUNT_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='countplugin1.Count.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=66,
)

_COUNT = _descriptor.Descriptor(
  name='Count',
  full_name='countplugin1.Count',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_COUNT_REQUEST, _COUNT_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=36,
  serialized_end=66,
)


_GETCOUNT_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='countplugin1.GetCount.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=54,
)

_GETCOUNT_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='countplugin1.GetCount.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='countplugin1.GetCount.Response.count', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=116,
)

_GETCOUNT = _descriptor.Descriptor(
  name='GetCount',
  full_name='countplugin1.GetCount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_GETCOUNT_REQUEST, _GETCOUNT_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=116,
)

_COUNT_REQUEST.containing_type = _COUNT
_COUNT_RESPONSE.containing_type = _COUNT
_GETCOUNT_REQUEST.containing_type = _GETCOUNT
_GETCOUNT_RESPONSE.containing_type = _GETCOUNT
DESCRIPTOR.message_types_by_name['Count'] = _COUNT
DESCRIPTOR.message_types_by_name['GetCount'] = _GETCOUNT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Count = _reflection.GeneratedProtocolMessageType('Count', (_message.Message,), {

  'Request' : _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
    'DESCRIPTOR' : _COUNT_REQUEST,
    '__module__' : 'countplugin1_pb2'
    # @@protoc_insertion_point(class_scope:countplugin1.Count.Request)
    })
  ,

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _COUNT_RESPONSE,
    '__module__' : 'countplugin1_pb2'
    # @@protoc_insertion_point(class_scope:countplugin1.Count.Response)
    })
  ,
  'DESCRIPTOR' : _COUNT,
  '__module__' : 'countplugin1_pb2'
  # @@protoc_insertion_point(class_scope:countplugin1.Count)
  })
_sym_db.RegisterMessage(Count)
_sym_db.RegisterMessage(Count.Request)
_sym_db.RegisterMessage(Count.Response)

GetCount = _reflection.GeneratedProtocolMessageType('GetCount', (_message.Message,), {

  'Request' : _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
    'DESCRIPTOR' : _GETCOUNT_REQUEST,
    '__module__' : 'countplugin1_pb2'
    # @@protoc_insertion_point(class_scope:countplugin1.GetCount.Request)
    })
  ,

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _GETCOUNT_RESPONSE,
    '__module__' : 'countplugin1_pb2'
    # @@protoc_insertion_point(class_scope:countplugin1.GetCount.Response)
    })
  ,
  'DESCRIPTOR' : _GETCOUNT,
  '__module__' : 'countplugin1_pb2'
  # @@protoc_insertion_point(class_scope:countplugin1.GetCount)
  })
_sym_db.RegisterMessage(GetCount)
_sym_db.RegisterMessage(GetCount.Request)
_sym_db.RegisterMessage(GetCount.Response)



_COUNTER = _descriptor.ServiceDescriptor(
  name='Counter',
  full_name='countplugin1.Counter',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=119,
  serialized_end=273,
  methods=[
  _descriptor.MethodDescriptor(
    name='Count',
    full_name='countplugin1.Counter.Count',
    index=0,
    containing_service=None,
    input_type=_COUNT_REQUEST,
    output_type=_COUNT_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetCount',
    full_name='countplugin1.Counter.GetCount',
    index=1,
    containing_service=None,
    input_type=_GETCOUNT_REQUEST,
    output_type=_GETCOUNT_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_COUNTER)

DESCRIPTOR.services_by_name['Counter'] = _COUNTER

# @@protoc_insertion_point(module_scope)
