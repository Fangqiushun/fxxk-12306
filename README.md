fxxk-12306
==============================================
一个旨在实现12306全自动抢票的持久项目会，后续不断更新

## 目录结构
    ├── fxxk_12306              -- 主要功能入口
    │   ├── __init__.py
    │   ├── left_ticket.py      -- 余票查询类
    │   ├── logger.py           -- 日志类
    │   └── login.py            -- 登录类
    ├── config.py               -- 配置
    ├── Pipfile                 -- 依赖
    ├── Pipfile.lock
    ├── README.md
    ├── run.py                  -- 启动脚本
    ├── station_name.py         -- 获取车站中英对应字典
    └── station.pk              -- 车站中英对应字典

## 安装
```bash
pip install pipenv
pipenv install
```

## 启动
```bash
# 查看帮助
python run.py --help
# 查询余票
python run.py --search_ticket <乘车日期> <出发站> <到达站>
# 登录
python run.py --login <账号> <密码>
```

## TODO
1. 自助下单
2. 多线程