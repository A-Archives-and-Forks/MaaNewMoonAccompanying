from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt

roi_index = 0  # roi位置
best_reward = None  # 最佳选项
better_reward = None  # 次级选项


# 初始化识别区域
@AgentServer.custom_action("init_reward")
class InitReward(CustomAction):
    def run(
            self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global roi_index
        global best_reward
        global better_reward
        try:
            roi_index = 0
            best_reward = None
            better_reward = None
            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("初始化委托事件选项", e)


# 更新识别区域
@AgentServer.custom_action("select_next_reward")
class SelectNextReward(CustomAction):
    def run(
            self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global roi_index
        try:
            if roi_index > 2:
                return CustomAction.RunResult(success=False)
            roi_index += 1
            roi = [840, 225 + roi_index * 85, 220, 70]
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
        global roi_index
        global best_reward
        global better_reward
        try:
            args = parse_query_args(argv)
            # 识别结果
            result = args.get("result")
            # 是否只要指定选项
            normal_first = args.get("normal_first")
            # 判断当前选项的识别结果
            # best 是指定选项且是高风险高收益
            if result == "best":
                best_reward = roi_index
            # better 非指定选项但是高风险高收益
            elif result == "better":
                if better_reward == None:
                    better_reward = roi_index
            # normal 是指定选项但非高风险高收益
            elif result == "normal":
                if normal_first == 'true':
                    better_reward = roi_index
            final_index = 0
            if best_reward != None:
                final_index = best_reward
            elif better_reward != None:
                final_index = better_reward
            # 更新最终的点击区域
            roi = [840, 225 + final_index * 85, 220, 70]
            # 循环完三个选项 或者已经找到最佳选项
            if roi_index >= 2 or final_index == best_reward:
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
            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("判断委托事件选项结果", e)
