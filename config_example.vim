" --------------------------------------------------
" [autocommand相关配置] {{{
" --------------------------------------------------
" 调用快捷键
let g:acmd_call_key='<c-s>'
" 针对文件类型
"let g:acmd_filetype_list=['haml', 'sass', 'less', 'coffee']
" 命令名称
"let g:acmd_cmd='Acmd'
" 执行前置函数默认为保存
"fu! autocommand_before(fullFileName)
	"echo a:fullFileName
	"echo 'before function'
	"sil up
"endf
" }}}

" vim:sw=4:ts=4:sts=4:noet:fdm=marker:fdc=1
