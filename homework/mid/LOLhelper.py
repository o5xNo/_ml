import tkinter as tk
from tkinter import ttk, messagebox
import json
import difflib
import google.generativeai as genai

API_KEY = "AIzaSyCIfzIPSPgAqdVv6DJ9og2rcr0oUVerT2Y"
genai.configure(api_key=API_KEY)

# 載入英雄資料
with open("heroes.json", "r", encoding="utf-8") as f:
    heroes = json.load(f)

# 自訂 Combobox：支援模糊搜尋與自動補全
class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._orig_values = self["values"]
        self.bind("<KeyRelease>", self._on_keyrelease)

    def _on_keyrelease(self, event):
        value = self.get()
        if value == "":
            self["values"] = self._orig_values
        else:
            matches = difflib.get_close_matches(value, self._orig_values, n=10, cutoff=0.3)
            self["values"] = matches
            if matches:
                self.event_generate('<Down>')  # 自動打開下拉

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
        combo = AutocompleteCombobox(frame, values=heroes)
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
你是一位英雄聯盟的戰術分析師，請用繁體中文分析以下雙方陣容（版本25.10）：
藍隊：{blue_team}
紅隊：{red_team}

請針對以下幾點進行分析：
1. 哪一方打團較強？
2. 哪一方前期、中期與後期較強？
3. 哪一方控制技能（CC）較完整？
4. 哪一方邊線能力較強？
5. 你覺得30分鐘前哪對的勝率高？
6. 你覺得30分鐘後哪對的勝率高？
7. 請總結並給出戰術建議。
8. 滿分100你給兩隊各多少分？
"""

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        result = response.text.strip()
        print("\n分析結果如下：\n" + result)
        messagebox.showinfo("分析結果", result)

    except Exception as e:
        print("Gemini API 錯誤：", e)
        messagebox.showerror("錯誤", f"呼叫 Gemini API 發生錯誤：\n{str(e)}")

btn = ttk.Button(root, text="分析陣容", command=analyze)
btn.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
