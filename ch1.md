### 最简单的操作系统
- linux 1.0
### 三个project
- 进程管理——CPU
- 内存管理——内存
- 文件管理——disk
### 指令集
- OS是kernel，是用环0(特权指令集)的指令集写的
- 应用程序一般用到环3的指令集
### 一般我们装的Windows系统
- OS内核(希望尽可能小->微内核)
- system and application programs(辅助一大堆)
### OS做什么
- 向上服务
- $向下管理：\begin{cases}
 \text{硬件资源} \\
\text{软件资源} \end{cases}$

- $软件资源：\begin{cases}
 \text{CPU} \\
 \text{内存} \\
 \text{磁盘} \\
 \text{外设} \end{cases}$

- $CPU \begin{cases}
  并发: \text{用户感觉是并行，CPU中是串行} \\
  并行 \end{cases}$
  
### OS的目标
- 方便性
- 有效性

### 保护模式
- 保护硬件不受用户随意性的破坏，$360^。$：所用操作都要经过OS允许