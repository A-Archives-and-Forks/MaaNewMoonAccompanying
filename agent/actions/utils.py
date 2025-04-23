from maa.custom_action import CustomAction

from typing import Dict, Any


def parse_args(argv: CustomAction.RunArg) -> dict[str, Any]:
    if not argv.custom_action_param:
        return {}
    args: list[str] = argv.custom_action_param.strip("\"'").split("&")
    params: Dict[str, Any] = {}
    for arg in args:
        params[arg.split("=")[0]] = arg.split("=")[1]
    return params
