from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt


# 选择编队
@AgentServer.custom_action("run_set_squad")
class RunSetSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            expected = args.get("e", "")
            if expected == "":
                return False
            context.run_task(
                "选择编队_开始",
                {
                    "选择编队_检测配队是否正确": {"expected": expected},
                    "选择编队_查找指定队伍": {"expected": expected},
                },
            )
            return True
        except Exception as e:
            return Prompt.error("选择编队", e)
