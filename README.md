# 簡単音量可視化ツール

実行ファイルと同階層に visualizer_config.yaml を置き、設定を変更するとボリュームのしきい値やインデックスが変更出来る。

mic_index 1 は既定のデバイスなので、既定のデバイス以外が必要がなければ変更しなくて良い

数字をボリュームバーの左、及び下に配置するかは、 layout プロパティを vertical または horizontal を指定する
```
alert: 80
warning: 70
layout: "horizontal"
# layout: "vertical"

mic_index: 1
```

mic_index を変更する際は、 [オーディオデバイスリスト化ツール](./bin/list_audio.exe)を使用することで、インデックスと名前が分かります。

## 操作方法
Ctrl + x で最大値をリセット出来ます。

### 開発メモ
実行ファイル化
```
pyinstaller .\main.py --name simple_volume_visualizer.exe --onefile --noconsole
pyinstaller .\list_audio.py --name list_audio.exe --onefile --noconsole
```
