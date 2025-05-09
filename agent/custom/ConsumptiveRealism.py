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

        try:
            times = 0
            args = json.loads(argv.custom_action_param)
            if args:
                times = args["times"]

            if times > 0:
                expected_times = times
                print(f"> 将自动使用 {expected_times} 次稳定合剂")
            else:
                expected_times = 0
            used_times = 0

            return CustomAction.RunResult(success=True)
        except Exception as e:
            print(f"设置合剂次数失败，请立即停止程序运行！")
            print(e)
            return CustomAction.RunResult(success=False)


@AgentServer.custom_action("check_eat_times")
class SetEatTimes(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global expected_times, used_times

        try:
            used_times += 1
            if used_times > expected_times:
                return CustomAction.RunResult(success=False)
            else:
                print(
                    f"> 第 {used_times} 次使用稳定合剂，剩余 {expected_times - used_times} 次"
                )

            return CustomAction.RunResult(success=True)
        except Exception as e:
            print(f"检查合剂次数失败，请立即停止程序运行！")
            print(e)
            return CustomAction.RunResult(success=False)
