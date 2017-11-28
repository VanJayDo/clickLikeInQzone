##   clickLikeInQzone
脚本依托于 [selenium](https://github.com/SeleniumHQ/selenium)模块，调用[phantomjs](https://github.com/ariya/phantomjs)实现功能。兼容python2和3。<br>
请根据自己的情况修改map VALS中的各个变量。

在运行时打印的日志中，

```markdown
Just clicked the-> URL <-

```

中间的url是刚刚所点的说说地址，如果你在浏览器中已登录空间，则粘贴该url可以直接访问该说说。<br>
因为js的异步特性，一个说说有时可能需要经过多次才能点上赞（只点了一次），但是日志会打印多次，无妨。

#### **更新日志：**

```markdown
Version 1.3 使用字符串模板对变量统一设置。

Version 1.2 修复了部分bug（程序跑飞，phantomjs会占用服务器过多资源等），通过目前所有的测试，较稳定。

Version 1.1 新增对于在评论里@本人的说说进行自动回复的功能。

Version 1.0 测试版，实现点赞功能。
``` 
**注：**
*该脚本运行在linux上时必须打印代码中的 js console日志，否则点赞无效（在我所有的测试中均如此，原因未知，觉得很玄学/斜眼笑）；windows上运行时则无所谓打印与否。*
