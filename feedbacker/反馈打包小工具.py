# pyinstaller --onefile --icon=./feedbacker.ico 反馈打包小工具.py

import os
import zipfile
import sys
from datetime import datetime, timedelta
import re
from tqdm import tqdm


version = "v1.3"


def filter_recent_logs_optimized(input_file, output_file="", days=2, max_len=5000000):
    if not os.path.exists(input_file):
        return

    print(f"> 正在精简文件 {input_file}")
    # 获取昨日日期
    now = datetime.now()
    cutoff_date = (now - timedelta(days=days - 1)).date()
    date_pattern = re.compile(r"^\[(\d{4}-\d{2}-\d{2}) ")

    found_cutoff = False
    line_count = 0
    kept_line_count = 0
    buffer = []

    # 如果输入和输出文件相同，使用临时文件
    if output_file == "":
        output_file = input_file
    temp_output = output_file
    if input_file == output_file:
        temp_output = output_file + ".temp"

    try:
        # 首先计算总行数
        with open(input_file, "r", encoding="utf-8", errors="replace") as f:
            total_lines = sum(1 for _ in f)

        with open(input_file, "r", encoding="utf-8", errors="replace") as infile:
            # 创建进度条
            pbar = tqdm(total=total_lines, desc="> 处理进度", unit="行")

            for line in infile:
                line_count += 1
                pbar.update(1)

                # 找到截止日期
                if found_cutoff:
                    buffer.append(line)
                    kept_line_count += 1
                    continue

                # 尝试匹配日期
                match = date_pattern.match(line)
                if match:
                    log_date_str = match.group(1)
                    try:
                        # 检查是否达到或超过截止日期
                        log_date = datetime.strptime(log_date_str, "%Y-%m-%d").date()
                        if log_date >= cutoff_date:
                            found_cutoff = True
                            buffer.append(line)
                            kept_line_count += 1
                    except ValueError:
                        # 无日期
                        pass

            pbar.close()

        # 如果行数超过限制，只保留最后几行
        if kept_line_count > max_len:
            buffer = buffer[-max_len:]
            kept_line_count = max_len

        # 写入文件
        with open(temp_output, "w", encoding="utf-8") as outfile:
            outfile.writelines(buffer)

        # 获取文件大小
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(temp_output)

        # 如果使用了临时文件，将其重命名为目标文件
        if input_file == output_file:
            os.replace(temp_output, output_file)

        print(
            f"> 处理完成，原文件大小: {input_size/1024/1024:.1f}MB，处理后大小: {output_size/1024/1024:.1f}MB"
        )

    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        # 如果出错，确保清理临时文件
        if input_file == output_file and os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except:
                pass
        return


class ZipPacker:
    def __init__(self):
        self.log_content = []
        self.script_dir = self.get_base_dir()
        self.log_file = os.path.join(self.script_dir, "feedbacker.log")

    def get_base_dir(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def log(self, message):
        message = "> " + message
        self.log_content.append(message)
        print(message)

    def create_zip(self, output_filename, source_paths):
        # 确保输出文件名以.zip结尾
        if not output_filename.lower().endswith(".zip"):
            output_filename += ".zip"

        output_path = os.path.join(self.script_dir, output_filename)

        # 检查输出文件是否已存在
        if os.path.exists(output_path):
            self.log(f"输出文件 {output_filename} 已存在，将被覆盖")

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 添加所有源文件/文件夹
            for source in source_paths:
                # 转换为绝对路径
                abs_source = os.path.abspath(os.path.join(self.script_dir, source))

                if not os.path.exists(abs_source):
                    self.log(f"文件 {source} 不存在，将跳过此日志")
                    continue

                self.log(f"添加日志: {source}")

                if os.path.isdir(abs_source):
                    # 处理文件夹
                    for root, dirs, files in os.walk(abs_source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # 计算在ZIP中的相对路径
                            arcname = os.path.relpath(
                                file_path, os.path.join(abs_source, "..")
                            )
                            zipf.write(file_path, arcname)
                else:
                    # 处理单个文件
                    arcname = os.path.basename(abs_source)
                    zipf.write(abs_source, arcname)

            # 将日志文件添加到ZIP中
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("\n".join(self.log_content))

            zipf.write(self.log_file, os.path.basename(self.log_file))

        # 删除临时日志文件
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

        self.log(f"成功打包日志: {output_filename}")
        zip_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"日志包生成时间: {zip_time}")
        self.log(f"保存路径: {output_path}")


def zip():
    global version

    packer = ZipPacker()
    output_filename = f"反馈日志.zip"
    source_paths = [
        "debug/maa.log",
        f"logs/log-{datetime.now().strftime('%Y%m%d')}.txt",
        f"logs/log-{(datetime.now() - timedelta(days=1)).strftime('%Y%m%d')}.txt",
        "config",
    ]

    try:
        packer.log(f"打包器版本: {version}")
        packer.create_zip(output_filename, source_paths)
    except Exception as e:
        packer.log(f"打包工具执行异常: {str(e)}")
        input("按任意键退出...")
        sys.exit(0)


if __name__ == "__main__":
    print(f"反馈打包小工具 - {version}")
    input("请在关闭 MNMA 后，按任意键执行打包操作...")
    print("> 即将打包日志，请等待提示后再关闭此窗口")
    filter_recent_logs_optimized("debug/maa.log")
    zip()
    print(
        "日志打包脚本执行完毕，请将目录下 反馈日志.zip 发送至交流群并@群主，同时描述错误内容并提交截图或录屏，或将以上信息提交至issue"
    )
    input("按任意键退出...")
    sys.exit(0)
