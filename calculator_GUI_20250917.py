import math
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# 多層級的經脈數據
meridian_data = {
    "黑血石": {
        "手三陽經": {
            "手陽明大腸經": (0.6, 0.3, 0.1),
            "手少陽三焦經": (0.61, 0.295, 0.095),
            "手太陽小腸經": (0.62, 0.29, 0.09)
        },
        "手三陰經": {
            "手太陰肺經": (0.63, 0.285, 0.085),
            "手厥陰心包經": (0.64, 0.28, 0.08),
            "手少陰心經": (0.65, 0.275, 0.075)
        },
        "足三陽經": {
            "足少陽膽經": (0.66, 0.27, 0.07),
            "足太陽膀胱經": (0.67, 0.265, 0.065),
            "足陽明胃經": (0.68, 0.26, 0.06)
        },
        "手厥陰陽經": {
            "手厥陽焦丹經": (0.62, 0.29, 0.09),
            "手少陰三焦經": (0.65, 0.275, 0.075),
            "足太陰腸經": (0.68, 0.26, 0.06)
        },
        "手少陰三經": {
            "足少陰太經": (0.66, 0.27, 0.07),
            "足太陰陽經": (0.68, 0.26, 0.06),
            "足少陰腎經": (0.69, 0.255, 0.055)
        },
        "手三厥陰經": {
            "手三陽大經": (0.62, 0.29, 0.09),
            "手三陰大經": (0.65, 0.275, 0.075),
            "手三陰脾經": (0.68, 0.26, 0.06)
        },
        "手太陰經": {
            "手太陰濕土肺經": (0.62, 0.29, 0.09),
            "手太陰濕土脾經": (0.65, 0.275, 0.075),
            "手太陰濕肺金經": (0.68, 0.26, 0.06)
        }
    },
    "黃血石": {
        "足三陰經": {
            "足太陰膀胱經": (0.6, 0.3, 0.1),
            "足太陰脾經": (0.63, 0.285, 0.085),
            "足厥陰肝經": (0.63, 0.285, 0.085)
        },
        "足少陰商經": {
            "足厥陰陽經": (0.64, 0.28, 0.08),
            "足厥陰大經": (0.64, 0.28, 0.08)
        }
    }
}

def calculate_probability():
    # 獲取用戶輸入
    try:
        p1_val = float(p1_entry.get())
        p2_val = float(p2_entry.get())
        p3_val = float(p3_entry.get())
        total_draws_val = int(draws_entry.get())
        sum_target_val = int(target_entry.get())
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "請輸入有效的數值")
        return
    
    # 清除之前的結果
    result_text.delete(1.0, tk.END)
    
    # 優化資料結構減少記憶體佔用
    solution_map = defaultdict(list)
    total_probability = 0.0
    
    # 優化迴圈結構，減少不必要的計算
    for x in range(0, total_draws_val + 1):
        remaining_draws = total_draws_val - x
        if 3*x > sum_target_val: 
            continue
            
        for y in range(0, remaining_draws + 1):
            remaining_draws_after_y = remaining_draws - y
            current_sum = 3*x + 2*y
            
            if current_sum > sum_target_val:
                continue
                
            z = sum_target_val - current_sum
            if z < 0 or z > remaining_draws_after_y:
                continue
                
            n = x + y + z
            if n > total_draws_val:
                continue

            # 計算組合數
            coeff = math.factorial(n) // (math.factorial(x) * math.factorial(y) * math.factorial(z))
            prob = coeff * (p3_val ** x) * (p2_val ** y) * (p1_val ** z)
            total_probability += prob
            
            # 使用字典分組
            solution_map[n].append((x, y, z, coeff, prob))

    # 顯示結果
    counter = 1
    for n, solutions in sorted(solution_map.items()):
        for sol in solutions:
            x, y, z, coeff, prob = sol
            if counter <= 30:  # 只顯示前30個解，避免介面卡頓
                result_text.insert(tk.END, 
                    f"{counter}. 3*{x} + 2*{y} + 1*{z} (n={n}, coeff={coeff}) => 機率 = {prob:.7f}\n")
            counter += 1
    
    result_text.insert(tk.END, 
        f"\n總機率 (最多衝{total_draws_val}次，目標{sum_target_val}個洞): {total_probability:.7f}")

def lock_prob_entries():
    """鎖定機率輸入框"""
    p1_entry.config(state='disabled')
    p2_entry.config(state='disabled')
    p3_entry.config(state='disabled')

def unlock_prob_entries():
    """解鎖機率輸入框"""
    p1_entry.config(state='normal')
    p2_entry.config(state='normal')
    p3_entry.config(state='normal')

def update_category_combo(event=None):
    # 清除當前選擇的經脈種類和細項
    category_combo.set('')
    meridian_combo.set('')
    
    # 獲取選中的物品
    selected_item = item_combo.get()
    # 更新經脈種類下拉清單
    if selected_item in meridian_data:
        categories = list(meridian_data[selected_item].keys())
        category_combo['values'] = categories
        # 解鎖機率輸入框
        unlock_prob_entries()
    else:
        category_combo['values'] = []
        # 如果是自訂選項，允許修改機率
        if selected_item == "自訂":
            unlock_prob_entries()
        else:
            lock_prob_entries()

def update_meridian_combo(event=None):
    # 清除當前選擇的經脈細項
    meridian_combo.set('')
    
    # 獲取選中的物品和經脈種類
    selected_item = item_combo.get()
    selected_category = category_combo.get()
    
    # 更新經脈細項下拉清單
    if selected_item in meridian_data and selected_category in meridian_data[selected_item]:
        meridians = list(meridian_data[selected_item][selected_category].keys())
        meridian_combo['values'] = meridians
        # 解鎖機率輸入框
        unlock_prob_entries()
    else:
        meridian_combo['values'] = []

def set_meridian_prob(event=None):
    # 獲取選中的物品、經脈種類和細項
    selected_item = item_combo.get()
    selected_category = category_combo.get()
    selected_meridian = meridian_combo.get()
    
    # 自訂模式時允許修改機率
    if selected_item == "自訂":
        unlock_prob_entries()
        return
    
    # 獲取機率值並設置到輸入框
    if (selected_item in meridian_data and 
        selected_category in meridian_data[selected_item] and 
        selected_meridian in meridian_data[selected_item][selected_category]):
        
        p1_val, p2_val, p3_val = meridian_data[selected_item][selected_category][selected_meridian]
        
        # 更新機率輸入框
        unlock_prob_entries()  # 臨時解鎖以修改值
        p1_entry.delete(0, tk.END)
        p1_entry.insert(0, f"{p1_val:.3f}")
        p2_entry.delete(0, tk.END)
        p2_entry.insert(0, f"{p2_val:.3f}")
        p3_entry.delete(0, tk.END)
        p3_entry.insert(0, f"{p3_val:.3f}")
        lock_prob_entries()  # 重新鎖定輸入框

# 創建主窗口
root = tk.Tk()
root.title("經脈打通機率計算器")
root.geometry("750x700")  # 增加寬度以適應層級選擇

# 分類選擇區域
selection_frame = ttk.LabelFrame(root, text="經脈分類選擇")
selection_frame.pack(pady=10, padx=10, fill="x")

# 物品選擇 (設置為唯讀下拉清單)
ttk.Label(selection_frame, text="物品類別:").grid(row=0, column=0, padx=5, pady=5)
item_values = list(meridian_data.keys()) + ["自訂"]
item_combo = ttk.Combobox(selection_frame, values=item_values, state="readonly")
item_combo.grid(row=0, column=1, padx=5, pady=5)
item_combo.current(0)  # 預設選擇第一個選項
item_combo.bind("<<ComboboxSelected>>", update_category_combo)

# 經脈種類選擇 (設置為唯讀下拉清單)
ttk.Label(selection_frame, text="經脈種類:").grid(row=1, column=0, padx=5, pady=5)
category_combo = ttk.Combobox(selection_frame, state="readonly")
category_combo.grid(row=1, column=1, padx=5, pady=5)
category_combo.bind("<<ComboboxSelected>>", update_meridian_combo)

# 經脈細項選擇 (設置為唯讀下拉清單)
ttk.Label(selection_frame, text="具體經脈:").grid(row=2, column=0, padx=5, pady=5)
meridian_combo = ttk.Combobox(selection_frame, state="readonly")
meridian_combo.grid(row=2, column=1, padx=5, pady=5)
meridian_combo.bind("<<ComboboxSelected>>", set_meridian_prob)

# 機率輸入區域
prob_frame = ttk.LabelFrame(root, text="打通機率")
prob_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(prob_frame, text="P1 (打通+1):").grid(row=0, column=0, padx=5, pady=5)
p1_entry = ttk.Entry(prob_frame)
p1_entry.grid(row=0, column=1, padx=5, pady=5)
p1_entry.insert(0, "0.651")

ttk.Label(prob_frame, text="P2 (打通+2):").grid(row=1, column=0, padx=5, pady=5)
p2_entry = ttk.Entry(prob_frame)
p2_entry.grid(row=1, column=1, padx=5, pady=5)
p2_entry.insert(0, "0.263")

ttk.Label(prob_frame, text="P3 (打通+3):").grid(row=2, column=0, padx=5, pady=5)
p3_entry = ttk.Entry(prob_frame)
p3_entry.grid(row=2, column=1, padx=5, pady=5)
p3_entry.insert(0, "0.086")

# 次數和目的地區域
params_frame = ttk.LabelFrame(root, text="目標設定")
params_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(params_frame, text="總打通次數:").grid(row=0, column=0, padx=5, pady=5)
draws_entry = ttk.Entry(params_frame)
draws_entry.grid(row=0, column=1, padx=5, pady=5)
draws_entry.insert(0, "10")

ttk.Label(params_frame, text="目標總和:").grid(row=1, column=0, padx=5, pady=5)
target_entry = ttk.Entry(params_frame)
target_entry.grid(row=1, column=1, padx=5, pady=5)
target_entry.insert(0, "20")

# 按鈕
calculate_btn = ttk.Button(root, text="計算機率", command=calculate_probability)
calculate_btn.pack(pady=10)

# 結果顯示區域
result_frame = ttk.LabelFrame(root, text="計算結果")
result_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, yscrollcommand=scrollbar.set)
result_text.pack(fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=result_text.yview)

# 初始化設置
update_category_combo()  # 觸發更新
set_meridian_prob()      # 設置初始機率
lock_prob_entries()      # 初始鎖定機率輸入框

root.mainloop()

