# wxcloudrun-flask
[![GitHub license](https://img.shields.io/github/license/WeixinCloud/wxcloudrun-express)](https://github.com/WeixinCloud/wxcloudrun-express)
![GitHub package.json dependency version (prod)](https://img.shields.io/badge/python-3.7.3-green)

微信云托管 python Flask 框架模版，实现简单的计数器读写接口，使用云托管 MySQL 读写、记录计数值。

![](https://qcloudimg.tencent-cloud.cn/raw/be22992d297d1b9a1a5365e606276781.png)


## 快速开始
前往 [微信云托管快速开始页面](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/basic/guide.html)，选择相应语言的模板，根据引导完成部署。

## 本地调试
下载代码在本地调试，请参考[微信云托管本地调试指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/guide/debug/)

## 实时开发
代码变动时，不需要重新构建和启动容器，即可查看变动后的效果。请参考[微信云托管实时开发指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/guide/debug/dev.html)

## Docker 运行

### 构建镜像

```bash
docker build -t quantalent-wxcloud .
```

### 运行容器

#### 基本用法（端口映射）

```bash
# 将主机 8080 端口映射到容器 80 端口（默认配置）
docker run -d -p 8080:80 --name my-app quantalent-wxcloud

# 指定主机 IP，仅允许本地访问
docker run -d -p 127.0.0.1:8080:80 --name my-app quantalent-wxcloud
```

#### 自定义容器内监听地址和端口

如果需要改变容器内应用监听的地址和端口，可以覆盖启动命令：

```bash
# 容器内监听 0.0.0.0:3000，主机映射到 8080
docker run -d -p 8080:3000 --name my-app quantalent-wxcloud python3 run.py 0.0.0.0 3000

# 容器内监听 127.0.0.1:5000，主机映射到 5000
docker run -d -p 5000:5000 --name my-app quantalent-wxcloud python3 run.py 127.0.0.1 5000
```

#### 常用参数

- `-p <主机端口>:<容器端口>` - 端口映射
- `-p <主机IP>:<主机端口>:<容器端口>` - 指定主机 IP 的端口映射
- `-d` - 后台运行
- `--name <容器名>` - 指定容器名称
- `--rm` - 容器停止后自动删除

**说明**：容器默认监听 `0.0.0.0:80`（见 Dockerfile），通常只需使用 `-p` 进行端口映射即可。

## Dockerfile最佳实践
请参考[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)

## 目录结构说明

~~~
.
├── Dockerfile dockerfile       dockerfile
├── README.md README.md         README.md文件
├── container.config.json       模板部署「服务设置」初始化配置（二开请忽略）
├── requirements.txt            依赖包文件
├── config.py                   项目的总配置文件  里面包含数据库 web应用 日志等各种配置
├── run.py                      flask项目管理文件 与项目进行交互的命令行工具集的入口
└── wxcloudrun                  app目录
    ├── __init__.py             python项目必带  模块化思想
    ├── dao.py                  数据库访问模块
    ├── model.py                数据库对应的模型
    ├── response.py             响应结构构造
    ├── templates               模版目录,包含主页index.html文件
    └── views.py                执行响应的代码所在模块  代码逻辑处理主要地点  项目大部分代码在此编写
~~~



## 服务 API 文档

### `GET /api/companies`

获取公司列表

#### 请求参数

无

#### 响应结果

- `code`：状态码 (200 表示成功)
- `message`：提示信息
- `data`：公司列表数组

**data 对象结构**:
- `id`：公司 ID
- `name`：公司名称
- `image`：公司 Logo 图片 URL
- `question_count`：该公司关联的题目数量

##### 响应结果示例

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "Jane Street",
      "image": "https://example.com/janestreet.png",
      "question_count": 100
    }
  ]
}
```

#### 调用示例

```bash
curl https://<云托管服务域名>/api/companies
```

---

### `GET /api/questions`

获取题目列表，支持按公司、难度、标签筛选

#### 请求参数

| 参数名     | 类型   | 必填 | 说明                                                    |
| :--------- | :----- | :--- | :------------------------------------------------------ |
| company_id | Number | 是   | 公司 ID                                                 |
| difficulty | String | 否   | 难度筛选 (Easy, Medium, Hard)，不传则为全部             |
| tag        | String | 否   | 标签筛选，多个标签用逗号分隔                            |
| page       | Number | 否   | 页码，默认为 1                                          |
| page_size  | Number | 否   | 每页数量，默认为 10                                     |

#### 响应结果

- `code`：状态码 (200 表示成功)
- `message`：提示信息
- `data`：响应数据对象

**data 对象结构**:
- `list`：题目列表数组
- `total`：总题目数
- `page`：当前页码
- `page_size`：每页数量

**list 元素结构**:
- `id`：题目 ID
- `title`：题目标题
- `difficulty`：难度 (Easy, Medium, Hard)
- `tags`：标签列表

##### 响应结果示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 10,
    "list": [
      {
        "id": 101,
        "title": "Expected Number of Tosses",
        "difficulty": "Medium",
        "tags": ["Probability", "Expected Value"]
      }
    ]
  }
}
```

#### 调用示例

```bash
curl "https://<云托管服务域名>/api/questions?company_id=1&difficulty=Medium&page=1&page_size=10"
```

---

### `GET /api/question_detail`

获取题目详情

#### 请求参数

| 参数名     | 类型   | 必填 | 说明   |
| :--------- | :----- | :--- | :----- |
| question_id | Number | 是   | 题目 ID |

#### 响应结果

- `code`：状态码 (200 表示成功)
- `message`：提示信息
- `data`：题目详情对象

**data 对象结构**:
- `id`：题目 ID
- `company_name`：公司名称
- `title`：题目标题
- `level`：难度级别
- `tags`：标签列表
- `firms`：关联公司列表
- `content`：题目内容
- `solution`：解题思路
- `answer`：答案
- `hint`：提示

##### 响应结果示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 101,
    "company_name": "Jane Street",
    "title": "Expected Number of Tosses",
    "level": "Medium",
    "tags": ["Probability", "Expected Value"],
    "firms": ["Jane Street", "Citadel"],
    "content": "题目内容...",
    "solution": "解题思路...",
    "answer": "答案...",
    "hint": "提示信息..."
  }
}
```

#### 调用示例

```bash
curl "https://<云托管服务域名>/api/question_detail?question_id=101"
```

---

### `POST /api/add_questions`

添加面试题

#### 请求参数

| 参数名       | 类型   | 必填 | 说明           |
| :----------- | :----- | :--- | :------------- |
| company_name | String | 是   | 公司名称       |
| title        | String | 是   | 题目标题       |
| content      | String | 是   | 题目内容       |
| solution     | String | 是   | 解题思路       |
| answer       | String | 是   | 答案           |
| level        | String | 是   | 难度级别       |
| hint         | String | 是   | 提示           |
| tags         | String | 是   | 标签           |
| firms        | String | 是   | 关联公司列表   |

##### 请求参数示例

```json
{
  "company_name": "Jane Street",
  "title": "Expected Number of Tosses",
  "content": "题目内容...",
  "solution": "解题思路...",
  "answer": "答案...",
  "level": "Medium",
  "hint": "提示信息...",
  "tags": "Probability,Expected Value",
  "firms": "Jane Street,Citadel"
}
```

#### 响应结果

- `code`：状态码 (200 表示成功)
- `data`：新创建的题目 ID

##### 响应结果示例

```json
{
  "code": 200,
  "data": 101
}
```

#### 调用示例

```bash
curl -X POST -H 'content-type: application/json' \
  -d '{
    "company_name": "Jane Street",
    "title": "Expected Number of Tosses",
    "content": "题目内容...",
    "solution": "解题思路...",
    "answer": "答案...",
    "level": "Medium",
    "hint": "提示信息...",
    "tags": "Probability,Expected Value",
    "firms": "Jane Street,Citadel"
  }' \
  https://<云托管服务域名>/api/add_questions
```

---

### `GET /health`

健康检查端点

#### 请求参数

无

#### 响应结果

- `status`：服务状态
- `message`：提示信息

##### 响应结果示例

```json
{
  "status": "ok",
  "message": "service is running"
}
```

#### 调用示例

```bash
curl https://<云托管服务域名>/health
```

## 使用注意
如果不是通过微信云托管控制台部署模板代码，而是自行复制/下载模板代码后，手动新建一个服务并部署，需要在「服务设置」中补全以下环境变量，才可正常使用，否则会引发无法连接数据库，进而导致部署失败。
- MYSQL_ADDRESS
- MYSQL_PASSWORD
- MYSQL_USERNAME
以上三个变量的值请按实际情况填写。如果使用云托管内MySQL，可以在控制台MySQL页面获取相关信息。



## License

[MIT](./LICENSE)
