" --------------------------------------------------
"   FileName: autocommand.vim
"       Desc: 插件主文件
"     Author: lcc
"      Email: leftcold@gmail.com
"    Version: $version$
"  buildTime: $buildTime$
" LastChange: $lastChange$
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
#$file:autocommand.py$
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
" vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
