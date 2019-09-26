
# BENCODING TOKEN MARKERS
T_INT           = b'i'
T_LIST          = b'l'
T_DICT          = b'd'
T_STR_SEPARATOR = b':'
T_END           = b'e'


class Decoder:
    """ Decode a bencoded byte sequence """

    def __init__(self, data: bytes):

        if not isinstance(data, bytes):
            raise TypeError('data must be of type bytes')

        self._data  = data
        self._i     = 0    # character index

    def decode(self):
        """
        Decode bencoded data and return the corresponding Python datatype

        :return A python object representing the bencoded data
        """

        c = self._peek()

        # token <--> action conditinoal rubric
        #     usually in the form of: 'consume' the marker token, then return relevant content
        if   c is None:
            raise EOFError('Unexpected EOF')
        elif c == T_INT:
            self._consume()
            return self._decode_int()
        elif c == T_LIST:
            self._consume()
            return self._decode_list()
        elif c == T_DICT:
            self._consume()
            return self._decode_dict()
        elif c in b'0123456789':
            return self._decode_string()
        elif c == T_END:
            return None
        else:
            raise RuntimeError(f'Invalid token read at position {str(self._i)}')

    def _peek(self) -> bytes:
        """ Return the next character from the bencoded data, or None """

        if self._i + 1 >= len(self._data):
            return None

        return self._data[self._i : self._i + 1]

    def _consume(self):
        """ Simulate the 'consumption' of a character by advancing the index """

        self._i += 1

    def _read(self, length: int) -> bytes:
        """ Read the {length} number of bytes and return that result """

        if self._i + length > len(self._data):
            raise IndexError(
                f'Cannot read {str(length)} bytes from current position: {str(self._i)}'
            )

        data = self._data[self._i : self._i + length]

        self._i += length

        return data

    def _read_until(self, token: bytes) -> bytes:
        """ Read from bencoded data until given token is found, and return read characters """

        try:
            occurs_at = self._data.index(token, self._i)
            chars     = self._data[self._i : occurs_at]

            self._i = occurs_at +1

            return chars

        except ValueError:
            raise RuntimeError(f'Unable to find token: {str(token)}')

    def _decode_int(self) -> int:
        return int(self._read_until(T_END))

    def _decode_list(self) -> list:

        l = []

        # recursively decode list contents
        while self._data[self._i : self._i + 1] != T_END:
            l.append(self.decode())

        self._consume()  # advance past the T_END token

        return l

    def _decode_dict(self) -> dict:

        d = OrderedDict()

        while self._data[self._i : self._i +1] != T_END:
            key = self.decode()
            obj = self.decode()

            d[key] = obj

        self._consume()  # advance past the T_END token

        return d

    def _decode_string(self) -> str:

        read_length = int(self._read_until(T_STR_SEPARATOR))
        s           = self._read(read_length)

        return s

class Encoder:
    """
    Encode Python datatypes to a byte sequence

    (str, int, list, dict, bytes) - anything else is ignored

    """

    def __init__(self, data):
        self._data = data

    def encode(self) -> bytes:
        """
        Encode Python datatype to bencoded bstring

        :return bencoded binary data
        """
        return self.encode_next(self._data)

    def encode_next(self, data):

        if   type(data) == str:
            return self._encode_string(data)
        elif type(data) == int:
            return self._encode_int(data)
        elif type(data) == list:
            return self._encode_list(data)
        elif isinstance(dict):
            # type()       evaluates exact type
            # isinstance() accounts for inheritance chain - e.g. OrderedDict
            return self._encode_dict(data)
        elif type(data) == bytes:
            return self._encode_bytes(data)
        else:  # any other datatype we haven't added support for: cya kiddo
            return None

    def _encode_int(self, i: int) -> bytes:
        return str.encode(T_INT + str(value) + T_END)

    def _encode_str(self, s: str) -> bytes:
        tokenized = str(len(s)) + T_STR_SEPARATOR + s
        return str.encode(tokenized)

    def _encode_bytes(self, b: str) -> bytes:

        content =  bytearray()
        content += str.encode(str(len(b)))
        content += str.encode(T_STR_SEPARATOR)
        content += b

        return content

    def _encode_list(self, l: list) -> bytes:

        content =  bytearray(T_LIST, 'utf-8')
        content += b''.join([self.encode_next(item) for item in l])
        content += str.encode(T_END)

        return content

    def _encode_dict(self, d: dict) -> bytes:

        content  = bytearay(T_DICT, 'utf-8')

        for k, v in d.items():
            key = self.encode_next(k)
            val = self.encode_next(v)

            if key and val:
                content += key
                content += val
            else:
                raise RuntimeError(f'Malformed dictinoary:\n{d}')

        content ++ str.encode(T_END)

        return content