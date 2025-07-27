# 项目结构

::: tip 注意
编写时基于 MNMA `v2.1.3` 版本
:::

## 项目目录

- `/.github`：存放 GitHub 配置文件，一般不用管
- `/DocSite`：文档站源码
- `/MFAAvalonia`：MFAAvalonia 本地调试存储
- `/MFATools`：MFATools 本地使用存储
- **`/agent`：存放 Custom 代码**
- **`/assets`：存放 Pipeline、Interface 文件与静态资源**
- `/ci`：存放自动化部署脚本，一般不用管
- `/deps`：存放 MaaFramework 依赖包
- `/dev`：存放开发相关脚本，可以在`开发相关.md`中查看调用方式
- `/docs`：存放不重要的文档，如更新记录等
- `/feedbacker`：自动打包小工具
- `/gc`：安全清理小工具
- `/launcher`：MNMA 启动器
- 其他文件：全局相关配置

## Custom 调用

MNMA 目前仅在 action 中调用 Custom

在需要使用 Custom 时，现有各文件总体功能如下：

- `/agent`
  - `main.py`、`dev_main.py`：agent 入口文件，一般不用修改
  - `setup.py`：本地环境更新器，在开发时无需关心
  - `custom.py`：导入相关子模块，在添加文件时需要在此处 import
  - `/customs`
    - `Abyss.py`：险境复现相关
    - `Activities.py`：活动相关
    - `AgentTraining.py`：特工界面相关
    - `CityWalk.py`：城市探索界面相关
    - `ConsumptiveRealism.py`：清体力相关
    - `Counter.py`：通用计数器
    - `IceDrink.py`：冰饮相关
    - `MatrixScheduling.py`：通用矩阵排布解决方案，一般用于需要矩阵分布点击的界面
    - `PipeLauncher.py`：需设置参数的 Pipeline 启动器
    - `Pipeliner.py`：通用 Pipeline 调度器
    - `Platform.py`：蓝色站台相关
    - `Procurement.py`：采购相关
    - `Strap.py`：卡带相关
    - `Timer.py`：通用独立计时器
    - `utils.py`：通用工具函数
