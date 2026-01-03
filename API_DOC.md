# API 接口文档

本文档定义了小程序前端与后端交互的数据接口协议。

## 1. 首页接口

### 1.1 获取公司列表

- **接口地址**: `/api/companies`
- **请求方式**: `GET`
- **描述**: 获取首页展示的公司列表数据。

#### 请求参数

无

#### 响应参数

| 参数名  | 类型   | 说明                  |
| :------ | :----- | :-------------------- |
| code    | Number | 状态码 (200 表示成功) |
| message | String | 提示信息              |
| data    | Array  | 公司列表              |

**data 对象结构**:

| 参数名        | 类型   | 说明                 |
| :------------ | :----- | :------------------- |
| id            | Number | 公司 ID              |
| name          | String | 公司名称             |
| image         | String | 公司 Logo 图片 URL   |
| questionCount | Number | 该公司关联的题目数量 |

#### 示例响应

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "Jane Street",
      "image": "https://www.coachquant.com/.../janestreet.png",
      "questionCount": 100
    }
  ]
}
```

## 2. 题目列表页接口 (详情页)

### 2.1 获取题目列表

- **接口地址**: `/api/questions`
- **请求方式**: `GET`
- **描述**: 获取题目列表，支持按公司、难度、标签筛选。

#### 请求参数

| 参数名     | 类型   | 必填 | 说明                                                    |
| :--------- | :----- | :--- | :------------------------------------------------------ |
| companyId  | Number | 是   | 公司 ID                                                 |
| difficulty | String | 否   | 难度筛选 (Easy, Medium, Hard)，不传则为全部             |
| tags       | String | 否   | 标签筛选，多个标签用逗号分隔 (e.g. "Probability,Games") |
| page       | Number | 否   | 页码，默认为 1                                          |
| pageSize   | Number | 否   | 每页数量，默认为 20                                     |

#### 响应参数

| 参数名  | 类型   | 说明                  |
| :------ | :----- | :-------------------- |
| code    | Number | 状态码 (200 表示成功) |
| message | String | 提示信息              |
| data    | Object | 响应数据              |

**data 对象结构**:

| 参数名   | 类型   | 说明     |
| :------- | :----- | :------- |
| list     | Array  | 题目列表 |
| total    | Number | 总题目数 |
| page     | Number | 当前页码 |
| pageSize | Number | 每页数量 |

**list 元素结构**:

| 参数名     | 类型   | 说明                      |
| :--------- | :----- | :------------------------ |
| id         | Number | 题目 ID                   |
| title      | String | 题目标题                  |
| difficulty | String | 难度 (Easy, Medium, Hard) |
| tags       | Array  | 标签列表 (String Array)   |
| companies  | Array  | 关联公司列表 (简略信息)   |

#### 示例响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "pageSize": 20,
    "list": [
      {
        "id": 101,
        "title": "Expected Number of Tosses",
        "difficulty": "Medium",
        "tags": ["Probability", "Expected Value"],
        "companies": [
          { "id": 1, "name": "Jane Street" },
          { "id": 2, "name": "Citadel" }
        ]
      }
    ]
  }
}
```
