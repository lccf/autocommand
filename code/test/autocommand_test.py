#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand_test.py
#       Desc: 插件python部份 测试文件
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: $version$
# LastChange: $lastChange$
# --------------------------------------------------
import os, sys

acmd = False

def testVimInterface():
  print '\n[test] vimInterface'
  #print '[test]vimInterface eval:'+acmd.vimInterface('eval', 'test eval')
  print '     eval:'+acmd.vimInterface('eval', 'test eval')
  print '  command:'+acmd.vimInterface('command', 'test command')

def loadAcmd():
  global acmd
  try:
    sys.path.insert(1, os.path.realpath('../src'))
    sys.path.insert(1, os.path.realpath('./'))
    acmd = __import__('autocommand')
  except ImportError:
    acmd = False
    print 'don\'t import autocommand'
    sys.exit()
  finally:
    sys.path.remove(os.path.realpath('../src'))
    sys.path.remove(os.path.realpath('./'))

def defaultTest():
  loadAcmd()
  print 'default'

def testTest():
  loadAcmd()
  testVimInterface()

if __name__ == '__main__':

  if len(sys.argv) < 2:
    testType = 'default'
  else:
    testType = sys.argv[1]

  if testType == 'default':
    defaultTest()
  elif testType == 'full':
    fullTest()
  elif testType == 'simple':
    simpleTest()
  elif testType == 'test':
    testTest()

# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
