# OneRaid
OneRaid 是集合各种Raid卡操作小工具 🚀

## 上手指南


## 工具介绍
工具地址：https://github.com/robertruan-x/OneRaid

在服务器命令行下尝试对raid卡进行操作(查看raid卡信息, 制作raid,设置磁盘状态灯...)的时候，发现有以下问题：
- **学习成本高** ，每个raid卡厂家都使用不同的控制软件，这些命令虽然功能类似但是各有各的操作方式
- **操作麻烦**，要控制这些raid卡，不仅找对应软件下载，有的操作还需要各种查询后才能再操作（尤其是点亮磁盘灯的时候）

为了解决这些问题，该项目从而诞生，正如其名，OneRaid将会集成各种raid卡操作把他们的功能抽象出来，你可以通过OneRaid控制不同类型raid软件来完成你的工作。


当然项目中也会有各种raid控制软件的教学，你也能在这里学习到各种raid软件的操作命令和例子😊

目前OneRaid还在开发中，如果各位有任何问题和改进建议，欢迎提交Issues和PR，如果项目对你有用，可以给它一个星星✨支持一下

## 功能特性
基础信息收集
- [ ] 展示raid卡信息
- [ ] 展示物理磁盘信息
- [ ] 展示raid组信息
- [ ] raid卡日志收集和展示

raid操作
- [ ] raid创建和删除

其他操作
- [ ] 磁盘定位灯点亮
- [ ] raid卡控制参数设置

## 目录结构

项目docs文件包含一些帮助和说明文档, 还有各种raid控制器软件介绍说明和输出展示

## 依赖环境
- [ptables]() - python数据图表展示库
- [arcconf]() - 一种raid控制软件
- [strocli64]() - 一种raid控制软件
- [precli64]() - 一种raid控制软件
- [sas3iru]() - 一种raid控制软件
- [sas2iru]() - 一种raid控制软件

## 后续计划