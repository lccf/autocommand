#!/usr/bin/env python
# -*- coding:utf-8 -*-
# w:fullFileName变量
vimFullFileName = False
# &enc变量
vimEnc = 'utf-8'
# w:acmd_auto_encode/g:acmd_auto_encode变量
vimAcmdAutoEncode = '1'
# w:commandCache变量
vimCommandCache = ''

def eval(param=''):
  if param == 'test eval':
    return 'success'
  elif param == 'w:fullFileName':
    return vimFullFileName
  elif param == '&enc':
    return vimEnc
  elif param == 'exists("w:acmd_auto_encode") ? w:acmd_auto_encode : g:acmd_auto_encode':
    return vimAcmdAutoEncode
  else:
    return 'failure'

def command(param=''):
  if param == 'test command':
    return 'success'
  else:
    return 'failure'
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
