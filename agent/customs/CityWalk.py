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
