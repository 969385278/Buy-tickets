import tkinter as tk
from tkinter import ttk, messagebox
import re
from main import BrushTicket  # 导入你的抢票类


class TicketBookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("12306 自动抢票系统")
        self.root.geometry("600x500")

        # 城市字典
        self.city_list = {
            'bj': '%u5317%u4EAC%2CBJP',  # 北京
            'nn': '%u5357%u5B81%2CNNZ',  # 南宁
            'wh': '%u6B66%u6C49%2CWHN',  # 武汉
            'cs': '%u957F%u6C99%2CCSQ',  # 长沙
            'qj': '%u6F5C%u6C5F%2CQJN',  # 潜江
            'njn': '%u5357%u4EAC%u5357%2CNKH',  # 南京南
            'shhq': '%u4E0A%u6D77%u8679%u6865%2CAOH',  # 上海虹桥
            'gzn': '%u5E7F%u5DDE%u5357%2CIZQ',  # 广州南
            'wzn': '%u68A7%u5DDE%u5357%2CWBZ',  # 梧州南
        }

        # 座位类型
        self.seat_types = [
            '商务座特等座', '一等座', '二等座', '高级软卧',
            '软卧', '动卧', '硬卧', '软座', '硬座', '无座', '其他'
        ]

        self.create_widgets()

    def create_widgets(self):
        # 用户名
        ttk.Label(self.root, text="12306用户名:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # 密码
        ttk.Label(self.root, text="12306密码:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # 乘车人
        ttk.Label(self.root, text="乘车人:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.passengers_entry = ttk.Entry(self.root)
        self.passengers_entry.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # 乘车日期
        ttk.Label(self.root, text="乘车日期(YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        # 出发站
        ttk.Label(self.root, text="出发站:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.from_station = ttk.Combobox(self.root, values=list(self.city_list.keys()))
        self.from_station.grid(row=4, column=1, padx=5, pady=5, sticky="we")

        # 终点站
        ttk.Label(self.root, text="终点站:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.to_station = ttk.Combobox(self.root, values=list(self.city_list.keys()))
        self.to_station.grid(row=5, column=1, padx=5, pady=5, sticky="we")

        # 座位类型
        ttk.Label(self.root, text="座位类型:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.seat_type = ttk.Combobox(self.root, values=self.seat_types)
        self.seat_type.grid(row=6, column=1, padx=5, pady=5, sticky="we")
        self.seat_type.current(4)  # 默认选择软卧

        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        # 开始抢票按钮
        self.start_button = ttk.Button(button_frame, text="开始抢票", command=self.start_booking)
        self.start_button.pack(side="left", padx=5)

        # 停止按钮
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_booking, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # 日志区域
        ttk.Label(self.root, text="操作日志:").grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="w")
        self.log_text = tk.Text(self.root, height=10, state="disabled")
        self.log_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # 配置网格权重
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(9, weight=1)

    def log_message(self, message):
        """在日志区域添加消息"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()

    def validate_inputs(self):
        """验证输入是否有效"""
        if not self.username_entry.get():
            messagebox.showerror("错误", "用户名不能为空")
            return False

        if not self.password_entry.get():
            messagebox.showerror("错误", "密码不能为空")
            return False

        if not self.passengers_entry.get():
            messagebox.showerror("错误", "乘车人不能为空")
            return False

        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not re.match(date_pattern, self.date_entry.get()):
            messagebox.showerror("错误", "乘车日期格式不正确，应为YYYY-MM-DD")
            return False

        if not self.from_station.get() in self.city_list:
            messagebox.showerror("错误", "请选择有效的出发站")
            return False

        if not self.to_station.get() in self.city_list:
            messagebox.showerror("错误", "请选择有效的终点站")
            return False

        if not self.seat_type.get():
            messagebox.showerror("错误", "请选择座位类型")
            return False

        return True

    def start_booking(self):
        """开始抢票"""
        if not self.validate_inputs():
            return

        # 禁用开始按钮，启用停止按钮
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # 获取输入值
        username = self.username_entry.get()
        password = self.password_entry.get()
        passengers = self.passengers_entry.get().split(",")
        from_time = self.date_entry.get()
        from_station = self.city_list[self.from_station.get()]
        to_station = self.city_list[self.to_station.get()]
        seat_type = self.seat_type.get()

        self.log_message("开始抢票...")
        self.log_message(f"用户名: {username}")
        self.log_message(f"乘车人: {', '.join(passengers)}")
        self.log_message(f"乘车日期: {from_time}")
        self.log_message(f"出发站: {self.from_station.get()}")
        self.log_message(f"终点站: {self.to_station.get()}")
        self.log_message(f"座位类型: {seat_type}")

        # 创建抢票实例
        try:
            self.brush_ticket = BrushTicket(
                username, password, passengers, from_time,
                from_station, to_station, seat_type
            )
            # 在新线程中运行抢票，避免阻塞GUI
            import threading
            self.booking_thread = threading.Thread(target=self.brush_ticket.start_brush)
            self.booking_thread.daemon = True
            self.booking_thread.start()
        except Exception as e:
            self.log_message(f"错误: {str(e)}")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def stop_booking(self):
        """停止抢票"""
        self.log_message("正在停止抢票...")
        try:
            # 这里需要你在BrushTicket类中添加一个停止方法
            if hasattr(self, 'brush_ticket') and self.brush_ticket:
                self.brush_ticket.driver.quit()  # 关闭浏览器
        except Exception as e:
            self.log_message(f"停止时出错: {str(e)}")

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log_message("抢票已停止")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingGUI(root)
    root.mainloop()