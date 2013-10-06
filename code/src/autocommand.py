# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand.py
#       Desc: 插件python部份
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: $version$
# LastChange: $lastChange$
# --------------------------------------------------
import os, re, sys, vim, json, time, types, locale, subprocess

configContent = ''

# 拦截对vim对象的直接访问，方便后期测试代码时模拟接口
def vimInterface(command, param):
  if command == 'eval':
    return vim.eval(param)
  elif command == 'command':
    return vim.command(param)

# 处理编码问题
formencoding = vimInterface('eval', '&enc').lower()
localeencoding = locale.getdefaultlocale()[1].lower()

# 获取配置文件名
def getCFileName():
  return vimInterface('eval', 'exists("b:acmd_config_name") ? b:acmd_config_name : g:acmd_config_name')

# 创建配置文件 createConfigFile {{{
def createConfigFile():
  # 获取配置文件名
  cFileName = getCFileName()
  global configContent
  # 初始化配置
  if not configContent:
    configContent = '''{
  "jade/": {
    "path": "~",
    "jade": {
      "command": [
        "jade -PO ../ jade/#{$fileName}.jade"
      ]
    }
  },
  "sass/": {
    "path": "~",
    "sass": {
      "command": [
        "sass --style compact sass/#{$fileName}.sass ../css/#{$fileName}.css"
         /* , "cp -fp ../css/#{$fileName}.css ../../public/css" */
      ]
    }
  },
  "coffee/": {
    "path": "~",
    "coffee": {
      "command":[
        "coffee -bp coffee/#{$fileName}.coffee>../js/#{$fileName}.js"
         /* , "cp -fp ../js/#{$fileName}.js ../../public/js" */
      ]
    }
  }
}
/* vim:ft=javascript ts=2 sts=2 sw=2 et
*/
'''
  # 写入配置
  fp = open(cFileName, 'w')
  fp.write(configContent)
  # 关闭文件
  fp.close()
  del fp

  return True;
# }}}

# 获取配置件 getConfig {{{
def getConfig(cPath):
  # 相对路径
  aPath = ''
  # 绝对路径
  rPath = ''
  # 是否读取到配置文件
  isConfig = False
  # 获取配置文件名
  cFileName = getCFileName()

  temp = os.path.split(cPath);
  if not temp[1]:
    path = temp[0]
  else:
    path = cPath

  for i in range(0, 3):
    if os.path.isdir(path):
      if os.path.isfile(path + '/' + cFileName):
        isConfig = True
        cPath = path+'/'
        break
      else:
        temp = os.path.split(path)
        path = temp[0]

        if temp[1] != '':
          aPath = temp[1]+'/'+aPath
          rPath += '../'
    else:
      break

  if isConfig:
    # 读取配置
    fp = open(cPath+'/'+cFileName)
    config = fp.read()
    fp.close()
    del fp
    # 去除注释
    rex = re.compile(r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
    config = rex.sub('', config).replace( '\\', '\\\\' )
    # 序列化Json
    config = json.loads(config)

    result = [config, cPath, aPath, rPath]
  else:
    result = [False, cPath, '', '']

  return result
# }}}

# 获取数据 getData {{{
def getData():
  # 获取文件相关信息
  fullFileName = vimInterface('eval', 'b:fullFileName')
  if os.name == 'nt': fullFileName = fullFileName.replace('\\', '/')

  fullFileName = fullFileName.decode(formencoding)

  tmpData = re.match(r'^(.*?|)([^/]+?)(?:\.)([^.]+|)$', fullFileName)
  tmpData = tmpData.groups()
  filePath = tmpData[0]
  fileName = tmpData[1]
  fileSuffix = tmpData[2]

  #if formencoding != localeencoding:
    #filePath = filePath.decode(formencoding).encode(localeencoding)
    #if autoencode == '1':
      #fileName = fileName.decode(formencoding).encode(localeencoding)

  result = [fullFileName, filePath, fileName, fileSuffix]

  return result
# }}}

# 获取缓存 getCache {{{
def getCache():
  command=''
  commandPath=''
  commandCache=vimInterface('eval', 'b:commandCache')

  if commandCache:
    commandCache = commandCache.decode(formencoding)
    command = re.split(r'(?<!\\)\|', commandCache)
    for i in range(0, len(command)):
      if command[i].find('|')>-1:
        command[i] = command[i].replace( '\|', '|' )

    if command[0].find('@')==0:
      commandPath = command[0].lstrip('@')
      del command[0]

  return [commandPath, command]
# }}}

# 设置缓存 setCache {{{
def setCache(commandPath, command):

  tmpCommand = ''
  if commandPath:
    tmpCommand = '@'+commandPath

  for i in range(0, len(command)):
    tmpCommand += '|'+command[i].replace( '|', r'\\|' )

  tmpCommand = 'let b:commandCache="'+tmpCommand+'"'
  tmpCommand = tmpCommand.encode(formencoding)

  vimInterface('command', tmpCommand)

  return True
# }}}

# 获取命令 getCommand {{{
def getCommand():
  commandName = ''
  commandPath, command = getCache()
  # 缓存为空
  if not command:
    fullFileName, filePath, fileName, fileSuffix = getData()
    config, cmdPath, aPath, rPath = getConfig(filePath)

    # 如果读取配失败则返回False
    if not config:
      # 如果未从配置文件取到命令则从vim中读取命令
      command = vimInterface('eval', 'autocommand#getCommand("'+fileSuffix+'")')
      # 命令数组
      if command.find('|') > -1:
        # 以|拆分
        command = re.split(r'(?<!\\)\|', command)
        for i in range(0, len(command)):
          if command[i].find('|')>-1:
            command[i] = command[i].replace( '\|', '|' )

        if command[0].find('@') == 0:
          commandPath = command[0].lstrip('@')
          del command[0]

      else:
        command = [command]
        commandPath = filePath

    # 处理配置文件
    else:
      # 当前路径
      if aPath:
        # 如果存在当前路径配置，当前路径配置中是否存在针对当前文件类型的配置
        if config.has_key(aPath) and config[aPath].has_key(fileSuffix):
          command = config[aPath][fileSuffix]['command']

          # 计算处理路径
          if config[aPath][fileSuffix].has_key('path'):
            commandPath = config[aPath][fileSuffix]['path']

          elif config[aPath].has_key('path'):
            commandPath = config[aPath]['path']

      # 如果未找到对应命令
      if not command:
        if config.has_key(fileSuffix):
          command = config[fileSuffix]['command']

      # 如果未找到指定路径
      if not commandPath:
        if config[fileSuffix].has_key('path'):
          commandPath = config[fileSuffix]['path']
        elif config.has_key('path'):
          commandPath = config['path']

      # 换算相对路径
      if commandPath:
        if commandPath[0] == '~':
          if commandPath > 1:
            commandPath = os.path.normpath(cmdPath+commandPath.lstrip('~'))

          elif len(commandPath) == 1:
            commandPath = cmdPath

        else:
          commandPath = os.path.normpath(filePath+commandPath)

        # 翻转换行
        if os.name == 'nt': commandPath = commandPath.replace('\\', '/')
        # 补反斜杠
        commandPath = re.sub(r'([^/])$', r'\1/', commandPath)
      else:
        commandPath = filePath

      if type(command) != types.ListType:
        command = [command]

    for i in range(0, len(command)):
      command[i] = command[i].replace('#{$fileName}', fileName)
      if aPath:
        command[i] = command[i].replace('#{$aPath}', aPath).replace('#{$rPath}', rPath)

    setCache(commandPath, command)

  # 获取执行命令的名称
  commandName = re.match(r'(^[^|> ]+)', command[0])
  if commandName:
    commandName = ' '+commandName.group()
  else:
    commandName = ' command'

  commandPath = commandPath.encode(localeencoding)

  return [commandPath, commandName, command]
# }}}

# 执行命令 runCommand {{{
def runCommand():
  errMsg = ''
  autoencode = vimInterface('eval', 'exists("b:acmd_auto_encode") ? b:acmd_auto_encode : g:acmd_auto_encode')
  commandPath, commandName, command = getCommand()

  # 改变路径
  if commandPath != '':
    tempPath = os.getcwd();
    os.chdir(commandPath);

  # 历遍命令数组，逐条执行
  for i in range(0, len(command)):
    #编码转换
    tmpcommand = command[i]
    if autoencode == '1':
      tmpcommand = tmpcommand.encode(localeencoding)
    else:
      tmpcommand = tmpcommand.encode(formencoding)

    # 执行命令
    ret = subprocess.Popen(tmpcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errMsg = ret.stderr.read()
    if errMsg != '': break

  # 返回初始目录
  if commandPath != '':
    os.chdir(tempPath)

  # 打印错误信息
  if errMsg:
    # 转义换行符、转义斜杠、转义引号
    errMsg = re.sub(r'\r(?:\n|)', r'\n', errMsg).replace('\\', '\\\\').replace('"', '\\"')

    if formencoding != localeencoding:
      #print 'errMsg.decode('+formencoding+').encode('+localeencoding+')'
      #print errMsg
      try:
        tErrMsg = errMsg.decode(localeencoding).encode(formencoding)
      except:
        tErrMsg = errMsg
      #tErrMsg = errMsg
    else:
      tErrMsg = errMsg

    # 打印错误命令
    vimInterface('command', 'echohl ErrorMsg | echo "'+tErrMsg+'" | echohl None')
  # 打印执行结果
  else:
    # 打印执行成功命令
    # print time.strftime('%H:%M:%S')+' execute'+commandName
    # 某些系统上gvim无法正确识别print指令，调过调用gvim的echo来实现打印
    vimInterface('command', 'ec "'+time.strftime('%H:%M:%S')+' execute'+commandName+'"')
# }}}

# build time $buildTime$
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
