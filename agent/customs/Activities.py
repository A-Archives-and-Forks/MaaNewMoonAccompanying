from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt, RecoHelper, get_controller


# 自动炒菜
type_num = 1
current_type = 1
round_times = 0


# 初始化
@AgentServer.custom_action("init_cook")
class InitCook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global type_num, current_type, round_times
        try:
            args = parse_query_args(argv)
            num = args.get("type_num", "1")
            type_num = int(num)

            current_type = 1
            round_times = 0

            return True
        except Exception as e:
            return Prompt.error("初始化自动炒菜", e)


# 点击位置
@AgentServer.custom_action("auto_cook")
class AutoCook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global type_num, current_type, round_times
        try:
            # 识别采购单
            reco_helper = RecoHelper(context)
            reco_helper.recognize("自动炒菜_识别采购单")
            if reco_helper.hit():
                print("> 尝试使用采购单")
                context.run_task("自动炒菜_使用")

            # 菜品名称
            if current_type == 1:
                zh_name = "主菜"
                en_name = "entree"
            elif current_type == 2:
                zh_name = "主食"
                en_name = "carbs"
            elif current_type == 3:
                zh_name = "甜品"
                en_name = "dessert"
            else:
                return Prompt.error("未知的菜品！", use_defult_postfix=False)

            # 点击五次当前菜品
            print("> 正在烹饪：" + zh_name)
            for i in range(3):
                get_controller(context).post_click(
                    130, 330 + 140 * (current_type - 1)
                ).wait()
                if is_cook_end(context):
                    return False
                time.sleep(0.3)

            # 直接提交
            if serve_dish(context):
                return False

            # 检测最高菜品
            biggest_dish = {1: 1, 2: 1}
            for i in range(1, 3):
                for j in range(2, 6):
                    if reco_dish(context, en_name, i, j, [306, 167, 827, 63]).hit():
                        biggest_dish[i] = j
            print(f"> 当前最大{zh_name}：1-{biggest_dish[1]}，2-{biggest_dish[2]}")

            # 删除最高菜品
            for i in range(1, 3):
                if biggest_dish[i] >= 4:
                    continue
                for j in range(4, 6):
                    reco_helper = reco_dish(context, en_name, i, j)
                    if not reco_helper.hit():
                        continue
                    results = RecoHelper.filter_reco(reco_helper.reco.all_results, 0.75)
                    if len(results) > 0:
                        print(f"> 回收{zh_name}{i}-{j}")
                    for res in results:
                        target = RecoHelper.get_reco_center(res)
                        get_controller(context).post_click(target[0], target[1]).wait()
                        time.sleep(0.2)
                        context.run_task("自动炒菜_回收")

            # 仅低等级菜品
            for i in range(1, 3):
                if biggest_dish[i] < 3:
                    biggest_dish[i] = 5

            # 合成菜品
            for i in range(1, 3):
                for j in range(1, biggest_dish[i]):
                    is_synthesis = False
                    reco_times = 0
                    while reco_times < 5:
                        # 检测是否有此菜品
                        reco_helper = reco_dish(context, en_name, i, j)
                        reco = reco_helper.reco
                        if not reco:
                            break
                        results = reco.all_results
                        results = RecoHelper.filter_reco(results, 0.75)
                        if len(results) < 2:
                            break

                        # 合成
                        print(f"> oi，拼好饭！({zh_name}{i}-{j+1})")
                        target_1 = reco_helper.get_reco_center(results[0])
                        target_2 = reco_helper.get_reco_center(results[1])
                        get_controller(context).post_swipe(
                            target_1[0],
                            target_1[1],
                            target_2[0],
                            target_2[1],
                            100,
                        ).wait()
                        is_synthesis = True
                        reco_times += 1
                        time.sleep(0.1)
                    if is_synthesis:
                        if serve_dish(context):
                            return False

            # 换菜
            current_type += 1
            if current_type > type_num:
                current_type = 1
            round_times += 1

            return True
        except Exception as e:
            return Prompt.error("自动炒菜", e)


# 识别菜品
def reco_dish(context: Context, en_name, i, j, roi=[292, 278, 917, 340]):
    dish_template = f"activity/{en_name}/{i}{j}.png"
    reco_helper = RecoHelper(context)
    reco_helper.recognize(
        "自动炒菜_识别菜品",
        {"template": dish_template, "roi": roi},
    )
    return reco_helper


# 上菜
def serve_dish(context: Context):
    while True:
        # 识别是否可提交
        reco_helper = RecoHelper(context)
        reco_helper.recognize("自动炒菜_提交菜品")
        if reco_helper.reco is None:
            break

        # 提交菜品
        print("> 菜齐了老铁！")
        target = reco_helper.get_target()
        get_controller(context).post_click(target[0], target[1]).wait()
        time.sleep(2)

        # 检测是否完成
        reco_helper = RecoHelper(context)
        reco_helper.recognize("自动炒菜_挑战完成")
        if reco_helper.reco is not None:
            return True

    return False


def is_cook_end(context: Context):
    reco_helper = RecoHelper(context)
    reco_helper.recognize("自动炒菜_材料数量不足")
    if reco_helper.hit():
        print("> 已无剩余材料")
        return True
    return False
