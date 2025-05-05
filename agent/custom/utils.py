from maa.custom_action import CustomAction

from typing import Dict, Any
import os
import json


# 解析查询字符串
def parse_query_args(argv: CustomAction.RunArg) -> dict[str, Any]:
    if not argv.custom_action_param:
        return {}

    # 预处理参数：去除首尾引号并按'&'分割参数列表
    args: list[str] = argv.custom_action_param.strip("\"'").split("&")

    # 解析键值对到字典
    params: Dict[str, Any] = {}
    for arg in args:
        # 每个参数按第一个'='分割键值（支持含等号的值）
        params[arg.split("=")[0]] = arg.split("=")[1]

    return params


# 提示
class Prompt:
    @staticmethod
    def error(str: str, e: Exception = None):
        print(f"{str}失败，请立即停止运行程序！")
        if e is not None:
            print(e)
        return CustomAction.RunResult(success=False)


# 本地存储
class LocalStorage:
    # 存储文件路径
    agent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(agent_dir, "..", "config")
    storage_path = os.path.join(config_dir, "mnma_storage.json")

    # 检查并创建 config 文件夹
    @classmethod
    def ensure_config_dir(cls):
        if not os.path.exists(cls.config_dir):
            os.makedirs(cls.config_dir)

    # 检查文件是否存在
    @classmethod
    def read(cls) -> dict:
        cls.ensure_config_dir()
        if not os.path.exists(cls.storage_path):
            with open(cls.storage_path, "w") as f:
                json.dump({}, f)
            return {}
        return json.load(open(cls.storage_path, "r"))

    # 获取存储值
    @classmethod
    def get(cls, task: str, key: str) -> str | bool | int | None:
        storage = LocalStorage.read()
        task_storage = storage.get(task)
        if task_storage is None:
            return None
        return task_storage.get(key)

    # 设置存储值
    @classmethod
    def set(cls, task: str, key: str, value: str | bool | int) -> None:
        storage = LocalStorage.read()
        if task not in storage:
            storage[task] = {}
        storage[task][key] = value
        cls.ensure_config_dir()
        with open(cls.storage_path, "w") as f:
            json.dump(storage, f)
