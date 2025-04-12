# 开发方式

## 调试

``` shell
explorer "D:\_Producers\ImageCropper"
python -m MaaDebugger
```

## 构建程序

``` shell
python ./install.py
python ./build.py
```

## 发布

``` shell
git pull github main
git push --set-upstream github main

git add .
git commit -m "Fix:公告图片加载异常"
git push github main

git tag v0.2.0
git push github v0.2.0
```
