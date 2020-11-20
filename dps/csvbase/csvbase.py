import base64

_csv_encode_trans = bytes.maketrans(b',', b'\x00')
_csv_decode_trans = bytes.maketrans(b'\x00', b',')

def csv_b85en(s):
    return base64.b85encode(s).translate(_csv_encode_trans)

def csv_b85de(s):
    return base64.b85decode(s.translate(_csv_decode_trans))

def csv_a85en(s):
    return base64.a85encode(s).translate(_csv_encode_trans)

def csv_a85de(s):
    return base64.a85decode(s.translate(_csv_decode_trans))
