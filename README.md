# L2P2P

## bencoding

See [references](#refs) below for a closer understanding of bencoding, as well as the broader BitTorrent specifications.

### decoding bencoded data

```python
>>> from bencoding import Decoder
>>>
>>> bencoded_int  = b'i12345e'
>>> bencoded_str  = b'9:bencoding'
>>> bencoded_list = b'l5:hello3:how3:are3:youi12345ee'
>>> bencoded_dict = b'd4:type4:dict8:told_you2:soe'
>>>
>>> from bencoding import Decoder, Encoder
>>> Decoder(bencoded_int).decode()
12345
>>> Decoder(bencoded_str).decode()
b'bencoding'
>>> Decoder(bencoded_list).decode()
[b'hello', b'how', b'are', b'you', 12345]
>>> Decoder(bencoded_dict).decode()
OrderedDict([(b'type', b'dict'), (b'told_you', b'so')])
```

### encoding bencoded data

```python
>>> from bencoding import Encoder
>>>
>>> i = 12345
>>> s = 'hi there thanks for stopping by'
>>> l = ['hi', 'there', 'thanks', 'for', 'checking', 'out', 'this', 'list']
>>> d = {'this': 'is', 'definitely': 'a', 'dict': 'type'}
>>> cx = ['everything', 101010, 'works', {'pretty': 'okay'}]
>>>
>>> Encoder(i).encode()
b'i12345e'
>>> Encoder(s).encode()
b'31:hi there thanks for stopping by'
>>> Encoder(l).encode()
bytearray(b'l2:hi5:there6:thanks3:for8:checking3:out4:this4:liste')
>>> Encoder(d).encode()
bytearray(b'd4:this2:is10:definitely1:a4:dict4:typee')
>>> Encoder(cx).encode()
bytearray(b'l10:everythingi101010e5:worksd6:pretty4:okayee')
```
## references <a name="refs"></a>

* [BitTorrent Protocol Specification v1.0](https://wiki.theory.org/index.php/BitTorrentSpecification) (unofficial)

* Markus Eliasson (Aug 2016): [A BitTorrent client in Python 3.5](https://markuseliasson.se/article/bittorrent-in-python/)
