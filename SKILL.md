---
name: 图片解析助手
description: >
  将图片解析为结构化的文本信息，输出包含图片内容与构图、画风、色彩参数的 JSON 文件和文本 prompt。
  Parse images into structured text information, output JSON file and text prompt containing image content & composition, art style, and color grading parameters.
---

# 图片解析助手

使用此 skill 将图片解析为结构化的文本信息，输出两份内容：一份是包含图片信息的 JSON 文件，一份是文本版的 prompt。

## 触发条件

当用户同时满足以下两个条件时，自动触发此 skill：
1. **上传图片**：用户上传了一张或多张图片
2. **文字描述**：用户输入文字包含"解析图片"关键词

## 输入要求

- 图片 URL 或本地图片路径
- 用户文字描述中包含"解析图片"

## 输出内容

解析结果包含三部分：
1. **图片内容及构图**：识别图片主体、场景、动作、细节，以及构图方式、视角、景别
2. **图片画风**：识别艺术风格、画派、技法特点
3. **图片色彩参数**：使用达芬奇调色专业参数描述图片色彩

## 工作流程

### Step 1：接收图片

获取用户上传的图片（URL 或本地路径）。

### Step 2：解析图片内容及构图

识别并描述：
- **主体对象**：人物、动物、物体等画面核心元素
- **场景环境**：室内/室外、地点类型、空间特征
- **动作状态**：正在进行的动作、情感表达、人物互动
- **关键细节**：表情、服饰、道具、背景元素
- **景别**：远景、全景、中景、近景、特写
- **视角**：平视、仰视、俯视、侧视、鸟瞰、低角度
- **构图方式**：三分法、对称构图、引导线、框架构图、对角线、三角形、S形、留白等
- **画面平衡**：视觉重心、空间分布、元素排布

### Step 3：识别图片画风

分析图片的艺术风格：
- **风格类型**：写实、超写实、漫画、插画、油画、水彩、素描、水墨、3D渲染、数字艺术、波普艺术等
- **画派特征**：印象派、后印象派、超现实主义、立体主义、抽象表现主义、极简主义等
- **技术特点**：笔触风格、线条特征、光影处理、色彩运用、质感表现
- **时代特征**：古典、现代、当代、复古、未来主义等
- **氛围调性**：明亮、阴暗、温暖、冷峻、梦幻、写实、夸张、细腻、粗犷

### Step 4：提取色彩参数

使用达芬奇调色专业参数描述图片色彩：

#### 一级调色（Primary Wheels）

```
【阴影】(Shadow Wheel)
色相：0-360°（红色=0，黄色=60，绿色=120，青色=180，蓝色=240，品红=300）
饱和度：0-100%
亮度：0-100%

【中间调】(Midtones Wheel)
色相：0-360°
饱和度：0-100%
亮度：0-100%

【高光】(Highlights Wheel)
色相：0-360°
饱和度：0-100%
亮度：0-100%

【全局】(Global Wheel)
色相：0-360°
饱和度：0-100%
亮度：0-100%
```

#### 对比与曝光

```
【对比度】(Contrast)：0-100%
【曝光】(Exposure)：-5.0 至 +5.0 EV
【Gamma】：0.1 至 3.0
【增益】(Gain)：0-100%
【偏移】(Offset)：-100 至 +100
【黑点】(Black Point)：0-100%
【白点】(White Point)：0-100%
```

#### 色轮偏移（Color Wheels）

```
【阴影色相偏移】：-180° 至 +180°
【阴影饱和度偏移】：-100% 至 +100%
【中间调色相偏移】：-180° 至 +180°
【中间调饱和度偏移】：-100% 至 +100%
【高光色相偏移】：-180° 至 +180°
【高光饱和度偏移】：-100% 至 +100%
```

#### 曲线（Curves）

```
【RGB曲线】：描述整体明暗关系（如：轻微S形、线性、上凸、下凹）
【红通道曲线】：红色分量的亮度分布
【绿通道曲线】：绿色分量的亮度分布
【蓝通道曲线】：蓝色分量的亮度分布
```

#### 饱和度与色相

```
【全局饱和度】(Global Saturation)：0-150%
【色相偏移】(Hue Shift)：-180° 至 +180°
```

#### 胶片模拟（Film Look）

```
【胶片类型】：柯达 Portra、富士 Velvia、爱克发 Vista、伊尔福 Delta 等
【颗粒感】(Grain)：0-100%
【暗角】(Vignette)：0-100%
【光晕】(Flare)：0-100%
```

#### 风格化工具

```
【锐化】(Sharpen)：0-100%
【模糊】(Blur)：0-100%
【去噪】(Denoise)：0-100%
【纹理】(Texture)：0-100%
```

## 输出格式

### 输出文件

解析完成后输出两份文件：

1. **JSON 文件**：`image_analysis.json` - 包含完整结构化解析数据
2. **文本 Prompt 文件**：`image_prompt.txt` - 包含用于 AI 图像生成的文本 prompt

### JSON 输出格式

```json
{
  "contentAndComposition": {
    "subject": "主体描述，如：一位身穿红色长裙的少女",
    "scene": "场景描述，如：黄昏时分的欧式花园",
    "action": "动作状态，如：少女正在轻抚花瓣，神情温柔",
    "details": ["金色长发", "蕾丝裙摆", "粉色玫瑰", "复古路灯"],
    "shotType": "景别，如：中景",
    "angle": "视角，如：平视略微仰视",
    "composition": "构图方式，如：三分法构图，主体位于右侧三分之一处",
    "balance": "画面平衡，如：左侧留白，右侧主体突出，视觉重心稳定"
  },
  "artStyle": {
    "styleType": "风格类型，如：数字插画",
    "movement": "画派，如：现代唯美主义",
    "technique": "技术特点，如：柔和笔触，细腻光影，渐变色彩",
    "era": "时代特征，如：当代",
    "atmosphere": "氛围调性，如：温暖梦幻，浪漫唯美"
  },
  "colorGrading": {
    "primaryWheels": {
      "shadow": {"hue": 30, "saturation": 40, "luminance": 20},
      "midtones": {"hue": 60, "saturation": 50, "luminance": 50},
      "highlights": {"hue": 240, "saturation": 30, "luminance": 80},
      "global": {"hue": 0, "saturation": 45, "luminance": 50}
    },
    "contrast": {
      "contrast": 65,
      "exposure": 0.5,
      "gamma": 1.2,
      "gain": 90,
      "offset": 5,
      "blackPoint": 5,
      "whitePoint": 95
    },
    "colorWheels": {
      "shadowHueShift": 15,
      "shadowSatShift": -10,
      "midtonesHueShift": 5,
      "midtonesSatShift": 5,
      "highlightsHueShift": -10,
      "highlightsSatShift": -5
    },
    "curves": {
      "rgb": "轻微S形曲线，增强对比度",
      "red": "中暗部略抬，增加暖色感",
      "green": "整体平缓",
      "blue": "高光略微下压，减少冷色"
    },
    "saturation": {
      "global": 75,
      "hueShift": 0
    },
    "filmLook": {
      "type": "Kodak Portra 400",
      "grain": 20,
      "vignette": 15,
      "flare": 10
    },
    "stylization": {
      "sharpen": 30,
      "blur": 0,
      "denoise": 15,
      "texture": 25
    },
    "summary": "色彩总结，如：整体偏暖色调，阴影带红色，高光带蓝色，饱和度适中，对比度较高"
  }
}
```

### 文本 Prompt 输出格式

生成适合用于 AI 图像生成的完整文本 prompt：

```
【艺术风格】数字插画风格，现代唯美主义，柔和笔触，细腻光影，渐变色彩，温暖梦幻氛围

【画面内容】一位身穿红色长裙的少女，金色长发，蕾丝裙摆，正在轻抚粉色玫瑰，神情温柔，位于黄昏时分的欧式花园中，复古路灯散发暖光

【构图方式】中景，平视略微仰视，三分法构图，主体位于右侧三分之一处，左侧留白，画面平衡稳定

【色彩参数】达芬奇调色：阴影色相30°饱和度40%亮度20%，中间调色相60°饱和度50%亮度50%，高光色相240°饱和度30%亮度80%，对比度65%，曝光+0.5EV，Gamma 1.2，全局饱和度75%，轻微S形曲线增强对比度，Kodak Portra 400胶片模拟，20%颗粒感，15%暗角

【画质细节】高清，8K分辨率，精美细节，细腻质感，电影级光影
```

## 使用示例

```bash
# 解析本地图片
python scripts/analyze_image.py --image /path/to/image.jpg

# 解析网络图片
python scripts/analyze_image.py --image https://example.com/image.jpg

# 指定输出目录
python scripts/analyze_image.py --image /path/to/image.jpg --output-dir ./output

# 生成简化版 prompt
python scripts/analyze_image.py --image /path/to/image.jpg --mode short
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image` | 图片路径或 URL | 必填 |
| `--output-dir` | 输出目录 | 当前目录 |
| `--mode` | 输出模式：`full`（完整）/ `short`（简化） | `full` |

## 注意事项

1. **色彩参数为估算值**：达芬奇调色参数是基于视觉分析的估算值，精确值需在达芬奇软件中调整。

2. **风格识别的主观性**：艺术风格识别具有主观性，结果可能存在多种解读。

3. **分辨率影响**：低分辨率图片可能影响细节识别精度。

4. **版权注意**：确保解析的图片具有合法使用权限。

5. **输出标准化**：所有输出参数都经过标准化处理，便于后续使用。

## 适用场景

- 游戏美术风格参考提取
- 影视后期色彩分析
- 插画风格学习
- AI 图像生成的 prompt 创作
- 图像内容检索与分类
- 视觉效果复刻与参考