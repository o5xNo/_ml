import requests

def translate_chinese_to_english(text, model="gemma:2b"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": f"請把以下中文翻譯成英文：{text}",
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        return f"錯誤：無法連線至 Ollama（HTTP {response.status_code}）"

chinese_input = input("請輸入中文：")
english_output = translate_chinese_to_english(chinese_input)
print("翻譯結果：", english_output)
