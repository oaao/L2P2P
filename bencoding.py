
# BENCODING TOKEN MARKERS
T_INTEGER       = b'i'
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
        pass

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
