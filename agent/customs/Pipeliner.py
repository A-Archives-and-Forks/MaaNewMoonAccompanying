from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, parse_list_input, Prompt


def parse_pipeline_args(argv: CustomAction.RunArg):
    args = parse_query_args(argv)
    node = args.get("node")
    keys = args.get("keys")
    values = args.get("values")
    return node, keys, values


@AgentServer.custom_action("set_str_node_attrs")
class SetStrNodeAttrs(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            node, keys, values = parse_pipeline_args(argv)
            keys = parse_list_input(keys)
            values = parse_list_input(values)

            if len(keys) != len(values):
                return Prompt.error("设置节点字符串类型属性", "keys和values长度不一致")

            for i in range(len(keys)):
                key = keys[i]
                value = values[i]
                if value == "[]":
                    value = []
                context.override_pipeline({node: {key: value}})

            return True
        except Exception as e:
            return Prompt.error("设置节点字符串类型属性", e)


@AgentServer.custom_action("break")
class Break(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        return False
