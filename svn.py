#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, os.path
from xml.dom import minidom
from . import util
from .core import logger

class svn:
    def __init__(self, path = None, url = None):
        self.path = path
        self.url = url

    def relative_path(self, path):
        return os.path.join(self.path, path)

    def info(self, path = None):
        if path is None:
            path = self.path

        output = util.run(['svn', 'info', path, '--xml'], output = False, fetch = True)[0]

        try:
            d = minidom.parseString(output)
        except:
            logger.error('get svn info error, cannot parse output xml, path: %s' % path)
            return False
        info = {}
        root = d.documentElement
        if len(root.getElementsByTagName('entry')) == 0:
            return False
        info['url'] = root.getElementsByTagName('url')[0].firstChild.data
        info['revision'] = root.getElementsByTagName('entry')[0].getAttribute('revision')
        info['uuid'] = root.getElementsByTagName('uuid')[0].firstChild.data
        if len(root.getElementsByTagName('schedule')):
            info['schedule'] = root.getElementsByTagName('schedule')[0].firstChild.data
        else:
            info['schedule'] = None
        if len(root.getElementsByTagName('author')):
            info['author'] = root.getElementsByTagName('author')[0].firstChild.data
        else:
            info['author'] = None
        if len(root.getElementsByTagName('date')):
            info['date'] = root.getElementsByTagName('date')[0].firstChild.data
        else:
            info['date'] = None
        return info

    '''
    run svn up
    '''
    def update(self, path = None):
        if path is None:
            path = self.path

        util.run(['svn', 'up', path])
        
    '''
    add all files to svn and prepare for commit
    '''
    def add_all(self, path = None):
        if path is None:
            path = self.path

        status_list = self.status(path)
        os.chdir(path)
        for f, s in status_list:
            if s == '?':
                util.run(['svn', 'add', f])
            elif s == '!':
                util.run(['svn', 'delete', f])
            elif s == 'M' or s == 'D' or s == 'A':
                continue
            else:
                logger.error('Unexcepted svn status, please fix it manually: [%s] %s' % (s, f))
                return False
        return True
        
    '''
    checkout svn repository
    '''
    def checkout(self, url = None, path = None):
        if url is None:
            url = self.url

        if path is None:
            path = self.path

        #cleanup
        if os.path.isdir(path):
            util.rmtree(path)
        
        #mkdir  
        if(not os.path.isdir(path)):
            os.makedirs(path)
        
        os.chdir(path)
        #checkout
        util.run(['svn','checkout', url, '.'])
        
    '''
    get svn status list
    '''
    def status(self, path = None):
        if path is None:
            path = self.path

        os.chdir(path)
        output = util.run(['svn', 'status'], output = False, fetch = True)[0]
        status_list = []
        
        for l in output.splitlines():
            l = l.strip()
            if len(l):
                status_list.append((l[1:].strip(), l[0]))
        return status_list
        
    '''
    run svn commit with custom message
    '''
    def commit(self, path = None, message = ''):
        if path is None:
            path = self.path

        os.chdir(path)
        util.run(['svn','commit','-m',message])
        return True