from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt


@AgentServer.custom_action("set_ice_squad")
class SetIceSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            squad = args.get("s", "")

            if squad != "":
                context.override_pipeline(
                    {
                        "冰饮_开始个人挑战": {"next": "冰饮_个人队伍"},
                        "冰饮_开始协助挑战": {"next": "冰饮_助战队伍"},
                    }
                )
                print(f"> 行动将使用队伍：{squad}")

            return CustomAction.RunResult(success=True)
        except Exception as e:
            return Prompt.error("设定指定队伍", e)
