# pyinstaller --onefile --icon=./feedbacker.ico 反馈打包小工具.py

import os
import zipfile
import sys
import datetime


version = "1.1.0"


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
        zip_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"日志包生成时间: {zip_time}")
        self.log(f"保存路径: {output_path}")


def main():
    global version

    packer = ZipPacker()
    output_filename = f"反馈日志.zip"
    source_paths = [
        "debug/maa.log",
        f"logs/log-{datetime.datetime.now().date()}.txt",
        f"logs/log-{datetime.datetime.now().date() - datetime.timedelta(days=1)}.txt",
        "config",
    ]

    try:
        packer.log(f"小工具版本: {version}")
        packer.create_zip(output_filename, source_paths)
    except Exception as e:
        packer.log(f"打包工具执行异常: {str(e)}")
        input("按任意键退出...")
        sys.exit(0)


if __name__ == "__main__":
    print("即将运行日志打包脚本，请等待提示后再关闭此窗口...")
    main()
    print(
        "日志打包脚本执行完毕，请将目录下 反馈日志.zip 发送至交流群并@群主，同时描述错误内容并提交截图或录屏，或将以上信息提交至issue"
    )
    input("按任意键退出...")
    sys.exit(0)
