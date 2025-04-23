from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from typing import Dict, Any, Optional
import json

from .utils import parse_args


@AgentServer.custom_action("log")
class Log(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        try:
            params = parse_args(argv)

            text: Optional[str] = params.get("t")
            if not text:
                return CustomAction.RunResult(success=True)

            print(f" > {text}")

            return CustomAction.RunResult(success=True)

        except Exception as e:
            print(e)
            print("未知的控制台提示，可能存在潜在错误！")
            return CustomAction.RunResult(success=True)
