from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt
from .MatrixScheduling import StepMatrixManager


# 环线调度
# 点击位置
@AgentServer.custom_action("loop_dispatching")
class LoopDispatching(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            index = (int(args.get("col")), int(args.get("row")))

            point = StepMatrixManager.get().get_point(index)
            print(f"> [{index[0]}, {index[1]}] 准备发车")
            context.run_action(
                "环线调度_点击",
                pipeline_override={
                    "环线调度_点击": {"target": [point[0], point[1], 1, 1]}
                },
            )

            return True

        except Exception as e:
            return Prompt.error("环线调度", e)
