# Project Defter App 

<div align=center><img width="355" height="144" src="https://s3.bmp.ovh/imgs/2021/08/ff22d30dc2db2a7d.png"/></div>

## "Defter, easier and quicker to develop your GUI Apps using Python in the built-in browser."
### URL: https://github.com/BarryWangQwQ/Defter
### Git: https://github.com/BarryWangQwQ/Defter.git
### Author: `BarryWang` `BOOKAI`


## 1. Quick Start

### 1.1 安装

> Python版本 `3.0+`

> 支持的系统 `Windows` `Linux` `Mac`(试验)

```sh
pip install defter
```

### 1.2 使用cli命令

#### 创建项目
```sh
defter-cli -create [here / your path]
```

#### 升级Defter Core及相关组件
```sh
defter-cli -update [here / your path]
```

#### 把javascript函数映射到python中(试验)
```sh
defter-cli -js2py [here / your path]
```

#### 打包项目(试验)
```sh
defter-cli -package [here / your 'main.py' path]
```

### 1.3 快速体验

#### 直接执行创建出的main.py模板
```sh
python main.py
```

## 2. 目录结构说明

`main.py` App的后端服务主要入口：

- `用于编写后端服务程序和App启动配置`

`./AppResources` App的资源文件集合目录：

至少包含：
- `app.html` App的前端设计页面
- `core.js` Defter Core
- `eel.js` Eel 依赖

可选：
- `icon.ico` App的图标
- `brython.js` Brython 依赖 (用于支持Web Python编程)
- `brython_stdlib.js` Brython 标准库
- `unicode.txt` Brython unicode字符集
- `main.js` Electron 启动主函数入口文件
- `package.json` Electron 配置文件

## 3. 发布版本

| 模块 | 版本 | 发布时间 |
| --- | --- | --- |
| `defter` | `1.0 Beta` | `2021/8/12` |

> 发布的第一个版本  
已知错误: 在Mac操作系统下可能无法正常使用defter-cli来创建新的项目

## 4. Reference & Thanks

| Project | URL |
| --- | --- |
| Eel | https://github.com/ChrisKnott/Eel |
| Brython | https://github.com/brython-dev/brython |
