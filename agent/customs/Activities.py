from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .MatrixScheduling import StepMatrixManager
from .utils import parse_query_args, Prompt, RecoHelperOld, RecoHelper, Tasker


# 码头八点半
pier_name = "码头一"
pier_level = "第1关"

pier_schedule = {
    "码头一": {
        "第1关": [
            (4, 6),
            (4, 7),
            (5, 2),
            (6, 6),
            (7, 3),
            (7, 7),
            (5, 3),
            (4, 5),
            (3, 5),
        ],
        "第2关": [
            (1, 3),
            (3, 9),
            (3, 3),
            (8, 3),
            (2, 5),
            (5, 7),
            (6, 7),
            (7, 5),
            (6, 2),
        ],
        "第3关": [
            (1, 6),
            (5, 7),
            (3, 1),
            (2, 3),
            (6, 6),
            (5, 6),
            (4, 5),
            (6, 4),
            (7, 3),
            (6, 1),
            (5, 2, 2),
        ],
        "第4关": [
            (1, 6),
            (2, 3),
            (7, 2),
            (3, 2),
            (4, 3),
            (7, 7),
            (6, 2),
            (5, 6),
            (6, 5),
            (2, 8),
        ],
        "第5关": [
            (2, 9),
            (6, 1),
            (7, 5),
            (7, 7),
            (1, 8),
            (3, 6),
            (3, 5),
            (4, 7),
            (2, 4),
            (3, 2),
            (5, 4),
            (4, 3),
        ],
        "第6关": [
            (1, 1),
            (4, 6),
            (4, 9),
            (7, 5),
            (3, 1),
            (2, 3),
            (1, 4),
            (8, 7),
            (7, 8),
            (3, 2),
            (6, 1),
            (5, 2),
            (8, 4),
            (4, 3),
        ],
        "第7关": [
            (4, 8),
            (2, 7),
            (3, 1),
            (3, 8),
            (1, 5),
            (4, 6),
            (3, 2),
            (5, 7),
            (8, 2),
            (7, 4),
            (2, 4),
            (7, 3),
            (1, 3),
            (6, 3),
        ],
        "第8关": [
            (1, 9),
            (2, 4),
            (3, 2),
            (5, 5),
            (3, 7),
            (8, 1),
            (7, 8),
            (8, 5),
            (7, 2),
            (4, 1),
            (6, 6),
            (5, 7),
            (1, 7),
            (6, 4),
        ],
        "第9关": [
            (1, 2),
            (1, 6),
            (2, 3),
            (2, 1),
            (4, 1),
            (2, 5),
            (4, 6),
            (6, 7),
            (5, 1),
            (5, 2),
            (5, 5),
            (7, 5),
            (8, 4),
            (7, 4),
        ],
        "第10关": [
            (1, 1),
            (3, 7),
            (4, 8),
            (8, 5),
            (2, 1),
            (7, 7),
            (7, 4),
            (5, 6),
            (2, 2),
            (4, 5),
            (8, 1),
            (3, 2),
            (7, 1),
            (6, 3),
            (7, 2),
        ],
    }
}


# 设置码头
@AgentServer.custom_action("set_pier")
class SetPier(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global pier_name
        try:
            args = parse_query_args(argv)
            pier_name = args.get("name", "码头一")
            Prompt.log(f"设置码头：{pier_name}")
            return True
        except Exception as e:
            return Prompt.error("设置码头", e)


# 设置码头关卡
@AgentServer.custom_action("set_pier_level")
class SetPierLevel(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global pier_level
        try:
            result = (
                RecoHelper(context).recognize("码头_关卡识别").reco_detail.best_result
            )
            if not result:
                return Prompt.error("关卡识别失败", use_defult_postfix=False)
            pier_level = result.text
            Prompt.log(f"当前关卡：{pier_level}")
            return True
        except Exception as e:
            return Prompt.error("设置关卡", e)


# 自动驾驶
@AgentServer.custom_action("auto_pier")
class AutoPier(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global pier_name, pier_level, pier_schedule
        try:
            # 初始化棋盘
            schedule = pier_schedule[pier_name][pier_level]
            if not schedule:
                return Prompt.error("关卡识别错误！", use_defult_postfix=False)
            matrix = StepMatrixManager.get()

            # 发船
            sleep_count = 0
            for coordinate in schedule:
                if Tasker.is_stopping(context):
                    return False

                # 等待上船
                if sleep_count >= 4:
                    Prompt.log("你上来啊！")
                    time.sleep(2)
                    sleep_count = 1
                else:
                    sleep_count += 1

                # 延时等待
                if len(coordinate) > 2:
                    Prompt.log("你上来啊！")
                    time.sleep(coordinate[2])

                # 发船
                Prompt.log(f"发船：{coordinate}")
                target = matrix.get_point(coordinate[0], coordinate[1])
                Tasker.get_controller(context).post_click(*target)
                time.sleep(1)

            Prompt.log("发船结束")
            return True
        except Exception as e:
            return Prompt.error("自动驾驶", e)


# 自动炒菜
type_num = 1
current_type = 1

zh_food_types = ["主菜", "主食", "甜品"]
en_food_types = ["entree", "carbs", "dessert"]


# 初始化
@AgentServer.custom_action("init_cook")
class InitCook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global type_num, current_type
        try:
            reco_helper = RecoHelperOld(context)
            reco_helper.recognize("自动炒菜_检测品类数量")
            type_num = 3
            if reco_helper.hit():
                results = reco_helper.reco.filterd_results
                type_num = 3 - len(results)

            num_tip = f"> 检测到菜品种类：{type_num}种（主菜"
            if type_num >= 2:
                num_tip += "、主食"
            if type_num >= 3:
                num_tip += "、甜品"
            num_tip += "）"
            print(num_tip)

            current_type = 1
            return True
        except Exception as e:
            return Prompt.error("初始化自动炒菜", e)


# 点击位置
@AgentServer.custom_action("auto_cook")
class AutoCook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global type_num, current_type, en_food_types, zh_food_types
        try:
            # 识别采购单
            reco_helper = RecoHelperOld(context)
            reco_helper.recognize("自动炒菜_识别采购单")
            if reco_helper.hit():
                print("> 尝试使用采购单")
                context.run_task("自动炒菜_使用")

            # 菜品名称
            if current_type > 3:
                return Prompt.error("未知的菜品！", use_defult_postfix=False)
            zh_name = zh_food_types[current_type - 1]
            en_name = en_food_types[current_type - 1]

            if Tasker.is_stopping(context):
                return False

            # 检测最高需求
            biggest_dish = {1: 0, 2: 0}
            dish_need_num = {1: 0, 2: 0}
            for i in range(1, 3):
                for j in range(1, 6):
                    if Tasker.is_stopping(context):
                        return False
                    reco_helper = reco_demand(context, en_name, i, j)
                    if reco_helper.hit():
                        biggest_dish[i] = j
                        dish_need_num[i] += len(reco_helper.reco.filterd_results)
            max_biggest_dish = max(biggest_dish[1], biggest_dish[2])
            print(f"> 当前最高{zh_name}需求：{max_biggest_dish}级")
            print(f"> 当前总{zh_name}需求量：{dish_need_num[1]+dish_need_num[2]}份")

            if max_biggest_dish == 0:
                print("> 无当前菜品需求，跳过当前菜品")
                change_dish()
                return True
            serve_num = round(max_biggest_dish * 1.5)

            # 检测最高菜品
            count = 0
            for i in range(1, 3):
                if biggest_dish[i] == 0:
                    count += 1
                    continue
                elif dish_need_num[i] >= 2:
                    continue
                reco_helper = reco_dish(context, en_name, i, biggest_dish[i])
                if reco_helper.hit():
                    count += 1

            if Tasker.is_stopping(context):
                return False

            if count == 2:
                print("> 已满足当前菜品需求，跳过当前菜品")
                change_dish()
                return True

            # 烹饪
            print("> 正在烹饪：" + zh_name)
            for i in range(serve_num):
                if Tasker.is_stopping(context):
                    return False
                Tasker.get_controller(context).post_click(
                    130, 330 + 140 * (current_type - 1)
                ).wait()
                if is_cook_end(context):
                    return False
                time.sleep(0.4)

            # 直接提交
            if serve_dish(context):
                return False

            # 过滤低等级菜品
            target_dish = {1: 5, 2: 5}
            for i in range(1, 3):
                if biggest_dish[i] > 2:
                    target_dish[i] = biggest_dish[i]

            # 合成菜品
            for i in range(1, 3):
                for j in range(1, target_dish[i]):
                    is_synthesis = False
                    reco_times = 0
                    while reco_times < serve_num:
                        if Tasker.is_stopping(context):
                            return False
                        # 检测是否有此菜品
                        reco_helper = reco_dish(context, en_name, i, j)
                        reco = reco_helper.reco
                        if not reco:
                            break
                        results = reco.all_results
                        results = RecoHelperOld.filter_reco(results, 0.91)
                        if len(results) < 2:
                            break

                        # 合成
                        print(f"> oi，拼好饭！({zh_name}{i}-{j+1})")
                        results = RecoHelperOld.sort_reco(results)
                        target_1 = reco_helper.get_reco_center(results[0])
                        target_2 = reco_helper.get_reco_center(results[1])
                        Tasker.get_controller(context).post_swipe(
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
                        time.sleep(0.2)
                        if serve_dish(context):
                            return False

            # 过剩菜品
            for i in range(1, 3):
                for j in range(max(biggest_dish[i] + 1, 4), 6):
                    if Tasker.is_stopping(context):
                        return False
                    reco_helper = reco_dish(context, en_name, i, j)
                    if not reco_helper.hit():
                        continue
                    results = RecoHelperOld.filter_reco(
                        reco_helper.reco.all_results, 0.91
                    )
                    if len(results) > 0:
                        print(f"> 回收过剩{zh_name}：{i}-{j}")
                        recycle_food(context, results)

            # 换菜
            change_dish()
            return True
        except Exception as e:
            return Prompt.error("自动炒菜", e)


# 换菜
def change_dish():
    global current_type, type_num
    current_type += 1
    if current_type > type_num:
        current_type = 1


# 识别菜品
def reco_dish(context: Context, en_name, i, j):
    dish_template = f"activity/{en_name}/{i}{j}.png"
    checked_dish_template = f"activity/{en_name}/{i}{j}c.png"
    reco_helper = RecoHelperOld(context)
    reco_helper.recognize(
        "自动炒菜_识别菜品",
        {"template": [dish_template, checked_dish_template]},
    )
    return reco_helper


# 识别需求
def reco_demand(context: Context, en_name, i, j):
    dish_template = f"activity/{en_name}/{i}{j}d.png"
    reco_helper = RecoHelperOld(context)
    reco_helper.recognize(
        "自动炒菜_识别需求",
        {"template": dish_template},
    )
    return reco_helper


# 上菜
def serve_dish(context: Context):
    while True:
        if Tasker.is_stopping(context):
            return True

        # 识别是否可提交
        reco_helper = RecoHelperOld(context)
        reco_helper.recognize("自动炒菜_提交菜品")
        if reco_helper.reco is None:
            break

        # 提交菜品
        print("> 豪赤！")
        target = reco_helper.get_target()
        Tasker.get_controller(context).post_click(target[0], target[1]).wait()
        time.sleep(2)

        # 检测是否完成
        reco_helper = RecoHelperOld(context)
        reco_helper.recognize("自动炒菜_挑战完成")
        if reco_helper.reco is not None:
            return True

    return False


# 回收菜品
def recycle_food(context: Context, results: list):
    context.run_task("自动炒菜_半盖")
    for res in results:
        target = RecoHelperOld.get_reco_center(res)
        Tasker.get_controller(context).post_click(target[0], target[1]).wait()
        time.sleep(0.2)
        context.run_task("自动炒菜_回收")


# 检查结束
def is_cook_end(context: Context):
    global en_food_types
    reco_helper = RecoHelperOld(context)
    reco_helper.recognize("自动炒菜_材料数量不足")
    if not reco_helper.hit():
        return False

    # 识别剩余菜品
    print("> 已无剩余材料")
    templates = []
    for food_type in en_food_types:
        for i in range(1, 3):
            for j in range(1, 6):
                templates.append(f"activity/{food_type}/{i}{j}.png")
    reco_helper = RecoHelperOld(context)
    reco_helper.recognize(
        "自动炒菜_识别菜品", {"template": templates, "roi": [292, 278, 917, 340]}
    )
    results = reco_helper.reco.all_results
    results = RecoHelperOld.filter_reco(results, 0.91)
    if len(results) < 3:
        return True

    # 清仓
    print("> 回收菜品")
    recycle_food(context, results)
    return False
