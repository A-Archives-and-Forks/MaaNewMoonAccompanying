from pathlib import Path
from pypinyin import lazy_pinyin
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

working_dir = Path(__file__).parent.parent
resource_path = working_dir / "assets" / "resource"
pipeline_paths = [
    (file / "pipeline") for file in resource_path.iterdir() if file.is_dir()
]


def encode_dir(dir):
    count = 1
    for file in dir.iterdir():
        if file.is_dir():
            encode_dir(file)
        try:
            new_name = f"{count:02d}_{''.join(lazy_pinyin(file.name))}"
            file.rename(file.with_name(new_name))
            print(f"{file.name} -> {new_name}", flush=True)
            count += 1
        except Exception as e:
            print(f"处理文件 {file.name} 时出错: {e}", flush=True)


if __name__ == "__main__":
    for pipeline_path in pipeline_paths:
        encode_dir(pipeline_path)
