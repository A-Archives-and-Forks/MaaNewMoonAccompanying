from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args,Prompt

import json



# 记录进入助战节点前的行动类型 4x行动/3x及以下行动 助战结束后执行此行动
@AgentServer.custom_action("record_action_type")
class RecordActionType(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            # 从argv中获取行动类型
            args = parse_query_args(argv)
            action_type = args.get("a")
            print(" 记录行动类型" + action_type)
            if action_type:
                # 修改助战_结束节点的next为记录的行动类型
                context.override_pipeline({
                    "清体力_助战结束": {
                        "next": [action_type]
                    }
                })
                return CustomAction.RunResult(success=True)
            return CustomAction.RunResult(success=False)
        except Exception as e:
            print(e + " record_action_type失败")
            Prompt.error("记录进入助战节点前的行动类型", e)

