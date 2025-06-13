# pyinstaller --onefile --icon=./gc.ico 安全清理小工具.py

import os
import shutil
import sys
from pathlib import Path

version = "1.0"


def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


def clean_directories():
    directories_to_clean = ["./debug", "./logs"]
    total_cleaned_size = 0

    for dir_path in directories_to_clean:
        path = Path(dir_path)
        if path.exists():
            try:
                if path.is_dir():
                    # 在删除前计算目录大小
                    dir_size = get_directory_size(path)
                    total_cleaned_size += dir_size
                    shutil.rmtree(path)
                    print(f"> 清理目录: {dir_path}")
                else:
                    # 如果是文件，直接获取文件大小
                    file_size = path.stat().st_size
                    total_cleaned_size += file_size
                    path.unlink()
                    print(f"> 清理文件: {dir_path}")
            except Exception as e:
                print(f"> 清理 {dir_path} 时出错: {str(e)}")
        else:
            print(f"{dir_path}不存在，跳过操作")

    cleaned_size_mb = round(total_cleaned_size / (1024 * 1024), 1)
    print(f"> 清理完成，共清理了 {cleaned_size_mb} MB 的文件！")


if __name__ == "__main__":
    print(f"安全清理小工具 - v{version}")
    print(
        "此功能不影响配置、adb记忆等，仅清理日志文件，若您需要保留日志请关闭此窗口。"
    )
    input("请在关闭 MNMA 后，按任意键执行清理操作...")
    print("> 开始清理...")
    clean_directories()
    input("> 按任意键退出...")
    sys.exit()
