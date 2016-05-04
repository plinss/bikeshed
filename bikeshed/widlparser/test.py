#!/usr/bin/env python
# coding=utf-8
#
#  Copyright © 2013 Hewlett-Packard Development Company, L.P.
#
#  This work is distributed under the W3C® Software License [1]
#  in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  [1] http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
#

import sys
import itertools
import cgi

from widlparser import parser


def debugHook(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        pdb.pm()

class Marker(object):
    def markupConstruct(self, text, construct):
        return ('<' + construct.idlType + '>', '</' + construct.idlType + '>')

    def markupType(self, text, construct):
        return ('<TYPE for=' + construct.idlType + '>', '</TYPE>')

    def markupTypeName(self, text, construct):
        return ('<TYPE-NAME for=' + construct.idlType + '>', '</TYPE-NAME>')

    def markupName(self, text, construct):
        return ('<NAME for=' + construct.idlType + '>', '</NAME>')

    def markupKeyword(self, text, construct):
        return ('<KEYWORD for=' + construct.idlType + '>', '</KEYWORD>')

    def markupEnumValue(self, text, construct):
        return ('<ENUM-VALUE for=' + construct.idlType + '>', '</ENUM-VALUE>')

    def encode(self, text):
        return cgi.escape(text)


class NullMarker(object):
    def __init__(self):
        self.text = u''

    def markupConstruct(self, text, construct):
        return (None, None)

    def markupType(self, text, type):
        return (None, None)

    def markupTypeName(self, text, construct):
        return ('', '')

    def markupName(self, text, construct):
        return ('', '')

    def markupKeyword(self, text, construct):
        return ('', '')

    def markupEnumValue(self, text, construct):
        return ('', '')

    def encode(self, text):
        self.text += text
        return text


class ui(object):
    def warn(self, str):
        print str

    def note(self, str):
#        return
        print str

def testDifference(input, output):
    if (output == input):
        print "NULLIPOTENT"
    else:
        print "DIFFERENT"
        inputLines = input.split('\n')
        outputLines = output.split('\n')

        for inputLine, outputLine in itertools.izip_longest(inputLines, outputLines, fillvalue = ''):
            if (inputLine != outputLine):
                print "<" + inputLine
                print ">" + outputLine
                print


if __name__ == "__main__":      # called from the command line
    sys.excepthook = debugHook
    parser = parser.Parser(ui=ui())

    if (1 < len(sys.argv)):
        for fileName in sys.argv[1:]:
            print "Parsing: " + fileName
            file = open(fileName)
            parser.reset()
            text = file.read()
            parser.parse(text)
            assert (text == unicode(parser))
        quit()


    idl = u"""dictionary CSSFontFaceLoadEventInit : EventInit { sequence<CSSFontFaceRule> fontfaces = [ ]; };
interface Simple{
    serializer;
    serializer = { foo };
    serializer = { foo, bar };
    serializer = { inherit };
    serializer = { inherit, foo };
    serializer = { attribute };
    serializer = { inherit, attribute };
    serializer = { getter };
    serializer = [ foo ];
    serializer = [ foo, bar ];
    serializer = [ getter ];
    serializer = foo;
    serializer cereal(short one);
    iterable<Foo>;
    iterable<Foo, Bar>;
    readonly maplike<Foo, Bar>;
    setlike<Uint8ClampedArray>;
    attribute boolean required;
    static attribute Foo foo;
    static Foo foo();
    Promise<ReallyISwear>? theCheckIsInTheMail();
};"""
    idl += u""" // this is a comment éß
interface Multi : One  ,  Two   ,   Three     {
        attribute short one;
        attribute DOMString id setraises(DOMException);
};
typedef sequence<Foo[]>? fooType;
typedef (short or Foo) maybeFoo;
typedef sequence<(short or Foo)> maybeFoos;
typedef FrozenArray<(short or Foo)> frozenMaybeFoos;
interface foo {
  [one] attribute Foo one;
  [two] Foo two()bar;
  [three] const Foo three = 3}}foo
typedef   short    shorttype  = error this is;

   const  long    long   one=   2   ;
   const long hex = 0xabcdef09;
   const long octal = 0777;
   const double reallyHigh = Infinity;
   const double reallyLow = -Infinity;
   const double notANumber = NaN;
   const double invalid = - Infinity;
 Window   implements     WindowInterface  ; // more comment

enum   foo    {"one"  ,    "two",    }     ;
enum foo { "one" };
enum bar{"one","two","three",}; // and another
enum comments {
"one", //comment one
       // more comment
"two", //comment two
"three"  , //coment three
};

 typedef  short shorttype;
typedef long longtype;
typedef long long longtype;
[hello, my name is inigo montøya (you ] killed my father)] typedef unsigned long long inigo;
typedef unrestricted double dubloons;
typedef short [ ] shortarray;
typedef DOMString string;
typedef DOMString[] stringarray;
typedef foo barType;
typedef foo [ ] [ ]  barTypes;
typedef sequence<DOMString[]> sequins;
typedef sequence<DOMString[]>? sequinses;
typedef object obj;
typedef Date? today;
typedef (short or double) union;
typedef (short or sequence < DOMString [ ] ? [ ] > ? or DOMString[]?[] or unsigned long long or unrestricted double) craziness;
typedef (short or (long or double)) nestedUnion;
typedef (short or (long or double) or long long) moreNested;
typedef (short or sequence<(DOMString[]?[] or short)>? or DOMString[]?[]) sequenceUnion;

[ Constructor , NamedConstructor = MyConstructor, Constructor (Foo one), NamedConstructor = MyOtherConstructor (Foo two , long long longest ) ] partial interface Foo: Bar {
    unsigned long long method(short x, unsigned long long y, optional double inf = Infinity, optional sequence<Foo> fooArg = 123.4) raises (hell);
    unsigned long long method(DOMString string);
    void anotherMethod(short round);
    [ha!] attribute short bar getraises (an, exception);
    const short fortyTwo = 42;
    long foo(long x, long y);
}
[ NoInterfaceObject , MapClass (short, Foo )] interface LinkStyle {
    stringifier attribute DOMString mediaText;
    readonly attribute short bar;
    getter object (DOMString name);
    getter setter object bob(DOMString name);
    stringifier foo me(int x);
    stringifier foo ();
    stringifier;
    stringifier attribute short string;
    this is a syntax error, naturally
};
[foo] partial dictionary FooDict:BarDict {
    [one "]" ( tricky ] test)] short bar;
    [two] sequence<(double or Foo)> foo = "hello";
    required Foo baz;
}

callback callFoo = short();
callback callFoo2 = unsigned long long(unrestricted double one, DOMString two, Fubar ... three);
callback interface callMe {
    inherit attribute short round setraises (for the heck of it);
};

[Exposed=(Window, Worker)] dictionary MyDictionary {
    any value = null;
    any[] value = null;
    any [] value = null;
};

interface Int {
    readonly attribute long? service;
    readonly attribute ArrayBuffer? value;
    readonly attribute ArrayBuffer value2;
    attribute ArrayBuffer? value3;
};

"""
#    idl = idl.replace(' ', '  ')
    print "IDL >>>\n" + idl + "\n<<<"
    parser.parse(idl)
    print repr(parser)

    testDifference(idl, unicode(parser))
    assert(unicode(parser) == idl)

    print "MARKED UP:"
    marker = NullMarker()
    testDifference(idl, parser.markup(marker))
    assert(marker.text == idl)
    print parser.markup(Marker())

    print "Complexity: " + unicode(parser.complexityFactor)


    for construct in parser.constructs:
        print unicode(construct.idlType) + u': ' + unicode(construct.normalName)
        for member in construct:
            print '    ' + member.idlType + ': ' + unicode(member.normalName) + ' (' + unicode(member.name) + ')'

    print "FIND:"
    print parser.find('round').fullName
    print parser.find('Foo/method/y').fullName
    print parser.find('Foo.method').fullName
    print parser.find('Foo(constructor)').fullName
    print parser.find('longest').fullName
    print parser.find('fooArg').fullName
    print parser.find('Window').fullName
    print parser.find('mediaText').fullName
    print parser.find('Foo.method').markup(Marker())
    for method in parser.findAll('Foo.method'):
        print method.fullName

    print "NORMALIZE:"
    print parser.normalizedMethodName('foo')
    print parser.normalizedMethodName('unknown')
    print parser.normalizedMethodName('testMethod(short one, double two)')
    print parser.normalizedMethodName('testMethod2(one, two, and a half)')
    print parser.normalizedMethodName('bob(xxx)', 'LinkStyle')
    print parser.normalizedMethodName('bob')
    print parser.normalizedMethodName('bob()')
    print repr(parser.normalizedMethodNames('method', 'Foo'))

