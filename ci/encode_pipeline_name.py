from pathlib import Path
from pypinyin import lazy_pinyin

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
        new_name = f"{count:02d}{file.suffix}"
        file.rename(file.with_name(new_name))
        count += 1
        print(f"{file.name} -> {new_name}")


if __name__ == "__main__":
    for pipeline_path in pipeline_paths:
        encode_dir(pipeline_path)
