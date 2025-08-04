from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
from maa.context import Context


from .utils import Prompt

isMimicryAid = False


# 初始化
@AgentServer.custom_action("platform_init")
class PlatformInit(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            isMimicryAid = False
            return True

        except Exception as e:
            return Prompt.error("初始化蓝色站台", e)


# 检测是否选择助战
@AgentServer.custom_action("platform_mimicry_aid")
class PlatformMimicryAid(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            if isMimicryAid:
                return False

            isMimicryAid = True
            return True
        except Exception as e:
            return Prompt.error("选择特工", e)


# 检测是否满进度
@AgentServer.custom_recognition("check_platform_process")
class CheckPlatformProcess(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            reco_detail = context.run_recognition("蓝色站台_识别分数", argv.image)

            for res in reco_detail.all_results:
                scores = res.text.split("/")
                if len(scores) == 2:
                    if scores[0] == scores[1]:
                        return CustomRecognition.AnalyzeResult(
                            box=res.box,
                            detail=res.text,
                        )

            return CustomRecognition.AnalyzeResult(box=None, detail="无目标")

        except Exception as e:
            return Prompt.error("识别蓝色站台分数", e, reco_detail=True)
