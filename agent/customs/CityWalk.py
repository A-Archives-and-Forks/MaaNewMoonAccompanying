from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt


@AgentServer.custom_action("set_event_squad")
class SetEventSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            squad = args.get("s", "")

            if squad != "":
                print(f"> 行动将使用队伍：{squad}")
            else:
                context.override_pipeline(
                    {
                        "城市探索_进入战斗": {"next": "城市探索_开始战斗"},
                    }
                )

            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("设定指定队伍", e)


entrustment_roi_index = 0  # roi位置
entrustment_best_reward = None  # 最佳选项
entrustment_etter_reward = None  # 次级选项


def calculate_roi(index: int) -> list[int]:
    """计算委托事件选项的ROI区域

    Args:
        index: ROI索引位置

    Returns:
        list[int]: ROI区域坐标 [x, y, width, height]
    """
    return [840, 225 + index * 85, 220, 70]


def set_reward_pipeline(context: Context, roi: list[int]) -> None:
    """设置委托事件选项的pipeline

    Args:
        context: 上下文对象
        roi: ROI区域坐标
    """
    context.override_pipeline(
        {
            "城市探索_识别下一区域": {
                "next": ["城市探索_点击奖励选项"],
            },
            "城市探索_点击奖励选项": {
                "target": roi,
            },
        }
    )


# 初始化识别区域
@AgentServer.custom_action("init_reward")
class InitReward(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global entrustment_roi_index
        global entrustment_best_reward
        global entrustment_etter_reward
        try:
            entrustment_roi_index = 0
            entrustment_best_reward = None
            entrustment_etter_reward = None
            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("初始化委托事件选项", e)


# 更新识别区域
@AgentServer.custom_action("select_next_reward")
class SelectNextReward(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global entrustment_roi_index
        try:
            if entrustment_roi_index > 2:
                return CustomAction.RunResult(success=True)
            entrustment_roi_index += 1
            roi = calculate_roi(entrustment_roi_index)
            context.override_pipeline(
                {
                    "城市探索_识别指定类型": {"roi": roi},
                    "城市探索_识别非指定高收益": {"roi": roi},
                }
            )
            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("设置委托事件选项", e)


# 判断当前选项 找出最佳奖励
@AgentServer.custom_action("compare_reward")
class CompareReward(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global entrustment_roi_index
        global entrustment_best_reward
        global entrustment_etter_reward
        try:
            args = parse_query_args(argv)
            # 识别结果
            result = args.get("result")
            # 是否只要指定选项
            normal_first = args.get("normal_first")
            # 判断当前选项的识别结果
            # best 是指定选项且是高风险高收益
            if result == "best":
                entrustment_best_reward = entrustment_roi_index
            # better 非指定选项但是高风险高收益
            elif result == "better":
                if entrustment_etter_reward == None:
                    entrustment_etter_reward = entrustment_roi_index
            # normal 是指定选项但非高风险高收益
            elif result == "normal":
                if normal_first == "true":
                    entrustment_etter_reward = entrustment_roi_index

            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("判断委托事件选项结果", e)


# 循环满三次/已找到最佳选项 则中断循环
@AgentServer.custom_action("end_reward_loop")
class BreakLoop(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global entrustment_roi_index
        global entrustment_best_reward
        global entrustment_etter_reward
        try:
            final_index = 0
            if entrustment_best_reward != None:
                final_index = entrustment_best_reward
            elif entrustment_etter_reward != None:
                final_index = entrustment_etter_reward
            # 更新最终的点击区域
            roi = calculate_roi(final_index)
            # 循环完三个选项 或者已经找到最佳选项
            if entrustment_roi_index == 2 or final_index == entrustment_best_reward:
                # print(f'> 循环完三次 决定选 {final_index}')
                set_reward_pipeline(context, roi)
            # 循环超过三次仍未识别到，则选择第一个选项
            elif entrustment_roi_index > 2:
                # print(f'> 超过三次仍未识别到 只好选第一个了')
                set_reward_pipeline(context, calculate_roi(0))
            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("中断委托事件循环", e)
