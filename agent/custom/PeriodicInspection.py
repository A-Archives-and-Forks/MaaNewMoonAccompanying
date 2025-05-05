from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from typing import Optional
from datetime import datetime, date

from .utils import parse_query_args, LocalStorage, Prompt


class Inspector:
    # 记录检查
    @staticmethod
    def record(task: str) -> None:
        LocalStorage.set(task, "last_date", str(date.today()))

    # 是否在同一周
    @staticmethod
    def week(task: str) -> bool:
        current_date = date.today()
        last_date_str: Optional[str] = LocalStorage.get(task, "last_date")

        if not last_date_str:
            return False

        try:
            last_date = date.fromisoformat(last_date_str)
        except (ValueError, TypeError):  # 如果字符串格式不正确
            return False

        return (
            current_date.isocalendar()[1] == last_date.isocalendar()[1]
            and current_date.year == last_date.year
        )


# 周期检查
@AgentServer.custom_action("periodic_check")
class PeriodicCheck(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            periodic = args.get("p")
            task = args.get("t")

            flag = False
            if periodic == "week":
                flag = Inspector.week(task)

            if flag:
                print("周期检查成功！")
                return CustomAction.RunResult(success=False)
            else:
                return CustomAction.RunResult(success=True)

        except Exception as e:
            Prompt.error("检查周期任务失败", e)


# 记录检查
@AgentServer.custom_action("record_periodic_check")
class SetLastPeriodicCheck(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            task = args.get("t")

            Inspector.record(task)

            return CustomAction.RunResult(success=True)

        except Exception as e:
            Prompt.error("记录检查时间失败", e)
