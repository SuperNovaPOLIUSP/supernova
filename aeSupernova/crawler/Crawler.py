"Generic Crawler object to read from a url"
# coding: utf8
import re
from BeautifulSoup import BeautifulSoup
import urllib2

MAXTRIES = 4


def removewhitespaces(string):
    "Removes whitespaces, newlines and carriage returns from string"
    return re.sub('\s', '', string)


def removewhitespacesstartandend(string):
    """Removes whitespaces, newlines and carriage from the start and end of a
    string"""
    string = re.sub('^\s', '', string)
    return re.sub('\s$', '', string)


def appendparameters(string, parameters):
    """Returns a string with each key and value from the dict parameters
    with the formatting: string?key1=value1&key2=value2&..."""
    string = string + '?'
    flag = False
    for key in parameters:
        if flag:
            string += '&'
        string += key + '=' + parameters[key]
        flag = True
    return string


def getwhatisbetweenthetags(entiretagstring):
    """Returns a string with the content that is described by the
    following format: <htmltag>content string<\htmltag>"""
    # Split the first '>'
    content = entiretagstring.split('>')[1]
    # Split the '<'
    content = content.split('<')[0]
    return removewhitespacesstartandend(content)


class Crawler(object):
    """Crawler Object with the following instance variables:

    htmlfile: Representing the object returned from urlopen
    htmltext: Representing a unicode string from the htmlFile"""

    def __init__(self):
        self.url = None
        self.htmlpage = None

    def loadpage(self, url):
        "Loads  html page from url at self.htmlfile and its text at htmltext"
        tries = 0
        while tries < MAXTRIES:
            try:
                htmltext = urllib2.urlopen(url)
                self.htmlpage = BeautifulSoup(htmltext)
                self.url = url
                return
            except urllib2.URLError:
                tries += 1

    def find(self, string):
        "Placeholder"
        string = string.decode('utf-8') + self.htmlpage
        return string
