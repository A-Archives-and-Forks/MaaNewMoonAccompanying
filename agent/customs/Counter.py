from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, Prompt


class Counter:
    def __init__(self, max_count: int = 0, exceed: bool = True):
        self.count = 0
        self.max = max_count
        self.exceed = exceed

    def init(self, max_count: int = 0, exceed: bool = True):
        self.count = 0
        self.max = max_count
        self.exceed = exceed

    def increment(self):
        self.count += 1
        return self.count

    def is_max(self):
        if self.max <= 0:
            return False
        if self.exceed:
            return self.count > self.max
        else:
            return self.count >= self.max

    def get_count(self):
        return self.count

    def set_max(self, max_count: int, exceed: bool = True):
        self.max = max_count
        self.exceed = exceed


class CounterManager:
    def __init__(self):
        self.counters = {}

    def get(self, key: str = "default") -> Counter:
        if key not in self.counters:
            self.counters[key] = Counter()
        return self.counters[key]

    def remove(self, key: str):
        if key in self.counters:
            del self.counters[key]

    def reset(self, key: str, max_count: int = 0, exceed: bool = True):
        self.counters[key] = Counter(max_count, exceed)


counter_manager = CounterManager()


@AgentServer.custom_action("init_counter")
class InitCounter(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", "default")
            maxCount = args.get("max")
            exceed = args.get("exceed")
            maxCount = int(maxCount) if maxCount is not None else 0
            exceed = str(exceed).lower() != "false" if exceed is not None else True
            counter_manager.reset(key, maxCount, exceed)
            return True
        except Exception as e:
            return Prompt.error("初始化计数", e)


@AgentServer.custom_action("count")
class Count(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", "default")
            text = args.get("t", "")
            counter = counter_manager.get(key)
            counter.increment()
            if counter.is_max():
                return False
            if text:
                print(f"> 第{counter.get_count()}次{text}")
            return True
        except Exception as e:
            return Prompt.error("计数", e)
