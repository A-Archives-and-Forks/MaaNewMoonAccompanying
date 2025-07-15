from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

from typing import Dict, Any
import os
import json
import re
import random


# 解析查询字符串
def parse_query_args(argv: CustomAction.RunArg) -> dict[str, Any]:
    if not argv.custom_action_param:
        return {}

    # 预处理参数：去除首尾引号并按'&'分割参数列表
    args: list[str] = argv.custom_action_param.strip("\"'").split("&")

    # 解析键值对到字典
    params: Dict[str, Any] = {}
    for arg in args:
        # 分割键值
        parts = arg.split("=")
        if len(parts) >= 2:
            params[parts[0]] = parts[1]

    return params


# 解析列表输入
def parse_list_input(input: str, split_regex=r",\s*|，\s*|、\s*|\s+") -> list[str]:
    if not input:
        return []

    items = re.split(split_regex, input)
    items = [item for item in items if item]

    return items


# 提示
class Prompt:
    @staticmethod
    def log(
        content: str, use_default_prefix=True, pre_devider=False, post_devider=False
    ):
        if pre_devider:
            print("——" * 5)
        if use_default_prefix and not (pre_devider or post_devider):
            content = f"> {content}"
        print(f"{content}")
        if post_devider:
            print("——" * 5)

    @staticmethod
    def error(
        content: str, e: Exception = None, reco_detail=None, use_defult_postfix=True
    ):
        if use_defult_postfix:
            content += "失败，请立即停止运行程序！"
        print("——" * 5)
        print(f"{content}")
        if e is not None:
            print("错误详情：")
            print(e)
        print("——" * 5)
        return (
            CustomAction.RunResult(success=False)
            if reco_detail == None
            else CustomRecognition.AnalyzeResult(
                box=None, detail="程序错误" if reco_detail == True else reco_detail
            )
        )


# 本地存储
class LocalStorage:
    # 存储文件路径
    agent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(agent_dir, "..", "config")
    storage_path = os.path.join(config_dir, "mnma_storage.json")

    # 检查并确保存储文件存在
    @classmethod
    def ensure_storage_file(cls):
        # 确保配置目录存在
        if not os.path.exists(cls.config_dir):
            os.makedirs(cls.config_dir)

        # 确保存储文件存在
        if not os.path.exists(cls.storage_path):
            with open(cls.storage_path, "w") as f:
                json.dump({}, f)

    # 读取存储数据
    @classmethod
    def read(cls) -> dict:
        cls.ensure_storage_file()
        try:
            with open(cls.storage_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 存储文件格式错误时重置为空对象
            with open(cls.storage_path, "w") as f:
                json.dump({}, f)
            return {}

    # 获取存储值
    @classmethod
    def get(cls, task: str, key: str) -> str | bool | int | None:
        storage = cls.read()
        task_storage = storage.get(task)
        if task_storage is None:
            return None
        return task_storage.get(key)

    # 写入存储数据到文件
    @classmethod
    def write(cls, storage: dict) -> bool:
        try:
            with open(cls.storage_path, "w") as f:
                json.dump(storage, f)
            return True
        except Exception as e:
            print(f"存储数据时出错: {e}")
            return False

    # 设置存储值
    @classmethod
    def set(cls, task: str, key: str, value: str | bool | int) -> bool:
        storage = cls.read()
        if task not in storage:
            storage[task] = {}
        storage[task][key] = value

        return cls.write(storage)


# 全局设置
class Configs:
    configs = {}

    @classmethod
    def set(cls, key: str, value: str):
        # 转义类型
        if value == "true":
            value = True
        elif value == "false":
            value = False
        elif value.isdigit():
            value = int(value)

        cls.configs[key] = value

    @classmethod
    def get(cls, key: str, default=None) -> str | bool | int | None:
        if (key not in cls.configs) and (default is not None):
            cls.configs[key] = default
        return cls.configs.get(key, default)
