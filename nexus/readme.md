# JSON 规则配置文档

## 概述

本文档描述了一个用于网页自动化操作的 JSON 规则配置格式。该配置可用于定义点击操作和数据抓取规则，支持重试机制和精确元素定位。

## 基本结构

```json
{
  "click": [],
  "selectors": [],
  "lists": []
}
```

## 1. 点击规则 (`click`)

定义需要执行的点击操作序列。

### 单个点击规则结构

```json
{
  "query": "CSS选择器",
  "index": "可选，元素索引（从0开始）",
  "delay": "可选，点击后等待时间（毫秒）",
  "retry": "可选，最大重试次数"
}
```

### 示例

```json
{
  "click": [
    {
      "query": ".buttonOver18",
      "index": 1,
      "delay": 3000,
      "retry": 5
    }
  ]
}
```

### 字段说明

| 字段    | 类型   | 必填 | 默认值 | 描述                                                                 |
|---------|--------|------|--------|----------------------------------------------------------------------|
| query   | string | 是   | -      | CSS选择器，用于定位元素                                              |
| index   | number | 否   | 0      | 当有多个匹配元素时，指定要操作的元素索引（从0开始）                 |
| delay   | number | 否   | 1000   | 点击后等待的时间（毫秒）                                            |
| retry   | number | 否   | 1      | 操作失败时的最大重试次数                                            |

## 2. 数据抓取规则 (`lists`)

定义需要抓取的数据列表及其字段。

### 单个列表规则结构

```json
{
  "query": "CSS选择器",
  "items": [
    {
      "query": "CSS选择器",
      "attr": "属性类型",
      "label": "字段名称"
    }
  ]
}
```

### 示例

```json
{
  "lists": [
    {
      "query": "ul#singleFeedSection li.pcVideoListItem",
      "items": [
        {
          "query": "a.latestThumb.js-linkVideoThumb",
          "attr": "href",
          "label": "视频打开链接"
        },
        {
          "query": "a.thumbnailTitle",
          "attr": "text",
          "label": "视频标题"
        }
      ]
    }
  ]
}
```

### 字段说明

#### 列表级字段

| 字段  | 类型   | 必填 | 描述                          |
|-------|--------|------|-------------------------------|
| query | string | 是   | 列表项的CSS选择器             |
| items | array  | 是   | 要抓取的字段定义数组          |

#### 字段级字段

| 字段  | 类型   | 必填 | 默认值 | 描述                                                                 |
|-------|--------|------|--------|----------------------------------------------------------------------|
| query | string | 是   | -      | 字段元素的CSS选择器（相对于列表项）                                  |
| attr  | string | 是   | -      | 要获取的属性类型：`text`、`html`、`outerHTML` 或任意HTML属性名      |
| label | string | 是   | -      | 字段名称，将作为结果对象的键名                                       |

## 3. 选择器规则 (`selectors`)

（保留字段，当前版本未实现具体功能）

## 完整示例

```json
{
  "click": [
    {
      "query": ".buttonOver18",
      "index": 1,
      "delay": 3000,
      "retry": 5
    }
  ],
  "selectors": [],
  "lists": [
    {
      "query": "ul#singleFeedSection li.pcVideoListItem",
      "items": [
        {
          "query": "a.latestThumb.js-linkVideoThumb",
          "attr": "href",
          "label": "视频打开链接"
        },
        {
          "query": "a.thumbnailTitle",
          "attr": "text",
          "label": "视频标题"
        },
        {
          "query": "a.latestThumb.js-linkVideoThumb img",
          "attr": "src",
          "label": "图片地址"
        },
        {
          "query": ".videoUploaderBlock .usernameWrap a",
          "attr": "text",
          "label": "视频发布者"
        },
        {
          "query": ".videoDetailBlock .views var",
          "attr": "text",
          "label": "观看次数"
        },
        {
          "query": ".marker-overlays var.bgShadeEffect.duration",
          "attr": "text",
          "label": "视频时长"
        }
      ]
    }
  ]
}
```

## 执行流程

1. **点击阶段**：
   - 按顺序执行所有点击规则
   - 每个点击操作会尝试找到匹配元素
   - 如果失败，会按指定的重试次数进行重试
   - 每次点击后有指定的延迟时间

2. **数据抓取阶段**：
   - 对每个列表规则，查找所有匹配的列表项
   - 对每个列表项，提取所有定义的字段
   - 返回结构化数据

## 结果格式

执行后返回的数据格式示例：

```json
[
  {
    "视频打开链接": "https://example.com/video1",
    "视频标题": "示例视频1",
    "图片地址": "https://example.com/thumb1.jpg",
    "视频发布者": "用户A",
    "观看次数": "1,234",
    "视频时长": "05:30"
  },
  {
    "视频打开链接": "https://example.com/video2",
    "视频标题": "示例视频2",
    "图片地址": "https://example.com/thumb2.jpg",
    "视频发布者": "用户B",
    "观看次数": "5,678",
    "视频时长": "10:15"
  }
]
```

## 最佳实践

1. **选择器编写**：
   - 尽量使用唯一的CSS选择器
   - 避免使用过于复杂的选择器
   - 优先使用class和id组合

2. **点击操作**：
   - 为关键操作设置足够的延迟时间
   - 对重要操作设置重试机制
   - 使用index精确指定要操作的元素

3. **错误处理**：
   - 在规则中设置合理的重试次数
   - 监控执行日志，优化不稳定选择器

## 注意事项

1. 所有CSS选择器都是相对于当前文档的
2. 索引从0开始计算
3. 延迟时间单位为毫秒
4. 如果元素不存在，对应字段值将为null
5. 确保规则与目标网页结构匹配
