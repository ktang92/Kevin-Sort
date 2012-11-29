import re
import unicodedata
import urlparse
from urllib import quote, unquote

from url import URL

import unittest
suite = unittest.TestSuite()

""" from http://www.intertwingly.net/wiki/pie/PaceCanonicalIds """
tests1 = [
    (False, "http://:@example.com/"),
    (False, "http://@example.com/"),
    (False, "http://example.com"),
    (False, "HTTP://example.com/"),
    (False, "http://EXAMPLE.COM/"),
    (False, "http://example.com/%7Ejane"),
    (False, "http://example.com/?q=%C7"),
    (False, "http://example.com/?q=%5c"),
    (False, "http://example.com/?q=C%CC%A7"),
    (False, "http://example.com/a/../a/b"),
    (False, "http://example.com/a/./b"),
    (False, "http://example.com:80/"),
    (True, "http://example.com/"),
    (True, "http://example.com/?q=%C3%87"),
    (True, "http://example.com/?q=%E2%85%A0"),
    (True, "http://example.com/?q=%5C"),
    (True, "http://example.com/~jane"),
    (True, "http://example.com/a/b"),
    (True, "http://example.com:8080/"),
    (True, "http://user:password@example.com/"),

    # from rfc2396bis
    (True, "ftp://ftp.is.co.za/rfc/rfc1808.txt"),
    (True, "http://www.ietf.org/rfc/rfc2396.txt"),
    (True, "ldap://[2001:db8::7]/c=GB?objectClass?one"),
    (True, "mailto:John.Doe@example.com"),
    (True, "news:comp.infosystems.www.servers.unix"),
    (True, "tel:+1-816-555-1212"),
    (True, "telnet://192.0.2.16:80/"),
    (True, "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"),
    # other
    (True, "http://127.0.0.1/"),
    (False, "http://127.0.0.1:80/"),
    (True, "http://www.w3.org/2000/01/rdf-schema#"),
    (False, "http://example.com:081/"),
]
def test_validator(expected, value):

    class test(unittest.TestCase):

        def runTest(self):
            assert (URL(value).isValid()) == expected, \
                   (expected, value, URL(value).isValid())
    return test()

for (expected, value) in tests1:
    suite.addTest(test_validator(expected, value))


""" mnot test suite; three tests updated for rfc2396bis. """
tests2 = {
    '/foo/bar/.':
        '/foo/bar/',
    '/foo/bar/./':
        '/foo/bar/',
    '/foo/bar/..':
        '/foo/',
    '/foo/bar/../':
        '/foo/',
    '/foo/bar/../baz':
        '/foo/baz',
    '/foo/bar/../..':
        '/',
    '/foo/bar/../../':
        '/',
    '/foo/bar/../../baz':
        '/baz',
    '/foo/bar/../../../baz':
        '/baz', #was: '/../baz',
    '/foo/bar/../../../../baz':
        '/baz',
    '/./foo':
        '/foo',
    '/../foo':
        '/foo', #was: '/../foo',
    '/foo.':
        '/foo.',
    '/.foo':
        '/.foo',
    '/foo..':
        '/foo..',
    '/..foo':
        '/..foo',
    '/./../foo':
        '/foo', #was: '/../foo',
    '/./foo/.':
        '/foo/',
    '/foo/./bar':
        '/foo/bar',
    '/foo/../bar':
        '/bar',
    '/foo//':
        '/foo/',
    '/foo///bar//':
        '/foo/bar/',
    'http://www.foo.com:80/foo':
        'http://www.foo.com/foo',
    'http://www.foo.com:8000/foo':
        'http://www.foo.com:8000/foo',
    'http://www.foo.com./foo/bar.html':
        'http://www.foo.com/foo/bar.html',
    'http://www.foo.com.:81/foo':
        'http://www.foo.com:81/foo',
    'http://www.foo.com/%7ebar':
        'http://www.foo.com/~bar',
    'http://www.foo.com/%7Ebar':
        'http://www.foo.com/~bar',
    'ftp://user:pass@ftp.foo.net/foo/bar':
         'ftp://user:pass@ftp.foo.net/foo/bar',
    'http://USER:pass@www.Example.COM/foo/bar':
         'http://USER:pass@www.example.com/foo/bar',
    'http://www.example.com./':
        'http://www.example.com/',
    '-':
        '-',
    'http://lifehacker.com/#!5753509/hello-world-this-is-the-new-lifehacker':
        'http://lifehacker.com/?_escaped_fragment_=5753509/hello-world-this-is-the-new-lifehacker',
}

def test_normalizer(original, normalized):

    class test(unittest.TestCase):
        def runTest(self):
            assert URL(original).getNormalized() == normalized, \
                      (original, normalized, URL(original).getNormalized())
    return test()

for (original, normalized) in tests2.items():
    suite.addTest(test_normalizer(original, normalized))



tests3 = [
    #Normalized url comparison
    (True, '==', 'http://example.com/', 'http://example.com/'),
    (False, '<', 'http://example.com/', 'http://example.com/'),
    (False, '>', 'http://example.com/', 'http://example.com/'),

    #Value1 Non-Normalized, Value2 Normalized
    (True, '==', 'http://example.com', 'http://example.com/'),
    (False, '<', 'http://example.com', 'http://example.com/'),
    (False, '>', 'http://example.com', 'http://example.com/'),

    #Value1 Normalized, Value2 Non-Normalized
    (True, '==', 'http://example.com/', 'example.com/'),
    (False, '<', 'http://example.com/', 'example.com/'),
    (False, '>', 'http://example.com/', 'example.com/'),

    #Value1 Non-Normalized, Value2 Non-Normalized
    (False, '==', 'www.google.com', 'www.example.com'),
    (False, '<', 'www.google.com', 'www.example.com'),
    (True, '>', 'www.google.com', 'www.example.com')
]

def test_comparator(expected, comp, value1, value2):
    class test(unittest.TestCase):
        def runTest(self):
             url1 = URL(value1)
             url2 = URL(value2)
             if comp == '==':
                 assert (url1 == url2) == expected, \
                        (expected, comp, value1, value2)
             elif comp == '>':
                 assert (url1 > url2) == expected, \
                        (expected, comp, value1, value2)
             elif comp == '<':
                 assert (url1 < url2) == expected, \
                        (expected, comp, value1, value2)
            
    return test()

for (expected, comp, value1, value2) in tests3:
    suite.addTest(test_comparator(expected, comp, value1, value2))

""" execute tests """
unittest.TextTestRunner().run(suite)

