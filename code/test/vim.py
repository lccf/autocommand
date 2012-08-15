#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
# b:fullFileName变量
vimFullFileName = False
# &enc变量
vimEnc = 'utf-8'
# b:acmd_auto_encode/g:acmd_auto_encode变量
vimAcmdAutoEncode = '1'
# b:commandCache变量
vimCommandCache = ''

def eval(param=''):
  if param == 'test eval':
    return 'success'
  elif param == 'b:fullFileName':
    return vimFullFileName
  elif param == '&enc':
    return vimEnc
  elif param == 'exists("b:acmd_auto_encode") ? b:acmd_auto_encode : g:acmd_auto_encode':
    return vimAcmdAutoEncode
  elif param == 'b:commandCache':
    return vimCommandCache
  else:
    return 'failure'

def command(param=''):
  if param == 'test command':
    return 'success'
  elif param.index('let b:commandCache') > -1:
    global vimCommandCache
    commandCache = re.match(r'let b:commandCache="(?P<commandCache>[^"]+)"', param)
    if commandCache and commandCache.group('commandCache'):
      vimCommandCache = commandCache.group('commandCache')
  else:
    return 'failure'
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
