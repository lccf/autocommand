" --------------------------------------------------
" [autocommand相关配置] {{{
" --------------------------------------------------
" 开启调试模式
"let g:acmd_debug=1
" 调用快捷键
let g:acmd_call_key='<c-s>'
" 针对文件类型
let g:acmd_filetype_list=['haml', 'sass', 'less', 'coffee', 'jade']
" 下线划打头的文件不执行命令
fu! Autocommand_before(fullFileName)
	let shortFileName=expand('%:t')
	let isUnderline=match(shortFileName,'_')
	if isUnderline==0
		sil up
		retu 0
	el
		retu 1
	en
endf
" 自定义命令
fu! Autocommand_usercmd(fileType)
	if a:fileType=="jade"
		let ret="jade #{$fileName}.jade -PO ./"
	el
		let ret=""
	en
	retu l:ret
endf
" 修正win平台ruby1.9x下自动编码出错
"au FileType haml,sass let w:acmd_auto_encode=0

" vim:sw=4:ts=4:sts=4:noet:fdm=marker:fdc=1
