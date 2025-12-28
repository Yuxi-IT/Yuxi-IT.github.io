## 标准API层级

- 该项目所有API接口返回的值都遵循以下JSON标准: 

其中
```Result```为布尔值，表示执行操作是否成功;
```Message```为字符串;
```Data```为可为null泛型。
```json
{
    "Result": true,
    "Message": "Successful",
    "Data": T
}
```
