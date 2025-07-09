from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt


delay_focus = {}


# 添加延迟提醒
@AgentServer.custom_action("delay_focus_hook")
class DelayFocusHook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global delay_focus
        try:
            args = parse_query_args(argv)
            key = args.get("key", "")
            focus = args.get("focus", "")
            delay_focus[key] = focus
            return True
        except Exception as e:
            return Prompt.error("添加延迟提醒", e)


# 延迟提醒
@AgentServer.custom_action("delay_focus")
class DelayFocus(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global delay_focus
        try:
            if len(delay_focus) > 0:
                print("——————————")
                print("注意：", flush=True)
                for key, focus in delay_focus.items():
                    time.sleep(0.1)
                    print(f" * {focus}", flush=True)
                    time.sleep(0.1)
                print("——————————")
                delay_focus = {}
                return False
            else:
                print("> 无需提醒项")
                delay_focus = {}
                return True

        except Exception as e:
            return Prompt.error("延迟提醒", e)
