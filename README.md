# GPT-SoVITS-Novel-Reader
GPT-SoVITS小说批量转换脚本

## 使用方法
1. 启动api_v2.py(官方文档有说明)
2. 修改对应参数
```
novel: 小说路径
url: api地址
payload: 同官方文档的参数，ref_audio_path为选择的音频路径
```
3. 修改`第(\w+)部`和`第(\w+)章`部分

例如你的小说文本中有`第xxx部`，`第xxx章`，则音频会被输出到`第xxx部/第xxx章.wav`

如果你的小说是`第xxx章`，`第xxx节`，只需修改正则对应的部分就行

如果你的小说只有类似于`第xxx章`的标记，那么在第一行加上`第xxx节`即可

4. 安装依赖库
```
pip install pydub
```

5. 运行脚本
