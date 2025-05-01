from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import json


isMimicryAid = False


@AgentServer.custom_action("platform_init")
class PlatformInit(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            isMimicryAid = False
            return CustomAction.RunResult(success=True)

        except Exception as e:
            print(f"初始化蓝色站台失败，请立即停止程序运行！")
            print(e)
            return CustomAction.RunResult(success=False)


@AgentServer.custom_action("platform_mimicry_aid")
class PlatformMimicryAid(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            if isMimicryAid:
                return CustomAction.RunResult(success=False)

            isMimicryAid = True
            return CustomAction.RunResult(success=True)
        except Exception as e:
            print(f"选择特工失败，请立即停止程序运行！")
            print(e)
            return CustomAction.RunResult(success=False)
