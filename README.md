在命令行里随机读一条别人发的 status，或者自己提交一条

使用
----

读 status

	$ sread

发布一条 status

	$ swrite 我的第一条 status
	
	# 打印帮助
	$ swrite -h

安装
----

	$ git clone https://github.com/shispt/shell-read
	$ python setup.py install

安装后会有 $HOME/.shell_read.conf 配置文件

卸载
----

	$ bash uninstall.sh
