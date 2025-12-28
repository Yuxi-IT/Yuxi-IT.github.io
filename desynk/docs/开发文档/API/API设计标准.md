## API接口设计标准
- API接口分为两种`未登录请求`和`登录请求`。
  - `未登录请求`是开放API，主要用于主页展示信息，无请求字段限制
  - `登录请求` 需要携带用于身份校验的Token和其他需要证明身份的字段才能正常请求
- 以下是一个`登录请求`的接口例子
```http
POST /api/getOrder
Authorization: Berear XXXXXXXXXXXXXXXXXXXXX //临时Token
Signature: (请求体和时间戳通过DesynkHash计算得出的签名)
Timestamp: 10位秒级时间戳(UTC+8)
{
    "Count":10,
    "Tech":["React", "C#", "Java", "C++"],
    "Timestamp": 13位时间戳(实际并不以这里为准，而是请求头中的时间戳)
}
```