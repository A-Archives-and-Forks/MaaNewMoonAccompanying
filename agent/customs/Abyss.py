from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
from maa.context import Context


from .utils import parse_query_args, Prompt, Judge


# 检测是否满进度
@AgentServer.custom_recognition("check_abyss_process")
class CheckAbyssProcess(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            return Judge.equal_process(
                context, argv, "险境复现_检测进度", return_analyze_result=True
            )

        except Exception as e:
            return Prompt.error("检查险境周期奖励", e, reco_detail=True)


# 检查是否填写编队
@AgentServer.custom_action("check_abyss_squad")
class CheckAbyssSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            squad_a = args.get("a", "")
            squad_b = args.get("b", "")
            return squad_a != "" and squad_b != ""
        except Exception as e:
            return Prompt.error("检查编队", e)
