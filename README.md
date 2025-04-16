<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="./logo.png" width="256" height="256" />
</p>

<div align="center">

# MNMA - 新月同行小助手</br>MaaNewMoonAccompanying</br>✨ 组长们的超级秋千人✨ 

项目正在绝赞开发中！

</div>

## 开发进度

> 在开发测试期间，可能会出现任何意想不到的问题，请谨慎使用！

开发计划：

- [x] 自动登录（领取签到）
- [x] 城市探索（资源收取、制造订单、设施管理、传闻调查）
- [ ] 城市事件
- [x] 每日采购（每日免费、数构银物资）
- [x] 领取奖励（任务/手册）
- [x] 友谊交换
- [ ] 消耗现实度（即清体力，支持任意材料）（**_v0.3.0即将上线！_**）
- [ ] 自动卡带特征激活（游戏改版后开发）
- [ ] 自动站台肉鸽
- [x] 【禅世遗香】领取每日奖励
- 更多活动功能适配（EX关卡、小游戏等，开发量较大，可能端上来比较慢）

\* 若有其他功能需求请提交 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues?q=is%3Aissue)

**如果你也是开发者，可以瞅一眼我的另一个项目 [YAMaaPE](https://github.com/kqcoxn/YAMaaPE)，可以使用基于 Web 的流水线 GUI 编辑你的 Pipeline！**

## 使用方式

当前可以使用命令行或GUI运行，根据提示进行下一步操作即可。

**每次版本更新后请手动把仅第一次出现的界面过一遍！**

功能说明：

|           功能           |    初始界面     | 结束界面 |              注意事项              |
| :----------------------: | :-------------: | :------: | :--------------------------------: |
|         自动登录         | 进入游戏前/首页 |   首页   |   活动奖励可能出问题，请注意更新   |
|         城市探索         |      首页       |   首页   |                 -                  |
|         每日采购         |      首页       |   首页   |                 -                  |
|         友谊交换         |      首页       |   首页   |                 -                  |
|         领取奖励         |      首页       |   首页   |   每次手册更新后需要手动进入一次   |
| 【禅世遗香】领取每日奖励 |      首页       |   首页   | 版本更新后请先进入活动过完开场动画 |
|         退出游戏         |  首页/任意界面  |    -     |        是否仅首页功能可配置        |

## 常见问题

在一切问题之前，请先确保你的`Python`与`MaaFw`框架环境正常，具体可参考这篇 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/4)

- **程序运行类**
  - [任务停留在“正在启动 Agent(耗时可能较久)”](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/4)
  - [修改连接部分的控制器ADB地址会卡死](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/2)
  - [在关闭MFAAvalonia.exe之后，左下状态栏依然会有MFA管理器图标，且点击无效](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues/6)

特别感谢 [@Yakir-George](https://github.com/Yakir-George) 在项目开发时期的测试与反馈！

如果有其他问题，欢迎提交 [issue](https://github.com/kqcoxn/MaaNewMoonAccompanying/issues?q=is%3Aissue)，您的反馈将使更多组长受益！

## 更新记录

<!-- ### Next Release (Committed) -->
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

<details>
<summary>更早的版本</summary>

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

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

- GUI：[MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia/tree/master)
- Pipeline 编辑器：[YAMaaPE](https://github.com/kqcoxn/YAMaaPE)
