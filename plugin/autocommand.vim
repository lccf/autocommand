" --------------------------------------------------
"   FileName: autocommand.vim
"       Desc: 插件主文件
"     Author: lcc
"      Email: leftcold@gmail.com
"    Version: 0.3(beta)
" LastChange: 08/21/2012 21:14
" --------------------------------------------------
" 需python支持
if !has('python') | fini | en
" 关闭插件
if exists('g:acmd_loaded') && g:acmd_loaded==1 | fini | en
" python文件是否加载
let s:py_loaded=0
" 脚本目录
let s:scriptDir=expand('<sfile>:h')
" 调试模式
let s:isDebug=exists('g:acmd_debug') ? g:acmd_debug : 0
" 主函数
fu! autocommand#main()
  " 保存文件
  if exists('*Autocommand_before')
    if Autocommand_before(expand('%:p'))==0 | retu 0 | en
  en
  sil up
  " 调试状态重新加载文件，不使用缓存
  if s:isDebug==1 | cal autocommand#flush() | en
  " 判断窗口变量
  if !exists('b:fullFileName') | cal autocommand#initBuffer() | en
  " 执行命令
  py runCommand()
endf

" 加载autoCommand.py {{{
fu! autocommand#loadpy()
  let s:py_loaded=1
  if s:isDebug==1
    exe "pyfile ".s:scriptDir."/autocommand.py"
  el
python << EOF
# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand.py
#       Desc: 插件python部份
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: 0.3(beta)
# LastChange: 08/21/2012 21:14
# --------------------------------------------------
import os, re, sys, vim, json, time, types, locale, subprocess

configContent = ''

# 拦截对vim对象的直接访问，方便后期测试代码时模拟接口
def vimInterface(command, param):
  if command == 'eval':
    return vim.eval(param)
  elif command == 'command':
    return vim.command(param)

def getCFileName():
  return vimInterface('eval', 'exists("b:acmd_config_name") ? b:acmd_config_name : g:acmd_config_name')

def createConfigFile():
  # 获取配置文件名
  cFileName = getCFileName()
  global configContent
  # 初始化配置
  if not configContent:
    configContent = '''{
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
  fp.write(configContent)
  # 关闭文件
  fp.close()
  del fp

  return True;

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

def getData():
  # 获取文件相关信息
  fullFileName = vimInterface('eval', 'b:fullFileName')
  if os.name == 'nt': fullFileName = fullFileName.replace('\\', '/')

  tmpData = re.match(r'^(.*?|)([^/]+?)(?:\.)([^.]+|)$', fullFileName)
  tmpData = tmpData.groups()
  filePath = tmpData[0]
  fileName = tmpData[1]
  fileSuffix = tmpData[2]

  # 处理编码问题
  formencoding = vimInterface('eval', '&enc').lower()
  localeencoding = locale.getdefaultlocale()[1].lower()
  autoencode = vimInterface('eval', 'exists("b:acmd_auto_encode") ? b:acmd_auto_encode : g:acmd_auto_encode')
  if formencoding != localeencoding:
    filePath = filePath.decode(formencoding).encode(localeencoding)
    if autoencode == '1':
      fileName = fileName.decode(formencoding).encode(localeencoding)

  result = [fullFileName, filePath, fileName, fileSuffix]

  return result

# 获取缓存
def getCache():
  command=''
  commandPath=''
  commandCache=vimInterface('eval', 'b:commandCache')

  if commandCache:
    command = re.split(r'(?<!\\)\|', commandCache)
    for i in range(0, len(command)):
      if command[i].find('|')>-1:
        command[i] = command[i].replace( '\|', '|' )

    if command[0].find('@')==0:
      commandPath = command[0].lstrip('@')
      del command[0]

  return [commandPath, command]

# 设置缓存
def setCache(commandPath, command):
  tmpCommand = ''
  if commandPath:
    tmpCommand = '@'+commandPath

  for i in range(0, len(command)):
    tmpCommand += '|'+command[i].replace( '|', '\|' )

  vimInterface('command', 'let b:commandCache="'+tmpCommand+'"')

  return True

# 获取命令
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

  return [commandPath, commandName, command]

def runCommand():
  commandPath, commandName, command = getCommand()

  # 改变路径
  if commandPath != '':
    tempPath = os.getcwd();
    os.chdir(commandPath);

  errMsg = ''

  for i in range(0, len(command)):
    # 执行命令
    ret = subprocess.Popen(command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errMsg = ret.stderr.read()
    if errMsg != '': break

  # 返回初始目录
  if commandPath != '':
    os.chdir(tempPath)

  # 打印错误信息
  if errMsg:
    # 转义换行符、转义斜杠、转义引号
    errMsg = re.sub(r'\r(?:\n|)', r'\n', errMsg).replace('\\', '\\\\').replace('"', '\\"')
    # 打印错误命令
    vimInterface('command', 'echohl ErrorMsg | echo "'+errMsg+'" | echohl None')
  # 打印执行结果
  else:
    # 打印执行成功命令
    # print time.strftime('%H:%M:%S')+' execute'+commandName
    # 某些系统上gvim无法正确识别print指令，调过调用gvim的echo来实现打印
    vimInterface('command', 'ec "'+time.strftime('%H:%M:%S')+' execute'+commandName+'"')

# build time 10/20/2012 21:15
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1

EOF
  en
endf
" }}}

" 初始化缓冲区
fu! autocommand#initBuffer()
  if !s:py_loaded | cal autocommand#loadpy() | en
  let b:fullFileName=expand('%:p')
  let b:commandCache=''
endf

" 重置缓存
fu! autocommand#flush()
  cal autocommand#loadpy()
  cal autocommand#initBuffer()
endf

" 绑定事件
fu! autocommand#bind()
  exe 'no <silent> <buffer> '.s:callKey.' :cal autocommand#main()<CR>'
  exe 'vno <silent> <buffer> '.s:callKey.' :cal autocommand#main()<CR>'
  exe 'ino <silent> <buffer> '.s:callKey.' <C-o>:cal autocommand#main()<CR>'
endf

" 初始化配置文件
fu! autocommand#initConfig()
  " 如果文件未加载则加载
  cal autocommand#loadpy()
  let s:cwd=getcwd()
  let s:dir=input("create config ".s:cwd."(yN):")
  redraw
  if s:dir=='y'
    py createConfigFile()
    ec "success"
  el
    ec "abort"
  en
endf

" 默认命令
fu! autocommand#getCommand(fileType)
  " 获取用户自定义命令
  if exists('*Autocommand_usercmd')
    let l:ret=Autocommand_usercmd(a:fileType)
    if l:ret!="" | retu l:ret | en
  en
  if a:fileType=="haml"
    let ret="haml -nq #{$fileName}.haml #{$fileName}.html"
  elsei a:fileType=="sass"
    let ret="sass #{$fileName}.sass #{$fileName}.css"
  elsei a:fileType=="less"
    let ret="lessc #{$fileName}.less>#{$fileName}.css"
  elsei a:fileType=="coffee"
    let ret="coffee -p #{$fileName}.coffee>#{$fileName}.js"
  elsei a:fileType=="jade"
:    let ret="jade -P #{$fileName}.jade"
  else
    let ret=""
  en
  retu l:ret
endf

" 获取绑定快捷键
let s:callKey=exists('g:acmd_call_key') ? g:acmd_call_key : ''
" 配置文件类型
let s:fileTypeList=exists('g:acmd_filetype_list') ?  g:acmd_filetype_list : ['haml', 'sass', 'less', 'coffee', 'jade']
" 设置自动绑定事件
if s:callKey!=""
  exe 'au FileType '.join(s:fileTypeList, ',').' cal autocommand#bind()'
  exe 'au BufNewFile,BufRead *.'.join(s:fileTypeList, ',*.').' cal autocommand#initBuffer()'
en

" 绑定命令
com! -nargs=0 Acmd cal autocommand#main()
com! -nargs=0 AcmdInitConfig cal autocommand#initConfig()

" 设置默认自动转码
if !exists('g:acmd_auto_encode') | let g:acmd_auto_encode=1 | en

" 设置默认配置文件名
if !exists('g:acmd_config_name') | let g:acmd_config_name='_config' | en

" build time 10/20/2012 21:15
" vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
