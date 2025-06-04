import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests  # 加入 requests

# 載入英雄資料
with open("heroes.json", "r", encoding="utf-8") as f:
    heroes = json.load(f)

root = tk.Tk()
root.title("英雄聯盟陣容分析工具")

positions = ["上路", "打野", "中路", "射手", "輔助"]
teams = ["藍隊", "紅隊"]
team_frames = {}
team_heroes = {team: {} for team in teams}

for idx, team in enumerate(teams):
    frame = ttk.LabelFrame(root, text=team)
    frame.grid(row=0, column=idx, padx=10, pady=10)
    team_frames[team] = frame
    for i, pos in enumerate(positions):
        ttk.Label(frame, text=pos).grid(row=i, column=0, sticky="w")
        combo = ttk.Combobox(frame, values=heroes, state="readonly")
        combo.grid(row=i, column=1)
        team_heroes[team][pos] = combo

def analyze():
    try:
        blue_team = {pos: cb.get() for pos, cb in team_heroes["藍隊"].items()}
        red_team = {pos: cb.get() for pos, cb in team_heroes["紅隊"].items()}

        if any(v == "" for v in blue_team.values()) or any(v == "" for v in red_team.values()):
            messagebox.showwarning("選擇不完整", "請選擇雙方完整的五位英雄")
            return

        prompt = f"""
你是一位英雄聯盟的戰術分析師，請用繁體中文分析以下雙方陣容：
藍隊：{blue_team}
紅隊：{red_team}

請針對以下幾點進行分析：
1. 哪一方打團較強？
2. 哪一方前期、中期與後期較強？
3. 哪一方控制技能（CC）較完整？
4. 哪一方邊線能力較強？
5. 你覺得30分鐘前哪對的勝率高?
6. 你覺得30分鐘後哪對的勝率高?
7. 請總結並給出戰術建議。
"""

        payload = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": "你是一位英雄聯盟分析師，專門進行繁體中文戰術建議。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800,
        }

        response = requests.post("http://localhost:1234/v1/chat/completions", json=payload)
        data = response.json()

        result = data["choices"][0]["message"]["content"].strip()
        print("\n分析結果如下：\n" + result)
        messagebox.showinfo("分析結果", result)

    except Exception as e:
        print("本地模型錯誤：", e)
        messagebox.showerror("錯誤", f"呼叫 LM Studio 模型發生錯誤：\n{str(e)}")

btn = ttk.Button(root, text="分析陣容", command=analyze)
btn.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
