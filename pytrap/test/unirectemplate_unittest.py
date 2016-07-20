import unittest
import doctest

class DeviceTest(unittest.TestCase):
    def runTest(self):
        try:
            import pytrap
        except ImportError as e:
            self.fail(str(e))

class DataTypesIPAddr(unittest.TestCase):
    def runTest(self):
        import pytrap
        ip1 = pytrap.UnirecIPAddr("192.168.3.1")
        self.assertEqual(ip1, ip1)
        self.assertEqual(type(ip1), pytrap.UnirecIPAddr, "Bad type of IP address object.")
        self.assertEqual(str(ip1),  "192.168.3.1", "IP address is not equal to its str().")
        self.assertEqual(repr(ip1), "UnirecIPAddr('192.168.3.1')", "IP address is not equal to its repr().")

        self.assertTrue(ip1.isIPv4(),  "IPv4 was not recognized.")
        self.assertFalse(ip1.isIPv6(), "IPv4 was recognized as IPv6.")

        ip2 = pytrap.UnirecIPAddr("192.168.0.1")
        ip3 = pytrap.UnirecIPAddr("192.168.3.1")
        self.assertFalse(ip1 == ip2, "Comparison of different IP addresses failed.")
        self.assertFalse(ip1 <= ip2, "Comparison of the same IP addresses failed.")
        self.assertFalse(ip2 >= ip1, "Comparison of the same IP addresses failed.")
        self.assertFalse(ip1 != ip3, "Comparison of the same IP addresses failed.")
        self.assertFalse(ip1  < ip3, "Comparison of the same IP addresses failed.")
        self.assertFalse(ip1  > ip3, "Comparison of the same IP addresses failed.")

        ip1 = pytrap.UnirecIPAddr("fd7c:e770:9b8a::465")
        self.assertEqual(type(ip1), pytrap.UnirecIPAddr, "Bad type of IP address object.")
        self.assertEqual(str(ip1), "fd7c:e770:9b8a::465", "IP address is not equal to its str().")
        self.assertEqual(repr(ip1), "UnirecIPAddr('fd7c:e770:9b8a::465')", "IP address is not equal to its repr().")
        self.assertFalse(ip1.isIPv4(), "IPv6 was not recognized.")
        self.assertTrue(ip1.isIPv6(), "IPv6 was recognized as IPv4.")


class DataTypesTime(unittest.TestCase):
    def runTest(self):
        import pytrap
        t = pytrap.UnirecTime(1466701316, 123)
        self.assertEqual(type(t), pytrap.UnirecTime, "Bad type of Time object.")
        self.assertEqual(str(t),  "1466701316.123", "Time is not equal to its str().")
        self.assertEqual(repr(t), "UnirecTime(1466701316, 123)", "Time is not equal to its repr().")
        self.assertEqual(float(t), 1466701316.123, "Conversion of Time to float failed.")
        self.assertEqual(t, t)
        self.assertEqual(t.getSeconds(), 1466701316, "Number of seconds differs.")
        self.assertEqual(t.getMiliSeconds(), 123, "Number of miliseconds differs.")
        self.assertEqual(t.getTimeAsFloat(), 1466701316.123, "Time as float differs.")

        t2 = pytrap.UnirecTime(10, 100)
        self.assertEqual(type(t2), pytrap.UnirecTime, "Bad type of Time object.")
        self.assertEqual(str(t2),  "10.100", "Time is not equal to its str().")
        self.assertEqual(repr(t2), "UnirecTime(10, 100)", "Time is not equal to its repr().")

        self.assertFalse(t == t2)
        self.assertFalse(t <= t2)
        self.assertTrue(t  >= t2)
        self.assertTrue(t  != t2)
        self.assertFalse(t < t2)
        self.assertTrue(t  > t2)

        res1 = pytrap.UnirecTime(1466701326, 223)
        self.assertEqual(t + t2, res1)
        res2 = pytrap.UnirecTime(2466701316, 123)
        self.assertEqual(t + 1000000000, res2)
        res3 = pytrap.UnirecTime(466701316, 123)
        self.assertEqual(t + (-1000000000), res3)

        self.assertEqual(res1.format(), "2016-06-23T17:02:06Z")
        self.assertEqual(res1.format("%d.%m.%Y"), "23.06.2016")

class DataAccessGetTest(unittest.TestCase):
    def runTest(self):
        import pytrap
        a = pytrap.UnirecTemplate("ipaddr SRC_IP,time TIME_FIRST,uint32 ABC,uint32 BCD,string TEXT,bytes STREAMBYTES")
        data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x0A\x00\x00\x01\xff\xff\xff\xff\xc8\x76\xbe\xff\xe3\x2b\x6c\x57\x00\x00\x00\x01\x00\x00\x00\x02\x06\x00\x04\x00\x00\x00\x06\x00abcdef\xde\xad\xfe\xed')
        a.setData(data)
        self.assertEqual(len(a), 6, "Number of fields differs, 6 expected.")
        self.assertEqual(str(a), "(ipaddr SRC_IP,time TIME_FIRST,uint32 ABC,uint32 BCD,bytes STREAMBYTES,string TEXT)")
        d = a.getFieldsDict()
        self.assertEqual(type(d), dict)
        self.assertEqual(d, {'TIME_FIRST': 1, 'ABC': 2, 'BCD': 3, 'TEXT': 4, 'STREAMBYTES': 5, 'SRC_IP': 0})

        self.assertEqual(a.get(data, "SRC_IP"), pytrap.UnirecIPAddr("10.0.0.1"))
        self.assertEqual(a.get(data, "SRC_IP"), a.getByID(data, 0))
        self.assertEqual(a.get(data, "SRC_IP"), a.SRC_IP)

        self.assertEqual(a.get(data, "TIME_FIRST"), a.getByID(data, 1))
        self.assertEqual(a.get(data, "TIME_FIRST"), pytrap.UnirecTime(1466706915, 999))
        self.assertEqual(a.get(data, "TIME_FIRST"), a.TIME_FIRST)

        self.assertEqual(a.get(data, "ABC"), 16777216)
        self.assertEqual(a.get(data, "ABC"), a.getByID(data, 2))
        self.assertEqual(a.get(data, "ABC"), a.ABC)

        self.assertEqual(a.get(data, "BCD"), 33554432)
        self.assertEqual(a.get(data, "BCD"), a.getByID(data, 3))
        self.assertEqual(a.get(data, "BCD"), a.BCD)

        self.assertEqual(a.get(data, "TEXT"), "abcdef")
        self.assertEqual(a.get(data, "TEXT"), a.getByID(data, 4))
        self.assertEqual(a.get(data, "TEXT"), a.TEXT)
        self.assertEqual(type(a.get(data, "STREAMBYTES")), bytearray)
        self.assertEqual(a.get(data, "STREAMBYTES"), bytearray(b'\xde\xad\xfe\xed'))
        self.assertEqual(a.get(data, "STREAMBYTES"), a.getByID(data, 5))
        self.assertEqual(a.get(data, "STREAMBYTES"), a.STREAMBYTES)
        stream = a.get(data, "STREAMBYTES")
        self.assertEqual(" ".join([hex(i) for i in stream]), "0xde 0xad 0xfe 0xed")


class DataAccessSetTest(unittest.TestCase):
    def runTest(self):
        import pytrap
        a = pytrap.UnirecTemplate("ipaddr SRC_IP,time TIME_FIRST,uint32 ABC,uint32 BCD,string TEXT,bytes STREAMBYTES")
        data = a.createMessage(100)
        for i in range(100):
            self.assertEqual(data, a.getData())

        a.ABC = 666
        self.assertEqual(a.ABC, 666)
        a.SRC_IP = pytrap.UnirecIPAddr("147.32.1.1")
        self.assertEqual(a.SRC_IP, pytrap.UnirecIPAddr("147.32.1.1"))
        a.setByID(data, 0, pytrap.UnirecIPAddr("fd7c:e770:9b8a::465"))
        self.assertEqual(a.SRC_IP, pytrap.UnirecIPAddr("fd7c:e770:9b8a::465"))
        a.set(data, "SRC_IP", pytrap.UnirecIPAddr("10.0.0.1"))
        self.assertEqual(a.SRC_IP, pytrap.UnirecIPAddr("10.0.0.1"))

        a.TIME_FIRST = pytrap.UnirecTime(666, 0)
        self.assertEqual(a.TIME_FIRST, pytrap.UnirecTime(666, 0))
        a.setByID(data, 1, pytrap.UnirecTime(1234, 666))
        self.assertEqual(a.TIME_FIRST, pytrap.UnirecTime(1234, 666))
        a.set(data, "TIME_FIRST", pytrap.UnirecTime(1468962758, 166))
        self.assertEqual(a.TIME_FIRST, pytrap.UnirecTime(1468962758, 166))

        a.TEXT = "different text"
        self.assertEqual(a.TEXT, "different text")
        a.setByID(data, 4, "my long text")
        self.assertEqual(a.TEXT, "my long text")
        a.set(data, "TEXT", "long text")
        self.assertEqual(a.TEXT, "long text")

        a.STREAMBYTES = bytearray(b"he\x01\x01")
        self.assertEqual(a.STREAMBYTES, bytearray(b"he\x01\x01"))
        a.STREAMBYTES = bytes(b"\xca\xfe")
        self.assertEqual(a.STREAMBYTES, bytes(b"\xca\xfe"))
        a.setByID(data, 5, bytes(b"\xde\xad\xbe\xef"))
        self.assertEqual(a.STREAMBYTES, bytes(b"\xde\xad\xbe\xef"))

        data = a.createMessage(100)
        a.setByID(data, 2, int(1234))
        a.ABC = int(1)
        self.assertEqual(a.ABC, int(1))
        a.set(data, "ABC", int(666))
        self.assertEqual(a.ABC, int(666))
        a.ABC = int(222)
        self.assertEqual(a.ABC, int(222))
        # overflow
        a.ABC = int(4294967296)
        self.assertEqual(a.ABC, int(0))
