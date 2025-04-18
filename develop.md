# 开发方式

## 调试

``` shell
explorer "D:\_Producers\ImageCropper"
python -m MaaDebugger
```

## 构建程序

``` shell
python ./install_and_run.py
python ./build.py
```

## 发布

``` shell
git pull github main
git push --set-upstream github main

git add .
git commit -m "Update:v0.3.0"
git push github main

git tag -a v0.3.0 -m "Release v0.3.0"
git push github v0.3.0
```
