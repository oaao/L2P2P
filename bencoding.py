
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

        ch = self._peek()

        # token <--> action conditinoal rubric
        #     usually in the form of: 'consume' the marker token, then return relevant content
        if c is None:
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

        if self._index + 1 >= len(data):
            return None

        return self._data[self._i : self._i + 1]

    def _consume(self):
        """ Simulate the 'consumption' of a character by advancing the index """

        self._i += 1

    def _read(self, length: int) -> bytes:
        pass

    def _read_until(self, token: bytes) -> bytes:
        pass

    def _decode_int(self) -> int:
        return int(self._read_until(TOKEN_END))

    def _decode_list(self) -> list:

        l = []

        # recursively decode list contents
        while self._data[self._i : self._i + 1] != T_END:
            l.append(self.decode())

        self.consume()  # advance past the T_END token

        return l

    def _decode_dict(self):

        d = OrderedDict()

        while self._data[self._i : self._i +1] != T_END:
            key = self.decode()
            obj = self.decode()

            d[key] = obj

        self._consume()  # advance past the T_END token

        return d

    def _decode_string(self):

        to_read = int(self._read_until(T_STR_SEPARATOR))
        s       = self._read(to_read)

        return s

