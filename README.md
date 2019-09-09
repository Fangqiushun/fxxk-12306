fxxk-12306
==============================================
一个旨在实现12306全自动抢票的持久项目会，后续不断更新

## 目录结构
    ├── fxxk_12306              -- 主要功能入口
    │   ├── __init__.py
    |   ├── common.py           -- 通用方法
    │   ├── left_ticket.py      -- 余票查询类
    │   ├── logger.py           -- 日志类
    │   ├── login.py            -- 登录类
    |   └── order.py            -- 下单类
    ├── chromedriver            -- 谷歌浏览器驱动(linux, window要下载chromedriver.exe)
    ├── config.py               -- 配置
    ├── Pipfile                 -- 依赖
    ├── Pipfile.lock
    ├── README.md               -- 说明文档
    ├── run.py                  -- 启动脚本
    ├── station_name.py         -- 获取车站中英对应字典
    └── station.pk              -- 车站中英对应字典
    

## 安装
```bash
# 安装依赖
pip install pipenv
pipenv install
# 安装模拟浏览器驱动
wget http://npm.taobao.org/mirrors/chromedriver/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```


## 启动
```bash
# 设置环境变量(需要先启用邮箱的SMTP服务,设置客户端授权码)
export MAIL_RECEIVERS=<接收邮箱>
export MAIL_USERNAME=<发送邮箱>             # hardcode只能使用126邮箱
export MAIL_PASSWORD=<发送邮箱密码>
# 查看帮助
python run.py --help
# 查询余票
python run.py --search_ticket
# 登录
python run.py --login
# 下单
python run.py --order
```

## TODO
1. 使用ip池定时切换ip,减少被封的机率
2. 多线程,提高抢票速度