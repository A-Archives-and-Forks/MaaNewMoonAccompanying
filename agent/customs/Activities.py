from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt, RecoHelper, get_controller


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
            args = parse_query_args(argv)
            num = args.get("type_num", "1")
            type_num = int(num)

            num_tip = f"> 菜品种类：{num}种（主菜"
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
            reco_helper = RecoHelper(context)
            reco_helper.recognize("自动炒菜_识别采购单")
            if reco_helper.hit():
                print("> 尝试使用采购单")
                context.run_task("自动炒菜_使用")

            # 菜品名称
            if current_type > 3:
                return Prompt.error("未知的菜品！", use_defult_postfix=False)
            zh_name = zh_food_types[current_type - 1]
            en_name = en_food_types[current_type - 1]

            # 检测最高需求
            biggest_dish = {1: 0, 2: 0}
            for i in range(1, 3):
                for j in range(1, 6):
                    if reco_demand(context, en_name, i, j).hit():
                        biggest_dish[i] = j
            max_biggest_dish = max(biggest_dish[1], biggest_dish[2])
            print(f"> 当前最高{zh_name}需求：{max_biggest_dish}级")

            if max_biggest_dish == 0:
                print("> 无当前菜品需求，跳过当前菜品")
                change_dish()
                return True

            # 检测最高菜品
            count = 0
            for i in range(1, 3):
                if biggest_dish[i] == 0:
                    count += 1
                    continue
                reco_helper = reco_dish(context, en_name, i, biggest_dish[i])
                if reco_helper.hit():
                    count += 1
            if count == 2:
                print("> 已满足当前菜品需求，跳过当前菜品")
                change_dish()
                return True

            # 烹饪
            print("> 正在烹饪：" + zh_name)
            for i in range(round(max_biggest_dish * 1.5)):
                get_controller(context).post_click(
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
                    while reco_times < 5:
                        # 检测是否有此菜品
                        reco_helper = reco_dish(context, en_name, i, j)
                        reco = reco_helper.reco
                        if not reco:
                            break
                        results = reco.all_results
                        results = RecoHelper.filter_reco(results, 0.91)
                        if len(results) < 2:
                            break

                        # 合成
                        print(f"> oi，拼好饭！({zh_name}{i}-{j+1})")
                        results = RecoHelper.sort_reco(results)
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
                        time.sleep(0.2)
                        if serve_dish(context):
                            return False

            # 过剩菜品
            for i in range(1, 3):
                if biggest_dish[i] >= 4:
                    continue
                for j in range(4, 6):
                    reco_helper = reco_dish(context, en_name, i, j)
                    if not reco_helper.hit():
                        continue
                    results = RecoHelper.filter_reco(reco_helper.reco.all_results, 0.91)
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
    reco_helper = RecoHelper(context)
    reco_helper.recognize(
        "自动炒菜_识别菜品",
        {"template": [dish_template, checked_dish_template]},
    )
    return reco_helper


# 识别需求
def reco_demand(context: Context, en_name, i, j):
    dish_template = f"activity/{en_name}/{i}{j}d.png"
    reco_helper = RecoHelper(context)
    reco_helper.recognize(
        "自动炒菜_识别需求",
        {"template": dish_template},
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
        print("> 豪赤！")
        target = reco_helper.get_target()
        get_controller(context).post_click(target[0], target[1]).wait()
        time.sleep(2)

        # 检测是否完成
        reco_helper = RecoHelper(context)
        reco_helper.recognize("自动炒菜_挑战完成")
        if reco_helper.reco is not None:
            return True

    return False


# 回收菜品
def recycle_food(context: Context, results: list):
    context.run_task("自动炒菜_半盖")
    for res in results:
        target = RecoHelper.get_reco_center(res)
        get_controller(context).post_click(target[0], target[1]).wait()
        time.sleep(0.2)
        context.run_task("自动炒菜_回收")


# 检查结束
def is_cook_end(context: Context):
    global en_food_types
    reco_helper = RecoHelper(context)
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
    reco_helper = RecoHelper(context)
    reco_helper.recognize(
        "自动炒菜_识别菜品", {"template": templates, "roi": [292, 278, 917, 340]}
    )
    results = reco_helper.reco.all_results
    results = RecoHelper.filter_reco(results, 0.91)
    if len(results) < 3:
        return True

    # 清仓
    print("> 回收菜品")
    recycle_food(context, results)
    return False
