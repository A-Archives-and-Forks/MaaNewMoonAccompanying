from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt

import time


current_time = 0
limit_time = 0


@AgentServer.custom_action("init_timer")
class InitTimer(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global current_time, limit_time

        try:
            args = parse_query_args(argv)
            limit = args.get("limit")

            current_time = time.time()
            if limit:
                limit_time = int(limit)
            else:
                limit_time = 0

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("初始化计时器", e)


@AgentServer.custom_action("check_time")
class CheckTime(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global current_time, limit_time

        try:
            diff = time.time() - current_time

            if diff > limit_time:
                return CustomAction.RunResult(success=False)
            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("检查时间", e)
