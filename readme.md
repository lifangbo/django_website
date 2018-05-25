该webSite是基于Django架构设计的，用python进行开发。<br>
Django只是一个web架构，不是一个webServer，因此在典型应用时，需要前端架设webServer；<br>
在测试时，可以不依赖于webServer，可以独立于webServer而单独运行。<br>
下面简单介绍如何搭建该webSite。<br>
一、安装python<br>
	本webSite基于python2.x，首先下载python(推荐python2.7)。python在安装过程中，默认会安装pip软件。安装完毕之后，默认路径是：
	C:\Python27下面有python.exe，C:\Python27\Scripts下面有pip.exe。可以将C:\Python27；C:\Python27\Scripts添加到系统的PATH环境变量中，
	这样在终端运行时可以不带绝对路径。如果不加入到PATH变量中，需要带绝对路径。<br>
二、安装django插件。<br>
	1、打开终端(开始-->cmd.exe),输入[python -v](如果没有将python路径加入到PATH，需要执行：C:\Python27\python.exe -v, 下同)，确认python安装成功<br>
	2、[pip install django==1.10.2] ,这里指定版本1.10.2，因为服务器是基于1.10.2开发的，最好保持一致。<br>
	3、确认django安装成功，终端输入：[python]， 之后[import django], 再之后输入[django.VERSION],确认终端输出django的版本信息。<br>
三、安装git(可选)<br>
	如果你已经获取了整个webSite的源代码，可以无需安装git，不过为了获取最新版本的webSite代码，建议安装git。<br>
	1、https://git-scm.com/downloads/guis，可以下载git客户端。<br>
	2、如果本地没有仓库，需要从服务器拉取到本地，并建立仓库：[git clone https://github.com/lifangbo/django_website.git]<br>
	3、如果本地已经有仓库，更新到最新版本。[git pull]<br>
<br>
四、启动服务器。<br>
	1、进入webSite源码顶层目录(假设是：D:\source\WebServer\trunk\website)，[cd D:\source\WebServer\trunk\website]<br>
	2、终端输入[python .\manage.py runserver]，如果没有报错的话，服务器应该已经跑起来了，这时候，打开浏览器，输入地址：<br>
	http://127.0.0.1:8000/admin， 这时候应该会弹出用户登录的界面。<br>

五、调试<br>
	1、下载fiddler，方便构建POST包。方便调试。<br>
