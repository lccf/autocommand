#autocommand

autocommand 是一款vim插件（依赖python），用来自动执行命令行操作。它最初被设计的应用场景是当保存 haml、sass、coffee 等类型文件时，生成对应的 html、css、javascript 文件，当然它的作用远不止这些，你可以用它来行任意需要自动执行的命令，例如调用 sed 去处理文件缩进、调用编译器去编译你当前编辑的程序代码等。它还支持通过配置文件来对不同的项目定制不同的命令。

##安装

需求

- python 2.x 支持
- vim 7.3x

将 plugin 目录拷贝至对应的 vim 默认目录即可。

##使用说明

###1.设置调用快捷键

在vim配置文件中增加如下配置项：

	let g:acmd_call_key='<c-s>'

定义一个全局变量 acmd_call_key 该变量的值会被映射为快捷键。上例中映射 Ctrl+s 作为调用快捷键，即常用的保存快捷键。当按下 Ctrl+s 快捷键时 autocommand 会自动尝试保存该文件，然后执行对应的命令。

###2.前置函数

在vim配置文件中增加如下代码：

	fu! autocommand_before(fullFileName)
		"echo a:fullFileName
		sil up
	endf

autocommand 允许在执行前调用一个用户自定义的函数对当前文件进行预处理，该函数名称约定为 autocommand_before 。 接受一个名为 fullFileName 的参数是当前正在编辑文件的全路径名称。 autocommand 会自动保存当前文件默认情况下你并不需要使用前置函数。

###3.针对文件类型

在vim配置文件中增加如下配置项：

	let g:acmd_filetype_list=['haml', 'sass', 'less', 'coffee']

上面的配置表示针对 haml sass less coffee 等类型文件执行命令，autocommand 默认针对 haml sass less coffee 等类型的文件调用命令。默认执行命令如下：

	#haml
	haml -nq #{$fileName}.haml #{$fileName}.html
	
	sass
	sass #{$fileName}.sass #{$fileName}.css
	
	less
	lessc #{$fileName}.less>#{$fileName}.css
	
	coffee
	coffee -p #{$fileName}.coffee>#{$fileName}.js

*#{$fileName}表示当前文件名

###4.创建自定义配置文件

打开vim执行如下命令：

	:call autocommand#init()

会自动在当前vim当前目录下创建 _config 的配置文件，配置文件使用json描述，默认文件内容如下：

	{
	  ".haml": {
	    "command": "haml -nq #{$fileName}.haml #{$fileName}.html"
	    /* 执行命令 */
	  },
	  ".sass": {
	    "command": "sass #{$fileName}.sass #{$fileName}.css"
	    /* 执行命令 */
	  },
	  ".less": {
	    "command": "lessc #{$fileName}.less>#{$fileName}.css"
	    /* 执行命令 */
	  },
	  ".coffee": {
	    "command": "coffee -bp #{$fileName}.coffee>#{$fileName}.js"
	    /* 执行命令 */
	  }
	}

修改以上的配置文件添加自己需要的选项或文件类型即可。command 可以声明为一个 json 数组，autocommand 会依次执行数组中的每条命令例如：

	".sass": {
	  "command": [
	    "sass --style compact #{$fileName}.sass ../css/#{$fileName}.css",
	    "replaceIndent ../css/#{$fileName}.css",
	    "cp ../css/#{$fileName}.css ../../../public/css/"
	  ]
	  /* 执行命令 */
	},

以上示例摘自本人开发的项目配置。首先调用 sass 将 .sass 类型的文件转换为 css，再利用 replaceIndent 脚本将文件中的2个空格替换为4个空格（项目需要），再调用 cp 命令将文件拷贝一份至项目根录目的 public/css 目录下。

###5.高级用法

待添加
