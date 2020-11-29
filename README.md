# imgstorage

画像を色々なサイズに自動で変換して、保管するPythonのツールです。

## 使用方法
### 1. 保管ディレクトリ作成
事前にディレクトリ構造は作成しておく必要があります。
画像を保管するためのディレクトリを適当に作成します。

```bash
# 事前準備
mkdir -p /srv/storage/images/{thum,small,medium,org}
```

### 2. 画像の格納

```python
from imgstorage import storage, imgfilter

# ImgStoreオブジェクト作成
s = imgstorage.storage.ImgStore('/srv/storage/images')

# 画像保存設定
s.add_config('thum', imgfilter.Crop(1.0) + imgfilter.Resize(256, 256))
s.add_config('small', imgfilter.Shrink(1600, 1600))
s.add_config('medium', imgfilter.Shrink(2400, 2400))
s.add_config('org', imgfilter.Null())

# 画像を登録 (-> 各ディレクトリ配下に格納されます)
s.push('./sample.jpg')

```
