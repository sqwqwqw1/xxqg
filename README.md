# 查询学习强国题库

查询学习强国答案的小程序，实际上不值一提，但是却是我第一次写出来的小玩意。

其实是偷的别人服务器的内容（http://www.syiban.com）。

核心程序是server里的query.py，实际上，只需要run_query(关键词)就可以得到答案了。学了两天fastapi，感觉好像可以写成个接口试试，就写了。

运行sever里的api.py，就可以调用http://127.0.0.1:8000/xxqg?key=keyword（本机或者服务器ip），返回结果，GET或POST请求均可。

使用了jwt验证，只有一个用户，用户名user01，密码password。

也可以不自己写代码调用接口，直接运行client里面的xxqg.py。
