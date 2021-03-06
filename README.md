# Project Defter App 

<div align=center><img width="355" height="144" src="https://s3.bmp.ovh/imgs/2021/08/ff22d30dc2db2a7d.png" style="border-radius: 15px; box-shadow: 0px 5px 4px rgba(0, 0, 0, 0.25);"/></div>

## "Defter, easier and quicker to develop your GUI Apps using Python in the built-in browser."
### URL: https://github.com/BarryWangQwQ/Defter
### Git: https://github.com/BarryWangQwQ/Defter.git
### Authors: `BarryWang` —(Main line) , `BOOKAI` —(Branches)  

<div>
<div> </div>
<img src="https://img.shields.io/pypi/l/defter?style=for-the-badge" alt="license" />
<img src="https://img.shields.io/pypi/v/defter?color=orange&style=for-the-badge" alt="pypiversion" />
<img src="https://img.shields.io/pypi/pyversions/defter?style=for-the-badge" alt="pyversions" />
<img src="https://camo.githubusercontent.com/9e08593ef5174a8466232c462ee6f7cfb53679acf2acbadd5f7c7b0bf5eb1ee0/68747470733a2f2f696d672e736869656c64732e696f2f6c67746d2f67726164652f707974686f6e2f672f73616d75656c6877696c6c69616d732f45656c2e7376673f6c6f676f3d6c67746d267374796c653d666f722d7468652d6261646765" alt="codequal" />
</div>

## 1. Quick Start

####     Project Defter App 是一种思想，旨在开发者在开发前后端分离式应用程序时无需关注中间请求与返回方式，这一切将由 Defter Core 来接管。  
####     Defter 把前后端复杂的数据交换模式抽象为 后端 (back-end) 与 前端 (front-end) 两个模型。  
####     因此，在 Python 中编写的方法以及在前端使用 Python/JavaScript 中编写的方法均可使用简单的暴露从而实现相互调用以及数据交互，无需过多的操作与API设计。  
####     Defter 还集成了强大的前端 Web Python 编译器，对于喜爱使用 Python 的开发者，其可以采纯 Python 代码来轻松构建前后端应用。并且重要的逻辑代码还可在几乎不损失性能的情况下安全的运行在内建虚拟机 DefterVM 之上，且与 Javascript 无缝协同。

### 1.1 安装

> Python版本 `3.8+`

> 系统 `Windows` `Linux` `Mac`(实验) `以及所有基于较新标准的浏览器系统`

```sh
pip install defter # -i https://pypi.org/simple
```

### 1.2 快速体验

#### 使用cli命令创建一个示例
```sh
defter -demo here
```

#### 直接执行backend.py
```sh
python backend.py
```

### 1.3 Cli命令

###### 1.3.1 defter.exe / defter.sh / defter
### 生成示例
```sh
defter -demo [here / other path]
```

### 创建项目
```sh
defter -create [here / other path]
```

###### 1.3.2 defter-frontendc.exe / defter-frontendc.sh / defter-frontendc
### 编译前端文件
```sh
defter-frontendc [front-end python file] [src directory] # 编译.py前端文件并输出到指定资源(src)目录
```

编译后输出的文件：
- `xxx.html` App的前端入口  
  `./build` 前端编译器编译后输出的目录：
    - `xxx.js` 主要的 JavaScript API
    - `DefterVM.runtime.js` DefterVM Runtime library 运行库 (如果目录中原本存在则不会输出)  
    - `~.js` 更多 JavaScript API  

Tip: 后端 (back-end) Python文件中只需在 backend.start() 方法引入`xxx.html`参数即可指明前端 (front-end)的入口。

###### 1.3.3 defter-packager.exe / defter-packager.sh / defter-packager
### 打包项目

#### cd 到指定项目位置
```sh
cd [defter project path] # 确保该项目下存在后端python文件，同时也存在伴随的资源(src)目录。
```

#### 执行打包
```sh
defter-packager [back-end python file] [src directory] # (两参数均为cd后的相对路径) 可选参数: -F 打包成一个可执行文件(有Console) -Fw 打包成一个可执行文件(无Console) -i 添加您喜欢的ico图标
```

###### 1.3.4 defter-accelerator.exe / defter-accelerator.sh / defter-accelerator

### 数据交换加速器 (Only 64bit)

```sh
defter-accelerator [True / False] # 开启可大幅提升对象数据的序列化和反序列化性能，适用于大数据量高并发的App类型，但必须是64位的环境才被允许开启。
```

## 2. 项目结构

`backend.py` App后端服务的主要入口(可自定义命名)：

- `用于编写后端服务程序和App启动配置`

`./src` App资源文件的集合目录(可自定义命名)：

### (默认) 纯Python实现(即前后端均使用Python语言开发，仅使用API方式与外部语言与支持的框架)将至少包含：
- `xxx.html` 通过 defter-frontendc 编译出的App的前端设计入口  
- `defter.js` defter 前端 (front-end) 内部方法与变量的传递核心  
  `./build` 前端编译器编译后输出的目录：
    - `xxx.js` 通过 defter-frontendc 编译出的主要 JS api
    - `DefterVM.runtime.js` DefterVM (Defter Virtual Machine) 虚拟机运行库
- `favicon.ico` 您喜爱的App图标


### (可选) 半Python实现(即后端使用Python语言开发，前端完全使用Javascript等其他语言和框架开发)将至少包含：
- `xxx.html` App的前端入口 (需引用 defter.js )
- `defter.js` defter 前端 (front-end) 内部方法与变量的传递核心
- `favicon.ico` 您喜爱的App图标

> 注意：使用(可选)方法的代码将不会在 DefterVM (Defter Virtual Machine) 虚拟机中运行。

## 3. 发布版本

| 模块 | 版本 | 发布时间 |
| --- | --- | --- |
| `defter` | `2.0 Beta3` | `2021/9/1` |
| `defter` | `2.0 Beta2` | `2021/8/31` |
| `defter` | `2.0 Beta` | `2021/8/27` |
| `defter` | `1.0 Beta2` | `2021/8/12` |
| `defter` | `1.0 Beta` | `2021/7/22` |

### 当前版本  

> `defter-frontendc` 前端 (front-end) 编译器在64位环境下的编译速度和准确性得到优化。

> `defter-frontendc` 前端 (front-end) 编译器的输出目录结构稍作微调，使其变得更加清晰明了。

> `defter-accelerator` 数据交换加速器的加速逻辑得到优化。

####修复问题:

> `2021/8/31 2.0 Beta2 issues` 数据交换加速器被多次缓存的BUG。

> `2021/8/27 2.0 Beta issues` 包无法被完全卸载。

> `2021/8/27 2.0 Beta issues` 前端 (front-end) 编译器发生异常引发的一些故障。(defter-frontendc)

> `2021/7/22 1.0 Beta issues` 在Mac操作系统下可能无法正常使用defter-cli来创建新的项目。  

> `2021/8/12 1.0 Beta2 issues` 解决了高并发异步方法引起的严重性阻塞问题。  

####新增特性:   
> 1 `前后两端` 数据交换加速器 (仅限64位环境开启）使用 Rust lang 重构的json序列化和反序列化工具，开启后可拥有强劲的大数据对象交换速度和传输性能。  
>> 2 `后端 (back-end)` 引入基于线程的协程并发，绕过CPython GIL全局解释器锁，大幅提升App性能，解决了高并发异步方法引起的严重性阻塞问题。  
>>> 3 `前端 (front-end)` 的模拟Python实现由原先的纯解释器解释模式转变为编译解释混合执行模式，并可与Google Chromium V8 JIT即时编译技术相互工作，大幅提升加载速度以及性能。  
4 `前端 (front-end)` 让重要逻辑运行在 DefterVM (Defter Virtual Machine) 虚拟机上，在尽可能不损失性能的情况下，使得Javascript解释器无权干涉内建虚拟机从而保证执行的安全，大幅降低了前端 (front-end) 被恶意调试代码的可能。  

####已知问题:   
> 由于基于线程的协程引入，暂不支持中央处理器单元的多核心负载分配。

### 历史  

>`2021/7/22` 发布的第一个版本  
已知问题: 在Mac操作系统下可能无法正常使用defter cli来创建新的项目。

>`2021/8/12` 执行重构  
部分代码用C lang重构, 方法映射和传递的速度提升4倍。  
已知问题:  
1 在Mac操作系统下仍然可能无法正常使用defter cli来创建新的项目。  
2 分布请求时，异步高并发导致线程阻塞。

>`2021/8/20` Defter 2.0 beta 计划启动。

>`2021/8/27` Defter 2.0 beta 发布。

## 4. 了解更多

<img src = 'https://s3.bmp.ovh/imgs/2021/09/ebfe7acb5844ec0c.png' style="border-radius: 15px; box-shadow: 0px 5px 4px rgba(0, 0, 0, 0.25);"/>

## 5. References & Thanks

| Projects | URLs |
| --- | --- |
| Eel | https://github.com/ChrisKnott/Eel |
| Transcrypt | https://github.com/QQuick/Transcrypt |
