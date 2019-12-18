# luabins_py

A simple python library for encoding and decoding [luabins](https://github.com/agladysh/luabins) formatted serialized data.

## API

`def decode_luabins(stream: BytesIO) -> List[Any]`

Given a file-like object (here BytesIO, but a raw file pointer should work as well), this will return the list of values decoded from the file.

`def encode_luabins(values: List[Any]) -> bytes`

Given a set of values, it will serialize them to bytes in the luabins format.

Supported types are:
* String
* Int
* Float
* Dict
* List
* None
* Bool

## Limitations

In lua, arrays and maps have the same underlying representation, whereas in python, they're differentiated more. This means that you can serialize a list, but it will deserialize to a dict, where the keys are the original indexes, and there is some potential for weirdness there. 

I believe this library supports the full scope of the lua data model, so this mostly crops up if you try to do some weird python stuff.


