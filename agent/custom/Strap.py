from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import re

from .utils import parse_query_args, Prompt

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
            return Prompt.error("初始化卡带升级", e)


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
            return Prompt.error("初始化卡带升级", e)


@AgentServer.custom_action("set_strap_attr")
class SetStrapAttr(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:

        try:
            args = parse_query_args(argv)
            attr: str = args.get("attr")
            value: str = args.get("value")

            attrs = re.split(r",\s*|，\s*|、\s*|\s+", attr)
            attrs = [a for a in attrs if a]
            print(f"> 目标属性：{attrs}")
            context.override_pipeline(
                {"卡带词条_检测是否为目标属性": {"expected": attrs}}
            )

            values = re.split(r",\s*|、\s*|\s+", value)
            values = [v for v in values if v]
            if len(values) > 0:
                print(f"> 目标数值：{values}")
            context.override_pipeline(
                {"卡带词条_检测属性值是否正确": {"expected": values}}
            )

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("初始化卡带升级", e)
