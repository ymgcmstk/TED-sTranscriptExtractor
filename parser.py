#!/usr/bin/env python
# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser, HTMLParseError
import sys
import os
import urllib2

def textdump(path, lines):
    f = open(path, 'w')
    for i in lines:
        f.write(i + '\n')
    f.close()

class TranscriptParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._transcript  = []
        self._title_flg = False
        self._flg = False
        self._author = ''
        self._title = ''
        self._curstr = ''
    def handle_starttag(self, tag, attrs):
        if dict(attrs).get('class', '') == 'talk-transcript__para__time' and not self._curstr == '':
            self._transcript.append(self._curstr)
            self._transcript.append('')
            self._curstr = ''
        if 'title' == tag:
            self._title_flg = True
        if ('span' == tag and dict(attrs).get('class', '') == 'talk-transcript__fragment'):
            self._flg = True
    def handle_endtag(self, tag):
        if 'title' == tag:
            self._title_flg = False
        if 'span' == tag:
            self._flg = False
    def handle_data(self, data):
        if self._title_flg:
            self._author = data.split(':')[0].replace(' ', '_')
            self._title = data.split(':')[1].replace(' ', '_')
            return
        if self._flg:
            self._curstr += data.replace('\n', ' ') + ' '
            return
    def save(self, path=None):
        self._transcript.append(self._curstr)
        if path is None:
            path = os.path.join(os.getcwd(), 'transcripts', '%s.txt' % self._author)
        textdump(path, self._transcript)

def main():
    url = sys.argv[1]
    assert 'ted.com' in url
    response = urllib2.urlopen(url)
    html     = response.read()
    response.close()
    parser = TranscriptParser()
    parser.feed(html)
    parser.close()
    parser.save()
    return

if __name__ == '__main__':
    main()
