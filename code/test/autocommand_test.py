#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand_test.py
#       Desc: 插件python部份 测试文件
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: 0.3(beta)
# LastChange: 08/01/2012 23:12
# --------------------------------------------------
import os, sys, re, json, shutil

acmd = False

# 测试创建配置文件
def testCreateConfigFile():
  print '\n[test] createConfigFile'

  isCreate = acmd.createConfigFile()
  testContent = acmd.configContent
  if isCreate:
    print '  create:success'
  else:
    print '  create:failure'

  try:
    fp = open(acmd.cFileName)
    readContent = fp.read()
  except:
    print '  read:failure'
    sys.exit()
  finally:
    fp.close()
    del fp

  print '  read:success'

  if testContent == readContent:
    print '  compare:equal'
  else:
    print '  compare:differ'

  try:
    os.unlink(acmd.cFileName)
    print '  remove:success'
  except:
    print '  remove:failure'
    sys.exit()

# 测试vim接口
def testVimInterface():
  print '\n[test] vimInterface'
  #print '[test]vimInterface eval:'+acmd.vimInterface('eval', 'test eval')
  print '  eval:'+acmd.vimInterface('eval', 'test eval')
  print '  command:'+acmd.vimInterface('command', 'test command')

# 测试获取配置文件
def testGetConfig():
  print '\n[test] getConfig'
  #暂存目录
  currDir = os.getcwd()

  if os.path.isdir('./testGetConfig'):
    shutil.rmtree('./testGetConfig')
  try:
    os.mkdir('testGetConfig')
    print '  create dir:./testGetConfig'
  except:
    print ' don\'t create dir:./testGetConfig'
    sys.exit()
  dirLv1 = os.path.realpath('./testGetConfig')
  #创建临时目录
  os.chdir(dirLv1)
  #创建测试配置文件
  acmd.createConfigFile()
  #获取1级目录配置文件读取值
  getResultLv1 = acmd.getConfig(dirLv1)
  #计算检验值
  rex = re.compile(r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
  jsons = rex.sub('', acmd.configContent)
  resultLv1 = [json.loads(jsons), dirLv1, '', '']
  #比较值输出结果
  if getResultLv1 == resultLv1:
    print '  current dir config:equal'
  else:
    print '  current dir config:differ'
    print '  [resultLv1]:'
    print '  '+str(resultLv1)
    print '  [getResultLv1]'
    print '  '+str(getResultLv1)

  #计算二级目录
  if os.path.isdir('./testGetConfigLv2'):
    shutil.rmtree('./testGetConfigLv2')
  try:
    os.mkdir('testGetConfigLv2')
    print '  create dir:./testGetConfigLv2'
  except:
    print ' don\'t create dir:./testGetConfigLv2'
    sys.exit()
  dirLv2 = os.path.realpath('./testGetConfigLv2')
  #创建临时目录
  os.chdir(dirLv2)
  #获取1级目录配置文件读取值
  getResultLv2 = acmd.getConfig(dirLv2)
  resultLv2 = [resultLv1[0], dirLv1, 'testGetConfigLv2/', '../']
  #比较值输出结果
  if getResultLv2 == resultLv2:
    print '  lv2 dir config:equal'
  else:
    print '  lv2 dir config:differ'
    print '  [resultLv2]:'
    print '  '+str(resultLv2)
    print '  [getResultLv2]'
    print '  '+str(getResultLv2)

  #计算三级目录
  if os.path.isdir('./testGetConfigLv3'):
    shutil.rmtree('./testGetConfigLv3')
  try:
    os.mkdir('testGetConfigLv3')
    print '  create dir:./testGetConfigLv3'
  except:
    print ' don\'t create dir:./testGetConfigLv3'
    sys.exit()
  dirLv3 = os.path.realpath('./testGetConfigLv3')
  #创建临时目录
  os.chdir(dirLv3)
  #获取3级目录配置文件读取值
  getResultLv3 = acmd.getConfig(dirLv3)
  resultLv3 = [resultLv1[0], dirLv1, 'testGetConfigLv2/testGetConfigLv3/', '../../']
  #比较值输出结果
  if getResultLv3 == resultLv3:
    print '  lv3 dir config:equal'
  else:
    print '  lv3 dir config:differ'
    print '  [resultLv3]:'
    print '  '+str(resultLv3)
    print '  [getResultLv3]'
    print '  '+str(getResultLv3)

  #清理复原
  os.chdir(currDir)
  if os.path.isdir('./testGetConfig'):
    shutil.rmtree(dirLv1)

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
  testCreateConfigFile()
  testVimInterface()
  testGetConfig()

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
