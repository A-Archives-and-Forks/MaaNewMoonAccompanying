from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt, Configs


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
            args = parse_query_args(argv)
            is_block = args.get("block", False)
            if is_block:
                is_block = True

            if len(delay_focus) > 0:
                print("——————————")
                print("注意：", flush=True)
                for key, focus in delay_focus.items():
                    time.sleep(0.1)
                    print(f" * {focus}", flush=True)
                    time.sleep(0.1)
                print("——————————")
                delay_focus = {}
                return not is_block
            else:
                print("> 无需提醒项")
                delay_focus = {}
                return True

        except Exception as e:
            return Prompt.error("延迟提醒", e)


# 全局设置
@AgentServer.custom_action("set_config")
class SetConfig(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", None)
            value = args.get("value", None)

            if key == None or value == None:
                return Prompt.error("未定义的全局设置值", use_defult_postfix=False)

            Configs.set(key, value)
            return True

        except Exception as e:
            return Prompt.error("全局设置", e)


# 判断bool设置
@AgentServer.custom_action("judge_config")
class SetConfig(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", None)
            default = args.get("default", False)

            if key == None:
                return Prompt.error("未定义的全局设置", use_defult_postfix=False)
            if default == "true":
                default = True
            else:
                default = False

            value = Configs.get(key, default)
            return value

        except Exception as e:
            return Prompt.error("判断bool设置", e)
