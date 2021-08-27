# Project Defter App 

<div align=center><img width="355" height="144" src="https://s3.bmp.ovh/imgs/2021/08/ff22d30dc2db2a7d.png"/></div>

## "Defter, easier and quicker to develop your GUI Apps using Python in the built-in browser."
### URL: https://github.com/BarryWangQwQ/Defter
### Git: https://github.com/BarryWangQwQ/Defter.git
### Authors: `BarryWang` —(main line) , `BOOKAI` —(branches)


## 1. Quick Start

### 1.1 安装

> Python版本 `3.6+`

> 支持的系统 `Windows` `Linux` `Mac`(实验) `支持所有基于较新标准的浏览器系统`

```sh
pip install defter # -i https://pypi.org/simple
```

### 1.2 快速体验

#### 使用cli命令创建出一个示例
```sh
defter -demo here
```

#### 直接执行backend.py
```sh
python backend.py
```

### 1.3 Cli命令

###### 1.3.1 defter.exe / defter.sh / defter
#### 生成示例
```sh
defter -demo [here / other path]
```

#### 创建项目
```sh
defter -create [here / other path]
```

###### 1.3.2 defter-frontendc.exe / defter-frontendc.sh / defter-frontendc
#### 编译前端文件
```sh
defter-frontendc [front-end python file] [src directory] # 编译.py前端文件并输出到指定资源目录
```

编译后输出的文件：
- `xxx.frontend` App的前端设计入口
- `xxx.js` JavaScript API
- `DefterVM.runtime.js` DefterVM Runtime library 运行库 (如果目录中原本存在则不会输出)  

Tip: 在后端 (back-end) Python文件中只需在 Backend.Start() 中引入`xxx.frontend`即可指明前端 (front-end)的入口。

###### 1.3.3 defter-packager.exe / defter-packager.sh / defter-packager
#### 打包项目

#### cd 到指定项目位置
```sh
cd [defter project path] # 确保该项目下存在后端python文件，同时也存在伴随的资源目录。
```

#### 执行打包
```sh
defter-packager [back-end python file] [src directory] # 可选参数: -F 打包成一个可执行文件(有Console) -Fw 打包成一个可执行文件(无Console)
```

## 2. 项目结构

`backend.py` App的后端服务主要入口(可自定义命名)：

- `用于编写后端服务程序和App启动配置`

`./res` App的资源文件集合目录(可自定义命名)：

(默认) 纯Python实现(即前后端均使用Python语言开发)将至少包含：
- `xxx.frontend` 通过 defter-frontendc 编译出的App的前端设计入口
- `xxx.js` 通过 defter-frontendc 编译出的 JS api
- `defter.js` defter 前端 (front-end) 方法与变量的传递核心
- `DefterVM.runtime.js` DefterVM (Defter Virtual Machine) 虚拟机运行库
- `favicon.ico` 您喜爱的App的图标


(可选) 半Python实现(即后端使用Python语言开发，前端使用HTML、Javascript等语言开发)将至少包含：
- `xxx.html` App的前端设计入口 (需引用 defter.js )
- `defter.js` defter 前端 (front-end) 方法与变量的传递核心
- `favicon.ico` 您喜爱的App的图标

注意：使用(可选)方法的代码将不会在 DefterVM (Defter Virtual Machine) 虚拟机中运行。
## 3. 发布版本

| 模块 | 版本 | 发布时间 |
| --- | --- | --- |
| `defter` | `2.0 Beta` | `2021/8/27` |
| `defter` | `1.0 Beta2` | `2021/8/12` |
| `defter` | `1.0 Beta` | `2021/7/22` |

### 当前版本  

####修复问题:   
> `2021/7/22 1.0 Beta issues` 在Mac操作系统下可能无法正常使用defter-cli来创建新的项目。  
`2021/8/12 1.0 Beta2 issues` 解决了高并发异步方法引起的严重性阻塞问题。  

####新增特性:   
> 1 后端 (back-end) 引入基于线程的协程并发，绕过Python GIL全局解释器锁，大幅提升App性能，解决了高并发异步方法引起的严重性阻塞问题。  
2 前端 (front-end) 的模拟Python实现由原先的纯解释器解释模式转变为编译解释混合执行模式，并可与Google Chromium V8 JIT即时编译技术相互工作，大幅提升加载速度以及性能。  
3 前端 (front-end) 让重要逻辑运行在 DefterVM (Defter Virtual Machine) 虚拟机上，在尽可能不损失性能的情况下，使得Javascript解释器无权干涉内建虚拟机从而保证执行的安全，大幅降低了前端 (front-end) 被恶意调试代码的可能。

####已知问题:   
> 由于基于线程的协程引入，暂不支持中央处理器单元的多核心负载分配。

### 历史  

`2021/7/22` 发布的第一个版本  
已知问题: 在Mac操作系统下可能无法正常使用defter cli来创建新的项目。

`2021/8/12` 执行重构  
部分代码用C lang重构, 方法映射和传递的速度提升4倍。  
已知问题:  
1 在Mac操作系统下仍然可能无法正常使用defter cli来创建新的项目。  
2 分布请求时，异步高并发导致线程阻塞。

`2021/8/20` Defter 2.0 beta 计划启动。


## 4. References & Thanks

| Projects | URLs |
| --- | --- |
| Eel | https://github.com/ChrisKnott/Eel |
| Transcrypt | https://github.com/QQuick/Transcrypt |
