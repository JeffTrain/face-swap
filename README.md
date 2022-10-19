# face-swap

> 换脸程序

## 准备

由于后面需要安装 `python dlib` 包，所以需要先确定 `CMake` 已经安装：

### Ubuntu 

```bash
sudo apt update
sudo apt install cmake
```

### Mac OSX

```bash
brew install cmake
```

## 安装
```bash
git clone https://github.com/JeffTrain/face-swap
cd face-swap
pip install -r requirements.txt
```

## 使用
```bash
python face-swap.py ted_cruz.jpg donald_trump.jpg
```

## 测试
```bash
sh test.sh
```

## 效果
以上示例命令会把特德·克鲁斯的脸部换到唐纳德·特朗普的照片上。

|源照片|目标照片|结果照片|
|-----:|-------:|-------:|
|![特德·克鲁斯](./ted_cruz.jpg)|![唐纳德·特朗普](./donald_trump.jpg)|![结果照片](./result.jpg)|
|![65680534-b7c82780-e089-11e9-8079-f926cbe05eff](./tests/65680534-b7c82780-e089-11e9-8079-f926cbe05eff/65680534-b7c82780-e089-11e9-8079-f926cbe05eff.jpeg)|![唐纳德·特朗普](./donald_trump.jpg)|![结果照片](./tests/65680534-b7c82780-e089-11e9-8079-f926cbe05eff/result.jpg)|


## 测试矩阵

|环境|Python 版本|结果|
|---:|---:|---:|
|Windows|2.7|通过|
|Windows WSL|2.7|通过|

