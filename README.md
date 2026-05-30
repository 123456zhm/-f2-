# F2 Crawler

F2 是一个基于 Python 的多平台爬虫项目，支持小红书、抖音和微博平台的数据爬取。

## 功能特性

- **小红书爬虫** - 支持用户主页、笔记详情、搜索等功能
- **抖音爬虫** - 支持视频、用户主页、直播等数据爬取
- **微博爬虫** - 支持微博内容、用户信息等数据获取
- **小程序支持** - 配套微信小程序前端

## 项目结构

```
f2/
├── f2/                    # 主应用目录
│   ├── apps/              # 各平台爬虫实现
│   │   ├── xiaohongshu/   # 小红书爬虫
│   │   ├── douyin/        # 抖音爬虫
│   │   └── weibo/         # 微博爬虫
│   ├── crawlers/          # 爬虫基类
│   ├── dl/                # 下载器模块
│   ├── cli/               # 命令行接口
│   ├── log/               # 日志模块
│   ├── utils/             # 工具函数
│   └── i18n/              # 国际化支持
├── miniprogram/           # 微信小程序
└── tests/                 # 测试文件
```

## 环境要求

- Python >= 3.10
- 依赖包见 requirements.txt

## 安装与使用

```bash
# 安装依赖
cd f2
pip install -r requirements.txt

# 运行爬虫
python main.py --help
```

## 许可证

MIT License