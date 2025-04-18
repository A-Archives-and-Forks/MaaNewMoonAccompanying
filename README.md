<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="./logo.png" width="256" height="256" />
</p>

<div align="center">

# MNMA - 新月同行小助手</br>MaaNewMoonAccompanying</br>✨ 组长们的超级秋千人✨ 

基于全新架构的 [**新月同行**](https://xytx.firewick.net/home) 小助手<br/>图像技术 + 模拟控制，解放双手，由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 与 [MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia) 强力驱动！

<p align="center">
  <img src="https://img.shields.io/github/license/kqcoxn/MaaNewMoonAccompanying">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pipeline-%23454545?logo=paddypower&logoColor=%23FFFFFF">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20android-blueviolet">
  <img src="https://img.shields.io/github/commit-activity/m/kqcoxn/MaaNewMoonAccompanying">
  <img src="https://img.shields.io/github/stars/kqcoxn/MaaNewMoonAccompanying?style=social">
  <img src="https://img.shields.io/badge/Group-993245868-0e80c1?logo=qq&logoColor=white&url=http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=VMC132QhbMDLi5U62MlDRvtCMj9WOXRr&authKey=yJNKO4sQ%2BBFHpBCLSSEvVOAyz%2FPjknNSl70W3ugg2%2BpELnKmEiHamj1emJMWcLwQ&noverify=0&group_code=993245868">
</p>

</div>

## 功能列表

### 常驻功能

- [x] 自动登录（领取签到）
- [x] 城市探索（资源收取、制造订单、设施管理、传闻调查、城市事件）
- [x] 每日采购（每日免费、数构银物资）
- [x] 领取奖励（任务/手册）
- [x] 友谊交换
- [x] 清体力（支持所有资源）
- [ ] 自动站台肉鸽
- [ ] 自动卡带特征激活（游戏改版后开发）

\* 若有其他功能需求请提交 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues?q=is%3Aissue)

### 活动功能

> 本期活动：禅世遗香 (2025.4.3 - 2025.4.30)

- [x] 领取每日禅香

\* 不在列表上的活动不会开发

<!-- <details>
<summary>往期活动</summary>

</details> -->

## 使用教程

> 教程视频正在筹备中，预计随正式版更新。

**每次版本更新后请手动把仅第一次出现的界面过一遍！**

- [文图教程](/docs/zh_cn/使用教程.md)


## 常见问题

在一切问题之前，请先确保你的`Python`与`MaaFw`框架环境正常，具体可参考这篇 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/4)

请确保现有 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues?q=is%3Aissue) 中还没有与您遇到的类似的问题

- **程序运行类**
  - [任务停留在“正在启动 Agent(耗时可能较久)”](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/4)
  - [修改连接部分的控制器ADB地址会卡死](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/2)
  - [在关闭MFAAvalonia.exe之后，左下状态栏依然会有MFA管理器图标，且点击无效](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/6)

特别感谢 [@Yakir-George](https://github.com/Yakir-George) 在项目开发时期的测试与反馈！

如果有其他问题，欢迎提交 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues?q=is%3Aissue)，您的反馈将使更多组长受益！

## 更新记录

<!-- ### Next Release (Committed but Unreleased) -->

### v0.3.1

> 2025.4.18

- **新增**
  - 新增功能：自动城市事件（测试）
  - 新增选项：清体力-自动使用稳定合剂
- **修复优化**
  - 优化了清体力的倍速判断机制，提高效率

### v0.3.0

> 2025.4.18

- **新增**
  - 实装清体力功能

<details>
<summary>更早的版本</summary>

### v0.2.7

> 2025.4.17

- **新增**
  - 新增选项：启动游戏-防止版本资讯延迟、启动游戏-紧张刺激的七日签到、启动游戏-检查邮箱
- **修复优化**
  - 修复了数构银物资已买后界面会卡住无法返回的问题，并新增选项：启用构束银再确认
  - 修复了若情报点数已赠送但未获取则会卡住的问题
  - 现有功能新版本适配

### v0.2.6

> 2025.4.16

- **修复优化**
  - 优化了首次启动游戏时可能会延迟且必定出现公告的问题，并添加选项：启动游戏-防止公告延迟
  - 修复了有助战时会卡在友谊互换界面前的问题

### v0.2.5

> 2025.4.15

- **新增**
  - 新增功能：【禅世遗香】领取每日奖励
  - 说明回来了！~~还带来了超级秋千人！~~
- **修复优化**
  - 修复了领取任务时，若无每周任务可领取则会卡住的问题
  - 调整了启动游戏时的识别逻辑，可预判部分未知情况
  - 修复了 CLI 无法设置选项的问题

### v0.2.4

> 2025.4.14

- **新增**
  - 添加了“关闭游戏”任务，用于仅退出游戏但不关闭模拟器的情况，支持检测主界面后退出
- **修复优化**
  - 修复了启动游戏时容易被每日签到阻塞的问题
  - 修正了“数构银”的文本错误
  - 暂时删除了“说明”功能以防止MFA显示异常
  - 修复了`interface.json`无法被 CLI 正常导入的bug
  - 优化了部分逻辑，提高效率与稳定性

### v0.2.3

> 2025.4.13

- 添加独立选项：每日采购-购买数构银物资
- 修复了组长手册升级时任务阻塞的问题

### v0.2.2

> 2025.4.13

- 修复了容易卡在领取确认界面的问题
- 修复了手册界面切换面板失效的问题
- 优化了部分逻辑，提高稳定性

### v0.2.1

> 2025.4.12

- 实装友谊交换、领取奖励功能
- 大幅度优化现有流程，更加稳定且高效
- 所有任务结束后主动回到主页，可连续执行其他任务
- 将 GUI 迁移至 [MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia/tree/master)
- ~~抓了只秋千人当 icon~~

### v0.1.1

> 2025.3.23

- 实现自动登录功能
- 实现每日采购功能
- 优化了部分逻辑

### v0.1.0

> 2025.3.22

- 初次提交
- 实装一键收菜功能
- 实装自动爬塔功能

</details>

## 鸣谢

- 本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！
- GUI：[MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia/tree/master)
- Pipeline 编辑器：[YAMaaPE](https://github.com/kqcoxn/YAMaaPE)

游戏官网：[烛薪网络-新月同行](https://xytx.firewick.net/home)

## 加入我们

- 🐧~~吹水~~交流群：[993245868](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=VMC132QhbMDLi5U62MlDRvtCMj9WOXRr&authKey=yJNKO4sQ%2BBFHpBCLSSEvVOAyz%2FPjknNSl70W3ugg2%2BpELnKmEiHamj1emJMWcLwQ&noverify=0&group_code=993245868)

