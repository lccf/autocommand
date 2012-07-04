# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand.py
#       Desc: 插件python部份
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: 0.2
# LastChange: 07/04/2012 21:39
#    History: 
# --------------------------------------------------
import os, re, sys, vim, json, time, types, locale, subprocess

cFileName = '_config'

def createConfigFile():
  # 初始化配置
  config = '''{
  "haml": {
    "command": "haml -nq #{$fileName}.haml #{$fileName}.html"
    /* 执行命令 */
  },
  "sass": {
    "command": "sass #{$fileName}.sass #{$fileName}.css"
    /* 执行命令 */
  },
  "less": {
    "command": "lessc #{$fileName}.less>#{$fileName}.css"
    /* 执行命令 */
  },
  "coffee": {
    "command": "coffee -bp #{$fileName}.coffee>#{$fileName}.js"
    /* 执行命令 */
  }
}'''
  # 写入配置
  fp = open(cFileName, 'w')
  fp.write(config)
  # 关闭文件
  fp.close()
  del fp

  return True;

def readConfig(cPath):
  if os.path.isfile(cPath+'/'+cFileName):
    # 读取配置
    fp = open(cPath+'/'+cFileName)
    config = fp.read()
    fp.close()
    del fp
    # 去除注释
    rex = re.compile(r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
    config = rex.sub('', config)
    # 序列化Json
    config = json.loads(config)
  else:
    config = False

  return config

def getCommand(path, fname, suffix):
  config = readConfig(path)
  #如果读取配失败则返回False
  if not config:
    #如果未从配置文件取到命令则从vim中读取命令
    command = vim.eval('autocommand#getCommand("'+suffix+'")')
  else:
    #读取配置成功
    command = config[suffix]['command']
  if type(command) is types.ListType:
    command = '|'.join(command)
  command = re.sub(r'#{\$fileName}', fname, command)
  return command

#def getRelativePath(path):
  #relative = ''
  #prefix = ''
  #result = False
  #temp = ''

  #for i in range(0, 3):
    #if os.path.isdir(path):
      #if os.path.isfile(path + '/' + cFileName):
        #result = (path, relative)
        #break

      #else:
        #temp = os.path.split(path)
        #path = temp[0]
        #relative = temp[1]+'/'+relative

    #else:
      #break

  #return result

def runCommand():
  # 获取文件相关信息
  fullFileName = vim.eval('w:fullFileName')
  if os.name == 'nt':
    fullFileName = re.sub(r'\\', '/', fullFileName)
  result = re.match(r'^(.*/|)([^/]+?)(\.)([^.]+|)$', fullFileName)
  result = result.groups()
  filePath = result[0]
  fileName = result[1]
  fileSuffix = result[3]

  # 检测命令缓存
  commandCache = vim.eval('w:commandCache')
  if not commandCache:
    command=getCommand(filePath, fileName, fileSuffix)
    #print 'let w:commandCache='+command
    vim.command('let w:commandCache="'+command+'"')
  else:
    #print "use cache"
    command=commandCache

  # 处理编码问题
  formencoding = vim.eval('&enc').lower()
  localeencoding = locale.getdefaultlocale()[1].lower()
  autoencod = vim.eval( 'exists("w:acmd_auto_encode") ? w:acmd_auto_encode : g:acmd_auto_encode' )
  if formencoding != localeencoding:
    filePath = filePath.decode(formencoding).encode(localeencoding)
    if autoencod == 1:
      command = command.decode(formencoding).encode(localeencoding)

  # 命令数组
  if command.find('|') > -1:
    command = command.split('|')
  else:
    command = [command]

  commandName = ''

  # 改变路径
  if filePath != '':
    tempPath = os.getcwd();
    os.chdir(filePath);

  for i in range(0, len(command)):
    # 获取执行命令的名称
    if not commandName:
      commandName = re.match(r'(^[^|> ]+)', command[i])
      if commandName:
        commandName = ' '+commandName.group()
      else:
        commandName = ' command'
    # 执行命令
    ret = subprocess.Popen(command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errMsg = ret.stderr.read()
    if errMsg != '': break

  # 返回初始目录
  if filePath != '':
    os.chdir(tempPath)
  # 打印错误信息
  if errMsg:
    #转义换行符
    errMsg = re.sub(r'\r(?:\n|)', r'\n', errMsg)
    #转义斜杠
    errMsg = re.sub(r'\\', r'\\\\', errMsg)
    #转义引号
    errMsg = re.sub(r'\"', r'\\"', errMsg)
    #打印错误命令
    vim.command('echohl ErrorMsg | echo "'+errMsg+'" | echohl None')
  #打印执行结果
  else:
    #打印执行成功命令
    print time.strftime('%H:%M:%S')+' execute'+commandName

#if __name__ == '__main__':
  #print 'autoCommand.py is load'
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
