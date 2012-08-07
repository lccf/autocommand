#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand_test.py
#       Desc: 插件python部份 测试文件
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: 0.3(beta)
# LastChange: 08/07/2012 01:22
# --------------------------------------------------
import os, sys, re, json, locale, shutil

# autocommand模块变量
acmd = False

# testCreateConfigFile 测试创建配置文件 {{{
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
# }}}

# testVimInterface 测试vim接口 {{{
def testVimInterface():
  print '\n[test] vimInterface'
  #print '[test]vimInterface eval:'+acmd.vimInterface('eval', 'test eval')
  print '  eval:'+acmd.vimInterface('eval', 'test eval')
  print '  command:'+acmd.vimInterface('command', 'test command')
# }}}

# testGetConfig 测试获取配置文件 {{{
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
  #resultLv1 = [json.loads(jsons), dirLv1, '', '.']
  #比较值输出结果
  if getResultLv1 == resultLv1:
    print '  test case 1:success'
  else:
    print '  test case 1:failure\n  [resultLv1]\n  %s\n  [getResultLv1]\n  %s' %(str(resultLv1), str(getResultLv1))
    sys.exit()

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
  #resultLv2 = [resultLv1[0], dirLv1, 'testGetConfigLv2/', '../.']
  #比较值输出结果
  if getResultLv2 == resultLv2:
    print '  test case 2:success'
  else:
    print '  test case 2:failure\n  [resultLv2]\n  %s\n  [getResultLv2]\n  %s' %(str(resultLv2), str(getResultLv2))
    sys.exit()

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
  #resultLv3 = [resultLv1[0], dirLv1, 'testGetConfigLv2/testGetConfigLv3/', '../../.']
  #比较值输出结果
  if getResultLv3 == resultLv3:
    print '  test case 3:success'
  else:
    print '  test case 3:failure\n  [resultLv3]\n  %s\n  [getResultLv3]\n  %s' %(str(resultLv3), str(getResultLv3))
    sys.exit()

  #清理复原
  os.chdir(currDir)
  if os.path.isdir('./testGetConfig'):
    shutil.rmtree(dirLv1)
# }}}

# testGetData 测试获取数据 {{{
def testGetData():
  print '\n[test] getData'
  pathName1 = './testGetData'
  pathName2 = './测试数据获取'
  fileName1 = 'readme.haml'
  fileName2 = '说明.haml'

  # test case 1
  # 针对情况：文件名及文件都为assic字符的情况下
  acmd.vim.vimFullFileName = os.path.realpath(pathName1 +'/'+ fileName1)
  getTc1Result = acmd.getData()
  tc1Result = [re.sub(r'\\', '/', os.path.realpath(pathName1 +'/'+ fileName1)), re.sub(r'\\', '/', os.path.realpath(pathName1))+'/', 'readme', 'haml']
  #tc1Result = [re.sub(r'\\', '/', os.path.realpath(pathName1 +'/'+ fileName1)), re.sub(r'\\', '/', os.path.realpath(pathName1))+'/', 'readme', 'haml.']

  if getTc1Result == tc1Result:
    print '  test case 1:success'
  else:
    print '  test case 1:failure\n  [tc1Result]\n  %s\n  [getTc1Result]\n  %s' %(str(tc1Result), str(getTc1Result))
    sys.exit()

  # test case 2
  # 针对情况：路径及文件名中带中文，且未开启文件名转码
  acmd.vim.vimFullFileName = os.path.realpath(pathName2 +'/'+ fileName2)
  getTc2Result = acmd.getData()
  codepage = locale.getdefaultlocale()[1].lower()
  tmp1 = re.sub( r'\\', '/', os.path.realpath(pathName2+'/'+fileName2))
  tmp2 = re.sub( r'\\', '/', os.path.realpath(pathName2).decode('utf-8').encode(codepage)+'/')
  tc2Result = [ tmp1, tmp2, re.sub( r'\.[^.]*$', '', fileName2).decode('utf-8').encode(codepage), 'haml' ]
  #tc2Result = [ tmp1, tmp2, re.sub( r'\.[^.]*$', '', fileName2).decode('utf-8').encode(codepage), 'haml.' ]

  if getTc2Result == tc2Result:
    print '  test case 2:success'
  else:
    print '  test case 2:failure\n  [tc2Result]\n  %s\n  [getTc2Result]\n  %s' %(str(tc2Result), str(getTc2Result))
    sys.exit()

  # test case 3
  # 针对情况：路径及文件名中带中文，且开启文件名转码
  acmd.vim.vimFullFileName = os.path.realpath(pathName2 +'/'+ fileName2)
  acmd.vim.vimAcmdAutoEncode = '0'
  getTc3Result = acmd.getData()
  codepage = locale.getdefaultlocale()[1].lower()
  tmp1 = re.sub( r'\\', '/', os.path.realpath(pathName2)+'/'+fileName2)
  tmp2 = re.sub( r'\\', '/', os.path.realpath(pathName2).decode('utf-8').encode(codepage)+'/')
  tc3Result = [ tmp1, tmp2, re.sub( r'\.[^.]*$', '', fileName2), 'haml' ]
  #tc3Result = [ tmp1, tmp2, re.sub( r'\.[^.]*$', '', fileName2), 'haml.' ]

  if getTc3Result == tc3Result:
    print '  test case 3:success'
  else:
    print '  test case 3:failure\n  [tc3Result]\n  %s\n  [getTc3Result]\n  %s' %(str(tc3Result), str(getTc3Result))
    sys.exit()
# }}}

# testSetCache 测试设置缓存 {{{
def testSetCache():
  print '\n[test] setCache'

  testPath = os.path.realpath('./testSetCache')
  # test case 1
  testCommand = ['haml -nq test.haml test.html', 'mv test.html ../']
  acmd.setCache(testPath, testCommand)
  tc1Result = '@'+re.sub(r'\\', '/', testPath)+'|'+'|'.join(testCommand)
  #tc1Result = '.@'+re.sub(r'\\', '/', testPath)+'|'+'|'.join(testCommand)
  getTc1Result = acmd.vim.vimCommandCache
  if getTc1Result == tc1Result:
    print '  test case 1:success'
  else:
    print '  test case 1:failure\n  [tc1Result]\n  %s\n  [getTc1Result]\n  %s' %(str(tc1Result), str(getTc1Result))
    sys.exit()

  acmd.vim.vimCommandCache=''

  # test case 2
  testCommand = ['sass te|st.sass te|st.css', 'mv te|st.css ../css']
  acmd.setCache(testPath, testCommand)
  tc2Result = '@'+re.sub(r'\\', '/', testPath)+'|'+re.sub( r'@', '|', re.sub( r'\|', '\|', '@'.join(testCommand)))
  #tc2Result = '.@'+re.sub(r'\\', '/', testPath)+'|'+re.sub( r'@', '|', re.sub( r'\|', '\|', '@'.join(testCommand)))
  getTc2Result = acmd.vim.vimCommandCache
  if getTc2Result == tc2Result:
    print '  test case 2:success'
  else:
    print '  test case 2:failure\n  [tc2Result]\n  %s\n  [getTc2Result]\n  %s' %(str(tc2Result), str(getTc2Result))
    sys.exit()

  acmd.vim.vimCommandCache=''

# }}}

# testGetCache 测试获取缓存 {{{
def testGetCache():
  print '\n[test] getCache'

  testPath = os.path.realpath('./testGetCache')
  # test case 1
  testCommand = ['haml -nq test.haml test.html', 'mv test.html ../']
  acmd.setCache(testPath, testCommand)
  tc1Result = [re.sub(r'\\', '/', testPath), testCommand]
  #tc1Result = [re.sub(r'\\', '/.', testPath), testCommand]
  getTc1Result = acmd.getCache()
  if getTc1Result == tc1Result:
    print '  test case 1:success'
  else:
    print '  test case 1:failure\n  [tc1Result]\n  %s\n  [getTc1Result]\n  %s' %(str(tc1Result), str(getTc1Result))
    sys.exit()

  acmd.vim.vimCommandCache=''

  # test case 2
  testCommand = ['sass te|st.sass te|st.css', 'mv te|st.css ../css']
  acmd.setCache(testPath, testCommand)
  tc2Result = '@'+re.sub(r'\\', '/', testPath)+'|'+re.sub( r'@', '|', re.sub( r'\|', '\|', '@'.join(testCommand)))
  #tc2Result = '.@'+re.sub(r'\\', '/', testPath)+'|'+re.sub( r'@', '|', re.sub( r'\|', '\|', '@'.join(testCommand)))
  getTc2Result = acmd.vim.vimCommandCache
  if getTc2Result == tc2Result:
    print '  test case 2:success'
  else:
    print '  test case 2:failure\n  [tc2Result]\n  %s\n  [getTc2Result]\n  %s' %(str(tc2Result), str(getTc2Result))
    sys.exit()

  acmd.vim.vimCommandCache=''

# }}}

# loadAcmd 加载autocommand模块 {{{
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
# }}}

def defaultTest():
  loadAcmd()
  print 'default'

def testTest():
  loadAcmd()
  testCreateConfigFile()
  testVimInterface()
  testGetConfig()
  testGetData()
  testSetCache()
  testGetCache()

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
