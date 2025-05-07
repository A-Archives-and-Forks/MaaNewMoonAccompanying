from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import Prompt

index = 0


# 记录检查
@AgentServer.custom_action("init_strap_upgrade")
class SetLastPeriodicCheck(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index

        try:
            index = 0
            return CustomAction.RunResult(success=True)

        except Exception as e:
            Prompt.error("初始化卡带升级", e)


@AgentServer.custom_action("select_next_strap")
class SetLastPeriodicCheck(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index

        try:
            if index > 3:
                return CustomAction.RunResult(success=False)

            context.override_pipeline(
                {"卡带升级_切换卡带": {"target": [66, 442 + index * 75, 1, 1]}}
            )
            index += 1

            return CustomAction.RunResult(success=True)

        except Exception as e:
            Prompt.error("初始化卡带升级", e)
