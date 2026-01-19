# test0201
import tkinter as tk
from tkinter import messagebox
import CoolProp.CoolProp as CP

def calc_power():
    try:
        m = float(entry_mass.get())
        t1 = float(entry_temp_in.get())
        p1 = float(entry_press_in.get())
        t2 = float(entry_temp_out.get())
        p2 = float(entry_press_out.get())
        eff = float(entry_eff.get()) if entry_eff.get() else 0.98

        # 单位换算
        mass_flow_in = m * 1000 / 3600
        p1_pa = p1 * 1e6
        p2_pa = p2 * 1e6
        t1_k = t1 + 273.15
        t2_k = t2 + 273.15

        h_in = CP.PropsSI('H', 'P', p1_pa, 'T', t1_k, 'Water') / 1000  # 转为 kJ/kg
        h_out = CP.PropsSI('H', 'P', p2_pa, 'T', t2_k, 'Water') / 1000
        delta_h = h_in - h_out
        power_kw = mass_flow_in * delta_h * eff

        result_label.config(text=f"输出功率为：{power_kw:.2f} kW")
        h_label.config(text=f"h₁ = {h_in:.2f} kJ/kg    h₂ = {h_out:.2f} kJ/kg    Δh = {delta_h:.2f} kJ/kg")

        formula_label.config(text="轴功率计算公式：\nP = ṁ × Δh × η\n"
                                  f"= {mass_flow_in:.2f} kg/s × {delta_h:.2f} kJ/kg × {eff:.3f}")

    except Exception as e:
        messagebox.showerror("输入错误", f"计算失败：\n{e}")

# ========== GUI 构建 ==========
root = tk.Tk()
root.title("汽轮机输出功率计算器")
root.geometry("500x550")  # 调整窗口尺寸

font_label = ("微软雅黑", 12)
font_entry = ("微软雅黑", 12)
font_result = ("微软雅黑", 13, "bold")

fields = [
    ("进口流量 (t/h):", "entry_mass"),
    ("进口温度 (℃):", "entry_temp_in"),
    ("进口压力 (MPa):", "entry_press_in"),
    ("出口温度 (℃):", "entry_temp_out"),
    ("出口压力 (MPa):", "entry_press_out"),
    ("机械效率 (一般0.7-0.85):", "entry_eff")
]

for i, (label_text, var_name) in enumerate(fields):
    label = tk.Label(root, text=label_text, font=font_label)
    label.grid(row=i, column=0, padx=10, pady=8, sticky='e')
    entry = tk.Entry(root, font=font_entry, width=20)
    entry.grid(row=i, column=1, padx=10, pady=8)
    globals()[var_name] = entry

btn = tk.Button(root, text="计算功率", font=("微软雅黑", 12), bg="#4CAF50", fg="white", command=calc_power)
btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="输出功率为：", fg="blue", font=font_result)
result_label.grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

h_label = tk.Label(root, text="焓值信息：", fg="gray", font=("微软雅黑", 11))
h_label.grid(row=len(fields)+2, column=0, columnspan=2)

formula_label = tk.Label(root, text="公式：", fg="black", font=("微软雅黑", 11), justify="left")
formula_label.grid(row=len(fields)+3, column=0, columnspan=2, pady=10)

root.mainloop()
