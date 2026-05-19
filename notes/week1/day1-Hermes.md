#### 目录

[前言](#前言)

[部署爱马仕(Hermes)](#部署爱马仕(Hermes))

​	[首先服务器推荐选择：](#首先服务器推荐选择：)

​	[安装docker](#安装docker)

​	[配置镜像源](#配置镜像源)

​	[安装爱马仕(Hermes)](#安装爱马仕(Hermes))

[出现的问题](#出现的问题)

​	[无法连接tg](#无法连接tg)

​	[模型的配置](#模型的配置)

[结语](#结语)





#### 前言

我是20年考入大学的，虽说是本科，我也在26年，也就是今年才毕业，具体原因是由于在校期间学习态度过于恶劣，导致挂了许多学分（超恐怖的数量），于是花了两年左右压缩着自己赶完课业，，目前在家躺平中。

在此之前，我已经几个月没有深度的使用AI了，它的发展太快了，快到我几乎绝望；我是一个比较懒散、拖延的人，我在博客的必须技能html、css、js上迂回了好几次，本来想着再次深入学习js，顺便把ts、vue学一学。

上周碰巧在X上看到了大神 [DIYGOD](https://x.com/DIYgod) 的分享的推文，也就是本次学习课程，我选择了报名，因为AI再恐怖，我也必须拥抱它。

昨天的开营仪式很精彩，在大学时我也参加过字节跳动举办的类似夏令营/冬令营活动，但毕竟我不是专业出身，又较为懒散，也无成就可言，本来想发言，可是奈何过于羞愧，便撰写自我介绍发在了tg群组里。

今天主要部署了hermes，并打通了与tg的连接（毕竟我的服务器在大陆），就是有一点，模型的配置让我苦恼了几个小时，不过也都解决了（毕竟是免费的模型），下面记录一下我使用 <ins>docker部署learning agent</ins>> 的过程与问题：

> 注意：除了服务器，咱对于模型主打的就是一个字：白嫖！！！

## 部署爱马仕(Hermes)

> 对于learning agent来说，无论是Hermes还是openclaw亦或者是课程中提到的其他，自行选择即可。

#### 首先服务器推荐选择：

> 这是官方文档中给出的规格 详见 [Hermes](https://hermes-agent.nousresearch.com/docs/) 

| 资源           | 最低限度 | 受到推崇的                       |
| -------------- | -------- | -------------------------------- |
| 记忆           | 1 GB     | 2–4 GB                           |
| 中央处理器     | 1 个核心 | 2个核心                          |
| 磁盘（数据卷） | 500 MB   | 2GB以上（随会话/技能提升而增长） |

我的阿里云服务器规格是：

```markdown
CPU&内存:2H2G
带宽:3M
系统：Alibaba Cloud Linux 3.2104 LTS 64位
```

部署过程流畅，在tg上对话速度稍慢

#### 安装docker

> 我是在购买服务器时便选择docker了
>
> 问题：由于缺少相关知识，对于docker的安装我有疑问，但能解决。后面会重新整理关于docker的知识！

不过我找了一个一键脚本安装：

```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

#### 配置镜像源

> 由于我的服务器在大陆所以部署Hermes时会超时，找个合适的镜像源比较好

终端切换目录找到`daemon.json`文件并打开编辑

```bash
cd /etc/docker # 一般安装后都在这里
ls # 会输出daemon.json
vim daemon.json # 可以使用你喜欢的编辑方式，vim操作不多赘述，浏览器自行搜索

# 将其中内容改成下列

{
  "registry-mirrors": [
  											"https://mirror.ccs.tencentyun.com",
                        "https://docker.1ms.run",
                        "https://hub.rat.dev",
                        "https://dockerpull.org"
  ]
}

# 记得重启生效
sudo systemctl reload docker
sudo systemctl restart docker
```



查看已经配置的镜像源：

```bash
docker info | grep -A 5 "Registry Mirrors"
```



#### 安装爱马仕(Hermes)

> 详细依旧在 [Hermes](https://hermes-agent.nousresearch.com/docs/) 

我们的项目树如下：

```markdown
hermes/
├── data/
│   ├── config.yaml
│   ├── skills/
│   └── ...
├── docker-compose.yml
└── .env(省略)
```

提前创建目录以保持整洁

```bash
mkdir -p hermes/data
mkdir docker-compose.yml
```

 使用vim编辑docker-compose.yml，保存退出即可

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"   # gateway API
      - "9119:9119"   # dashboard (only reached when HERMES_DASHBOARD=1)
    volumes:
      - ./data:/opt/data  # 如果你设置的不一样，这里也要改
    environment:
      - TZ=Asia/Shanghai  # 时区，加不加都可以，自己时区网上搜索

      - HERMES_DASHBOARD=1 # 面板建议开启

      - GATEWAY_ALLOW_ALL_USERS=true # 谁能访问面板0.0
      
      #你的tg_id
      - TELEGRAM_ALLOWED_USERS=${TELEGRAM_ALLOWED_USERS}
      
			# 下面两个无所谓，后面直接更改data/config.yaml文件设置模型
      - OPENAI_BASE_URL=${OPENAI_BASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      
      # 根据官方文档获取输入tg_bot token将下面内容直接替换即可
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# 下面五行代码后续问题中会提到，先别使用
     # - HTTP_PROXY=http://host.docker.internal:7890
     # - HTTPS_PROXY=http://host.docker.internal:7890
     # - ALL_PROXY=socks5://host.docker.internal:7890

    #extra_hosts:
     # - "host.docker.internal:host-gateway"

networks:
  default:
    driver: bridge
```



执行 `docker compose up -d ` 启动

访问 `http://IP:9119` 便可看到面板了，那么恭喜你，成功部署Hermes，这位还可以的learning agent



模型配置这里就不多赘述！请看下面 ↓ 



## 出现的问题

在部署过程中出现了各种各样的问题，毕竟我是零基础，且环境不一样啊，只能遇到问题解决问题，这里总结一下比较困难的问题。

> 自建节点可以看一下我之前的博客 [ahyun的爱孤岛](https://ahyun.org.cn/projects/self-built-node-record/)  

#### 无法连接tg

由于服务器在大陆所以爱马仕即便部署成功，也很难访问到tg

不信你可以执行一下下面的命令：

```bash
curl https://api.telegram.org
```

你看看有没有反应0.0(～￣▽￣)～



接下来就是给服务器走一个代理（切莫自建节点违规使用，本文档只做学习记录）

我选择的是docker部署一个singbox来让Hermes独享我自建的节点

同样：

```bash
# 创建目录
mkdir -p ~/proxy-singbox
cd ~/proxy-singbox
# 配置，这部分不多赘述（你会自建节点就会这部分），可以自行ai学习
vim config.json
# 配置镜像 将下面复制进去
vim docker-compose.yml

services:
  sing-box:
    image: ghcr.io/sagernet/sing-box:latest
    container_name: sing-box
    restart: unless-stopped

    volumes:
      - ./config.json:/etc/sing-box/config.json

    command: run -c /etc/sing-box/config.json

    ports:
      - "7890:7890"
      
      
# 最后点火启动
docker compose up -d
```

再把上面注释掉的部分启用配合使用

不用测试，去面板刷新就能看到tg连接成功了。



#### 模型的配置

这部分我是使用阿里百炼提供的几十个模型（每个都有100万token），配置了一下午，最后也搞定了，也很方便切换。对于这方面我很是疑惑，无论是之前的龙虾，还是其他的工具，对于模型的调用究竟是如何运作的，我想这一点明白后，大概率没有这个问题了。



先说我的方案：

阿里百炼获取key → vim编辑data/config.yaml文件 → 

更改其部分内容：(注释很多，在其中找对应输入即可)

```yaml
model:
  default: qwen3.5-flash # 你想先使用的模型 比如 qwen3.5-flash
  provider: custom
  api_key: your-key
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
```

在tg中如果遇到模型token使用完，可以输入 `/model 模型` 来直接更改（就能继续白嫖了0.0），再输入对话即可！



其中在课程网站 → 个人资料页 最下方的key，到现在我不知道这个是干啥用的0.0超疑惑！！！



## 结语

今天学习任务其实很少，因为我没有仔细的去阅读学习页面，不过嘛，些许知识的翻涌罢了，大家肯定能跟我一样速度灌输近脑海的。



对了，记得给你的 learning agent 加上课程专属 skill (在对话框直接输入)

```markdown
请作为我的 AI × Web3 School Learning Agent，先阅读启动 Prompt：https://aiweb3.school/learning-agent.zh.txt，并结合 Handbook：https://aiweb3.school/zh/handbook/，帮我初始化个人学习计划、GitHub 学习仓库、每日打卡草稿和 Handbook feedback 流程。
```

