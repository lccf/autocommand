" --------------------------------------------------
"   FileName: autocommand.vim
"       Desc: 插件主文件
"     Author: lcc
"      Email: leftcold@gmail.com
"    Version: 0.1
" LastChange: 06/16/2012 20:39
"    History: 
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
let s:isDebug=exists('g:acmd_debug') ? g:acmd_debug : 1
" 主函数
fu! autocommand#main()
  " 保存文件
  if exists('*Autocommand_before')
    cal Autocommand_before(expand('%:p'))
  el
    sil up
  en
  " 如果文件未加载则加载
  if s:isDebug == 1
    cal autocommand#load()
    let w:fullFileName = expand('%:p')
    let w:commandCache = ''
  el
    if !g:autoCommandIsLoad | cal autocommand#load() | en
    " 保存缓冲区文件名
    if !exists('w:fullFileName') | let w:fullFileName = expand('%:p') | en
    " 保存命令
    if !exists('w:commandCache') | let w:commandCache = '' | en
  en
  " 执行命令
  py runCommand()
endf

" 加载autoCommand.py
fu! autocommand#load()
  "echo "pyfile ".s:scriptDir."/autocommand/autocommand.py"
  exe "pyfile ".s:scriptDir."/autocommand/autocommand.py"
  let g:autoCommandIsLoad=1
endf

" 重置缓存
fu! autocommand#flush()
  call autocommand#load()
  if exists('w:fullFileName') | unlet w:fullFileName | en
  if exists('w:commandCache') | unlet w:commandCache | en
endf

" 绑定事件
fu! autocommand#bind()
  exe 'no <silent> <buffer> '.s:callKey.' :call autocommand#main()<CR>'
  exe 'vno <silent> <buffer> '.s:callKey.' :call autocommand#main()<CR>'
  exe 'ino <silent> <buffer> '.s:callKey.' <C-o>:call autocommand#main()<CR>'
endf

" 初始化配置文件
fu! autocommand#init()
  " 如果文件未加载则加载
  if !g:autoCommandIsLoad | call autocommand#load() | en
  let s:cwd = getcwd()
  let s:dir=input("create config ".s:cwd."(yN):")
  if s:dir == 'y'
    py createConfigFile()
    echo "success"
  else
    echo "abort"
  en
endf

" 默认命令
fu! autocommand#getCommand(type)
  if a:type==".haml"
    let ret="haml -nq #{$fileName}.haml #{$fileName}.html"
  elsei a:type==".sass"
    let ret="sass #{$fileName}.sass #{$fileName}.css"
  elsei a:type==".less"
    let ret="lessc #{$fileName}.less>#{$fileName}.css"
  elsei a:type==".coffee"
    let ret="coffee -p #{$fileName}.coffee>#{$fileName}.js"
  en
  retu l:ret
endf

" 获取绑定快捷键
let s:callKey=exists('g:acmd_call_key') ? g:acmd_call_key : ''
" 配置文件类型
let s:fileTypeList=exists('g:acmd_filetype_list') ?  g:acmd_filetype_list : ['haml', 'sass', 'less', 'coffee']
" 设置自动绑定事件
if s:callKey!=''
  for s:item in s:fileTypeList
    exe 'au FileType '.s:item.' call autocommand#bind()'
  endfo
en
" 绑定命令
let s:cmdName=exists('g:acmd_cmd') ? g:acmd_cmd : 'Acmd'
if s:cmdName!=''
  exe 'com! -nargs=0 '.s:cmdName.' call autocommand#main()'
en
" 设置默认自动转码
if !exists( 'g:acmd_auto_encode' )
  let g:acmd_auto_encode=1
en
" vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
