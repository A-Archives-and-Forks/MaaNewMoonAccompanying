from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import json


expected_times = 0
used_times = 0


@AgentServer.custom_action("set_eat_times")
class SetEatTimes(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global expected_times, used_times

        args = json.loads(argv.custom_action_param)
        if args["times"]:
            expected_times = args["times"]
        else:
            expected_times = 0
        used_times = 0

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("check_eat_times")
class SetEatTimes(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global expected_times, used_times

        used_times += 1
        if used_times > expected_times:
            return CustomAction.RunResult(success=False)
        else:
            print(f"第 {used_times} 次使用稳定合剂，剩余 {expected_times - used_times} 次")

        return CustomAction.RunResult(success=True)
