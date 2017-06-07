##   clickLikeInQzone
对于空间里朋友们的动态，我们有时候觉得点赞不够及时或者会漏赞，基于这种需求，便有了这个脚本。<br>
脚本依托于 [selenium](https://github.com/SeleniumHQ/selenium)模块，调用[phantomjs](https://github.com/ariya/phantomjs)实现功能。python2和3均可运行。<br>
你需要手动改写脚本中ACCOUNT，PASSWORD，myAccount，myNickName等变量。

在运行时打印的日志中，

```markdown
Just clicked the-> URL <-

```

中间的url是刚刚所点的说说地址，如果你在浏览器中已登录，则粘贴该url可以直接访问该说说。<br>
因为js的特性，一个说说有时可能需要经过多次才能点上赞（只点了一次），但是日志会打印多次，无妨。

#### **更新日志：**

```markdown
Version 1.2.1 修复了部分bug（程序跑飞，phantomjs会占用服务器过多资源等），在我目前所有的测试中都是通过的，较稳定。

Version 1.1 新加了对于在评论里@本人的说说进行自动回复的功能。

Version 1.0 测试版，实现点赞功能。
``` 
**注：**
*该脚本运行在linux上时必须打印代码中的 js console日志，否则点赞无效（在我所有的测试中均如此）；windows上运行时则无所谓打印与否。*
