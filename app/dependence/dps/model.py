import ctypes

_userso = ctypes.cdll.LoadLibrary('./go/user.so')

User = _userso.User
