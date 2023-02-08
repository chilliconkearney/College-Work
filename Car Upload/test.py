import pickle
import sys

class TestClass:
    def __init__(self, number):
        self.number = number

t1 = TestClass(14) # 
s1 = pickle.dumps(t1) # 
print(s1)
str_version = s1.decode('unicode_escape')
print(str_version)
decoded = pickle.loads(str_version.encode('utf-8', 'unicode_escape').replace(b'\xc2', b''))
print(decoded.number)