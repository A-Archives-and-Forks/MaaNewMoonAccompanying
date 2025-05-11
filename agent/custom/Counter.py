from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context


from .utils import parse_query_args, Prompt


count = 0


@AgentServer.custom_action("init_counter")
class InitCounter(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global count

        try:
            count = 0

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("初始化计数", e)


# 计数
@AgentServer.custom_action("count")
class Count(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global count

        try:
            args = parse_query_args(argv)
            text = args.get("t")

            count += 1
            print(f"> 第{count}次{text}")

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("计数", e)
