from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt, Tasker


class StepMatrix:
    def __init__(self, origin: tuple, step_size: tuple):
        self.origin = origin
        self.step_size = step_size

    def get_point(self, row: int = 1, col: int = 1) -> tuple:
        return (
            self.origin[0] + self.step_size[0] * (col - 1),
            self.origin[1] + self.step_size[1] * (row - 1),
        )

    def click(self, context: Context, row: int = 1, col: int = 1) -> bool:
        target = self.get_point(row, col)
        Tasker.get_controller(context).post_click(*target).wait()


class StepMatrixManager:
    step_matrixes = {}

    @classmethod
    def init(cls, origin: tuple, step_size: tuple, key="default"):
        cls.step_matrixes[key] = StepMatrix(origin, step_size)
        return cls.step_matrixes[key]

    @classmethod
    def get(cls, key="default") -> StepMatrix:
        return cls.step_matrixes[key]


# 初始化矩阵
@AgentServer.custom_action("init_step_matrix")
class InitStepMatrix(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            origin = (int(args.get("ox")), int(args.get("oy")))
            step_size = (int(args.get("sx")), int(args.get("sy")))

            StepMatrixManager.init(origin, step_size)

            return True

        except Exception as e:
            return Prompt.error("初始化步长矩阵", e)
