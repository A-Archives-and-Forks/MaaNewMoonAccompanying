import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, run_cmd):
        self.run_cmd = run_cmd
        self.process = None
        self.restart()

    def restart(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("正在启动进程：", " ".join(self.run_cmd))
        self.process = subprocess.Popen(self.run_cmd)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} 发生变动，重启进程...")
            self.restart()

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} 新建，重启进程...")
            self.restart()

    def on_deleted(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} 被删除，重启进程...")
            self.restart()


if __name__ == "__main__":
    path = "agent"
    cmd = [sys.executable, "agent/dev_main.py"]
    event_handler = RestartOnChangeHandler(cmd)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if event_handler.process:
        event_handler.process.terminate()
