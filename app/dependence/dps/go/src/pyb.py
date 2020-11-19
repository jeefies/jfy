import ctypes

so = ctypes.cdll.LoadLibrary('./base.so')


us = (['email', 'name', 'password', 'permission', 'sex', 'age', 'birth', 'locale', 'country', 'desc'],
        'ls n pwd prm sex age bth lcl cty des'.split()
        )
so.Init(us)

print(so.User.Get('email'))
print(so.User.Get('ls'))
