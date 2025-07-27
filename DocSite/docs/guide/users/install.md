# 下载与安装

## 下载前须知

**对于下列环境，MNMA 不提供支持**：

- win7 及更早版本的 windows 系统
- 各类定制系统（如 XOS 等非官方系统）
- 各类微 PE 系统（辅助安装环境）
- HarmonyOS 系统
- 移动设备

**对于下列系统，MNMA 不提供安装教程与服务，仅提供打包自行尝试**：

- MacOS（且 mac 环境无新月 playcover 服务）
- Linux

**对于以下情况，MNMA 可能经常出现卡顿、失败等情况**：

- 网络环境波动较大（经常出现游戏内微卡顿）
- 电脑硬件配置较差（推荐 CPU ≥ i5 12400f/R5 5600X，内存 ≥ 16G，GPU 基本无要求）
- 同时运行多个/多开模拟器、 Maa 类软件或其他高算力需求软件
- 游戏处于开荒期，Box/事件解锁不满足 MNMA 逻辑需求（MNMA 只是帮忙完成重复日常，账号新内容无法跳过）
- 其他神秘设备原因（对于日常与周常，经常性的不同位置卡顿大概率为设备问题，偶尔卡顿大概率为 MNMA bug）

如果您不确定是否处于上述某一种情况，可以在群内请教群友。

## 下载 MNMA 压缩包

您可以在 Github 上下载 MNMA 的任意 Release 版本。

首先，打开 [MNMA Github Release 页面](https://github.com/kqcoxn/MaaNewMoonAccompanying/releases)。

![图片加载中，请稍等...](/users/release.png)

::: tip
如果 Github 页面打不开，请参考 [问题排查 - Github 页面打不开/下载缓慢](../users/errors.md#github-页面打不开-下载缓慢)
:::

一般，最上面的即为最新版。

下载适合自己系统的版本，目前 MNMA 支持 `Windows`、`Linux` 和 `MacOS` 系统，找到 `Assets` 列表中包含系统字段，点击链接即可下载。

![图片加载中，请稍等...](/users/assets.png)

::: tip
如果下载缓慢，请参考 [问题排查 - Github 页面打不开/下载缓慢](../users/errors.md#github-页面打不开-下载缓慢)
:::

注意事项：

- MNMA 在 **Windows 下仅支持 10 和 11**，旧版 Windows 请参阅 [MAA 常见问题](https://maa.plus/docs/zh-cn/manual/faq.html#%E7%B3%BB%E7%BB%9F%E9%97%AE%E9%A2%98) 中的系统问题部分。
- MNMA **暂不支持搭载 `Intel` 芯片的 MacBook**（包括双系统），`M`系列芯片建议进入交流群与群主说明后进行远程协助安装。
- MNMA 对于 Linux 的支持程度有限，仅打包可运行文件，如何运行与连接请自行探索。
- 若您希望操控 `Android` 实体设备，请前往[此页面](https://maa.plus/docs/zh-cn/manual/device/android.html)。 由于此方法涉及 adb 调试且仍需与电脑连接，不推荐使用此方法。

## \*Mirror 酱支持

在 [Mirror 酱](https://mirrorchyan.com/zh/projects?source=mnma-docsite) 官方的帮助下， MNMA 同样也接入了 Mirror 酱的国内高速下载与更新服务，详情请见[【Bilibili】震惊！MAA 开启收费功能？！](https://www.bilibili.com/video/BV1cZFreLEja)

**您可以通过 [此链接](https://mirrorchyan.com/zh/projects?rid=MNMA&source=mnma-docsite) 获取带有 Mirror 酱服务的 MNMA**。

简单来说，Mirror 酱（简称 mirrorc）是一个由开源社区维护的有偿分发平台，可以理解为一个中转站，从海外源获取一份最新版存至国内站点，当您需要时直接从国内站点下载。

由于海内外下载、站点维护等需要，mirrorc 会产生大量开销，因此 mirrorc 的服务是有偿的，但这**并不代表 MNMA 是收费的，您完全可以通过其他方式更新并无限制使用，仅在您需要 mirrorc 时才需要自行向 mirrorc 方付费，MNMA 社区并不承担此过程中的一切责任，当出现问题时您可以在 mirrorc 客户群联系客服解决。**

## 解压 MNMA

确认解压完整，并**确保将 MNMA 解压到一个独立的文件夹中**。

注意：除关闭内建管理员批准的 `Administrator` 账号外，请勿将 MAA 解压到如 `C:\`、`C:\Program Files\` 等需要 UAC 权限的路径。（如果看不懂，反正能不往 C 盘放就别往 C 盘放）

如果您不了解如何解压压缩包，可以参考：[【Bilibili】电子扫盲课之如何解压藏在视频里的压缩包简易教程](https://www.bilibili.com/video/BV1tZ421N7EV)

::: danger 注意
无论如何，请不要在压缩软件直接打开程序！
:::

MNMA 为可直接运行程序，无须安装等操作，在解压后您可以查看下一节手册尝试运行。
