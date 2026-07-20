import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "07e514571c764daeaec7bfbbf1df63e3.o9wh1t6oHLuhkTWP"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

SYSTEM_PROMPT = """你是一位专业的图像分析师。请分析上传的图片，输出结构化的JSON数据，包含以下三个部分：

1. contentAndComposition（图片内容及构图）：
   - subject: 主体对象描述
   - scene: 场景环境描述
   - action: 动作状态描述
   - details: 关键细节数组
   - shotType: 景别（远景/全景/中景/近景/特写）
   - angle: 视角（平视/仰视/俯视/侧视/鸟瞰/低角度）
   - composition: 构图方式
   - balance: 画面平衡描述

2. artStyle（艺术风格）：
   - styleType: 风格类型
   - movement: 画派特征
   - technique: 技术特点
   - era: 时代特征
   - atmosphere: 氛围调性

3. colorGrading（色彩参数，达芬奇调色风格）：
   - primaryWheels: {shadow, midtones, highlights, global}，每个包含hue(0-360), saturation(0-100), luminance(0-100)
   - contrast: {contrast, exposure, gamma, gain, offset, blackPoint, whitePoint}
   - colorWheels: {shadowHueShift, shadowSatShift, midtonesHueShift, midtonesSatShift, highlightsHueShift, highlightsSatShift}
   - curves: {rgb, red, green, blue}
   - saturation: {global, hueShift}
   - filmLook: {type, grain, vignette, flare}
   - stylization: {sharpen, blur, denoise, texture}
   - summary: 色彩总结

请直接输出JSON，不要有任何额外文字，JSON格式严格正确。"""


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_base64 = data.get('image_base64', '')
        image_url = data.get('image_url', '')

        if not image_base64 and not image_url:
            return jsonify({'error': '请提供图片'}), 400

        content = []
        if image_base64:
            content.append({
                'type': 'image_url',
                'image_url': {'url': image_base64}
            })
        elif image_url:
            content.append({
                'type': 'image_url',
                'image_url': {'url': image_url}
            })

        content.append({
            'type': 'text',
            'text': SYSTEM_PROMPT
        })

        payload = {
            'model': 'glm-4v-flash',
            'messages': [
                {
                    'role': 'user',
                    'content': content
                }
            ],
            'temperature': 0.3,
            'max_tokens': 1024
        }

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response_data = response.json()

        if 'error' in response_data:
            return jsonify({'error': response_data['error'].get('message', str(response_data['error']))}), 500

        result_text = response_data['choices'][0]['message']['content'].strip()

        result_text = result_text.strip('```json').strip('```').strip()

        try:
            result_json = json.loads(result_text)
        except json.JSONDecodeError:
            result_json = {'raw': result_text}

        prompt_text = generate_prompt(result_json)

        return jsonify({
            'json': result_json,
            'prompt': prompt_text
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': '网络请求失败: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_prompt(data):
    if 'contentAndComposition' not in data and 'artStyle' not in data:
        return data.get('raw', str(data))

    cc = data.get('contentAndComposition', {})
    style = data.get('artStyle', {})
    color = data.get('colorGrading', {})

    art_style = f"{style.get('styleType', '')}，{style.get('movement', '')}，{style.get('technique', '')}，{style.get('atmosphere', '')}"

    content = f"{cc.get('subject', '')}，{cc.get('scene', '')}，{cc.get('action', '')}，{', '.join(cc.get('details', []))}"

    composition = f"{cc.get('shotType', '')}，{cc.get('angle', '')}，{cc.get('composition', '')}，{cc.get('balance', '')}"

    pw = color.get('primaryWheels', {})
    shadow = pw.get('shadow', {})
    mid = pw.get('midtones', {})
    high = pw.get('highlights', {})
    primary = f"阴影色相{shadow.get('hue', 30)}°饱和度{shadow.get('saturation', 40)}%亮度{shadow.get('luminance', 20)}%，中间调色相{mid.get('hue', 60)}°饱和度{mid.get('saturation', 50)}%亮度{mid.get('luminance', 50)}%，高光色相{high.get('hue', 240)}°饱和度{high.get('saturation', 30)}%亮度{high.get('luminance', 80)}%"

    contrast = color.get('contrast', {})
    contrast_str = f"对比度{contrast.get('contrast', 65)}%，曝光{contrast.get('exposure', 0.5):+}EV，Gamma {contrast.get('gamma', 1.2)}"

    curves = color.get('curves', {})
    curves_str = curves.get('rgb', '轻微S形曲线增强对比度')

    film = color.get('filmLook', {})
    film_str = f"{film.get('type', 'Kodak Portra 400')}胶片模拟"
    film_detail = f"{film.get('grain', 20)}%颗粒感，{film.get('vignette', 15)}%暗角"

    color_params = f"达芬奇调色：{primary}，{contrast_str}，{curves_str}，{film_str}，{film_detail}"

    return f"""【艺术风格】{art_style}

【画面内容】{content}

【构图方式】{composition}

【色彩参数】{color_params}

【画质细节】高清，8K分辨率，精美细节，细腻质感，电影级光影"""


if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════╗
║     图片解析助手 - 后端服务启动中         ║
╚═══════════════════════════════════════════╝

服务地址: http://localhost:5000
API接口:  http://localhost:5000/api/analyze

按 Ctrl+C 停止服务
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
