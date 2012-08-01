" --------------------------------------------------
"   FileName: autocommand.vim
"       Desc: 插件主文件
"     Author: lcc
"      Email: leftcold@gmail.com
"    Version: 0.3(beta)
" LastChange: 07/21/2012 13:59
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
  " 执行命令
  py runCommand()
endf

" 加载autoCommand.py
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
# LastChange: 07/21/2012 13:59
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
  autoencode = vim.eval( 'exists("w:acmd_auto_encode") ? w:acmd_auto_encode : g:acmd_auto_encode' )
  if formencoding != localeencoding:
    filePath = filePath.decode(formencoding).encode(localeencoding)
    if autoencode == '1':
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
# build time 07/21/2012 15:38
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1

EOF
  en
endf

" 初始化窗口
fu! autocommand#initWindow()
  if !s:py_loaded | cal autocommand#loadpy() | en
  let w:fullFileName=expand('%:p')
  let w:commandCache=''
endf

" 重置缓存
fu! autocommand#flush()
  cal autocommand#loadpy()
  cal autocommand#initWindow()
endf

" 绑定事件
fu! autocommand#bind()
  exe 'no <silent> <buffer> '.s:callKey.' :cal autocommand#main()<CR>'
  exe 'vno <silent> <buffer> '.s:callKey.' :cal autocommand#main()<CR>'
  exe 'ino <silent> <buffer> '.s:callKey.' <C-o>:cal autocommand#main()<CR>'
endf

" 初始化配置文件
fu! autocommand#init()
  " 如果文件未加载则加载
  cal autocommand#initWindow()
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
let s:fileTypeList=exists('g:acmd_filetype_list') ?  g:acmd_filetype_list : ['haml', 'sass', 'less', 'coffee']
" 设置自动绑定事件
if s:callKey!=""
  exe 'au FileType '.join(s:fileTypeList, ',').' cal autocommand#bind()'
  exe 'au BufNewFile,BufRead *.'.join(s:fileTypeList, ',*.').' cal autocommand#initWindow()'
en

" 绑定命令
com! -nargs=0 Acmd cal autocommand#main()
com! -nargs=0 AcmdInitConfig cal autocommand#init()

" 设置默认自动转码
if !exists('g:acmd_auto_encode') | let g:acmd_auto_encode=1 | en

" build time 07/21/2012 15:38
" vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
