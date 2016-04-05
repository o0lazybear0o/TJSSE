
##配置开发环境

###1. Python 3.4.2

mac : 

mac 中自带python2，使用python3需要安装

`brew install python3` -- 如果有homebrew

在terminal中输入`python3 --version`或者直接输入`python3`验证安装完成

others && Details：

[廖雪峰Python3教程 -- 安装Python](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316090478912dab2a3a9e8f4ed49d28854b292f85bb000)

###2. Django 1.9.4 

1. 安装pip [pip doc](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)  注意如果是mac，在每个使用 `python` 的地方用`python3`
2. 安装Django `sudo pip install Django`
3. 验证安装，在terminal输入`python3`进入python terminal
	````
	>>> import django
	
	>>> print(django.get_version()
	````
	 
Details: [Django 安装 - 请选择安装官方正式发布的版本](http://python.usyiyi.cn/django/intro/install.html)

###3. 使用MySQL5.6.21

1. 安装MySQL
	
	`brew install mysql`
	
2. (Optional) 喜欢图形化的可以使用MySqlWorkbench
3. 安装pymysql， python3不支持mysqldb(mysql-python)
	
	`pip install PyMySQL`
	
	[安装及使用Details](https://www.robberphex.com/2013/12/254)

##数据库建立连接.
1. git clone 代码
2. 创建如下数据库

    'NAME': 'TJSSE' -- 数据库名称

    'USER': 'root',

    'PASSWORD': 'o0lazybear0o',

    'HOST': '127.0.0.1',

    'PORT': '3306'
    
3. 在项目目录执行`python3 manage.py makemigration accounts`

    `python3 manage.py migrate`
