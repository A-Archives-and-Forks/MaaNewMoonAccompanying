from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import re

from .utils import parse_query_args, parse_list_input, Prompt

index = 0


@AgentServer.custom_action("set_procurement_list")
class SetProcurementList(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index
        index = 0

        try:
            args = parse_query_args(argv)
            white: str = args.get("white")
            black: str = args.get("black")

            # 白名单
            white_list = parse_list_input(white)
            if len(white_list) > 0:
                print(f"> 物资白名单：{white_list}")
            context.override_pipeline(
                {"卡带词条_检测是否为目标属性": {"expected": white_list}}
            )

            # 黑名单
            black_list = parse_list_input(black)
            if len(black_list) > 0:
                print(f"> 物资黑名单：{black_list}")
            else:
                black_list = "我全都要！"
            context.override_pipeline(
                {"卡带词条_检测属性值是否正确": {"expected": black_list}}
            )

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("设置物资黑白名单", e)


@AgentServer.custom_action("select_next_procurement")
class SelectNextProcurement(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global index

        try:
            if index > 3:
                return CustomAction.RunResult(success=False)

            roi = [320 + index * 228, 380, 200, 230]
            context.override_pipeline(
                {
                    "每日采购_识别是否为数构银物资": {"roi": roi},
                    "每日采购_检查是否已购买": {"roi": roi},
                    "每日采购_检测是否为特惠": {"roi": roi},
                    "每日采购_检测是否为超值": {"roi": roi},
                    "每日采购_检测是否在白名单": {"roi": roi},
                    "每日采购_检测是否在黑名单": {"roi": roi},
                    "每日采购_点击详情页": {"target": roi},
                }
            )
            index += 1
            print(f"> 检测物资[2, {index}]")

            return CustomAction.RunResult(success=True)

        except Exception as e:
            return Prompt.error("设置物资检测区域", e)
