# face-swap

> 换脸程序

## 以本地程序直接运行

### 准备

由于后面需要安装 `python dlib` 包，所以需要先确定 `CMake` 已经安装：

#### Ubuntu 

```bash
sudo apt update
sudo apt install cmake
```

#### Mac OSX

```bash
brew install cmake
```

### 安装
```bash
git clone https://github.com/JeffTrain/face-swap
cd face-swap
pip install -r requirements.txt
```

### 使用
```bash
python face_swap.py ted_cruz.jpg donald_trump.jpg
```

### 测试
```bash
sh test.sh
```

### 效果
以上示例命令会把特德·克鲁斯的脸部换到唐纳德·特朗普的照片上。

|源照片|目标照片|结果照片|
|-----:|-------:|-------:|
|![特德·克鲁斯](./ted_cruz.jpg)|![唐纳德·特朗普](./donald_trump.jpg)|![结果照片](./result.jpg)|
|![65680534-b7c82780-e089-11e9-8079-f926cbe05eff](./tests/65680534-b7c82780-e089-11e9-8079-f926cbe05eff/65680534-b7c82780-e089-11e9-8079-f926cbe05eff.jpeg)|![唐纳德·特朗普](./donald_trump.jpg)|![结果照片](./tests/65680534-b7c82780-e089-11e9-8079-f926cbe05eff/result.jpg)|


### 测试矩阵

|环境|Python 版本|结果|
|---:|---:|---:|
|Windows|2.7|通过|
|Windows WSL|2.7|通过|
 |Mac OSX | 3.9.12 | 通过 |

### 以线上服务形式运行

#### 线上服务（提交代码后自动部署）

- Okteto: https://face-swap-jeff-tian.cloud.okteto.net/apidocs
- Napptive: https://face-swap-cctsq03nniljeo1bj0ng.apps.playground.napptive.dev/apidocs

#### 本地运行服务

```shell
. venv/bin/activate

pip install -r requirements.txt
python -m flask --app hello run
open http://localhost:5000/apidocs
```

#### docker 方式运行

```shell
docker build --tag face-swap .
docker run -d -p 5001:5000 face-swap
open http://localhost:5001/apidocs/
```