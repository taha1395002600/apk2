"""
====================================================================
 پروژه بازی فکری ماتریکس (Matrix Mind Game)
 نسخه: 1.0.0
 زبان: پایتون (Python 3.x)
 توضیحات: این برنامه یک بازی فکری کامل شامل جدول معما، تایمر،
          سیستم امتیازدهی، راهنما و گرافیک کاربرپسند با Tkinter است.
====================================================================
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class MatrixMindGame:
    def __init__(self, root):
        self.root = root
        self.root.title("بازی فکری ماتریکس - نسخه حرفه‌ای")
        self.root.geometry("750x650")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # متغیرهای وضعیت بازی
        self.score = 0
        self.time_left = 60
        self.timer_running = False
        self.current_level = "متوسط"
        self.grid_size = 3  # ابعاد پیش‌فرض 3 در 3
        self.cells = []
        self.target_sum = 0
        
        # بارگذاری اجزای رابط کاربری
        self.create_header()
        self.create_game_board_frame()
        self.create_control_panel()
        
        # شروع اولین بازی
        self.start_new_game()

    def create_header(self):
        """ساخت بخش بالای صفحه (عنوان و امتیاز)"""
        header_frame = tk.Frame(self.root, bg="#1e1e2f")
        header_frame.pack(pady=15)

        title_label = tk.Label(
            header_frame, 
            text="🧠 چالش فکری ماتریکس", 
            font=("B Nazanin", 20, "bold"), 
            bg="#1e1e2f", 
            fg="#00d2d3"
        )
        title_label.pack()

        # پنل نمایش امتیاز و زمان
        stats_frame = tk.Frame(self.root, bg="#1e1e2f")
        stats_frame.pack(pady=5)

        self.score_label = tk.Label(
            stats_frame, 
            text="امتیاز: 0", 
            font=("Arial", 12, "bold"), 
            bg="#1e1e2f", 
            fg="#ffffff"
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(
            stats_frame, 
            text="زمان: 60 ثانیه", 
            font=("Arial", 12, "bold"), 
            bg="#1e1e2f", 
            fg="#ff6b6b"
        )
        self.timer_label.pack(side=tk.RIGHT, padx=20)

    def create_game_board_frame(self):
        """ساخت فریم اصلی صفحه بازی"""
        self.board_frame = tk.Frame(self.root, bg="#2d2d44", bd=2, relief=tk.GROOVE)
        self.board_frame.pack(pady=10)

        # راهنمای قانون بازی روی صفحه
        self.instruction_label = tk.Label(
            self.root, 
            text="قانون: مجموع اعداد هر سطر و ستون باید عدد هدف را بسازد!", 
            font=("Arial", 11), 
            bg="#1e1e2f", 
            fg="#feca57"
        )
        self.instruction_label.pack(pady=5)

    def create_control_panel(self):
        """ساخت دکمه‌های کنترل بازی (ثبت، راهنما، جدید)"""
        control_frame = tk.Frame(self.root, bg="#1e1e2f")
        control_frame.pack(pady=20)

        check_btn = tk.Button(
            control_frame, 
            text="بررسی پاسخ ✅", 
            font=("Arial", 12, "bold"), 
            bg="#10ac84", 
            fg="white", 
            padx=15, 
            pady=5,
            command=self.check_solution
        )
        check_btn.grid(row=0, column=0, padx=10)

        hint_btn = tk.Button(
            control_frame, 
            text="راهنما 💡", 
            font=("Arial", 12, "bold"), 
            bg="#ff9f43", 
            fg="white", 
            padx=15, 
            pady=5,
            command=self.give_hint
        )
        hint_btn.grid(row=0, column=1, padx=10)

        new_game_btn = tk.Button(
            control_frame, 
            text="بازی جدید 🔄", 
            font=("Arial", 12, "bold"), 
            bg="#54a0ff", 
            fg="white", 
            padx=15, 
            pady=5,
            command=self.start_new_game
        )
        new_game_btn.grid(row=0, column=2, padx=10)

    def generate_puzzle(self):
        """تولید معما و اعداد تصادفی برای جدول"""
        # پاکسازی صفحه قبلی اگر وجود داشته باشد
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.cells = []
        self.target_sum = random.randint(12, 25)
        
        # بروزرسانی راهنما با عدد هدف جدید
        self.instruction_label.config(
            text=f"قانون: مجموع اعداد هر سطر و ستون باید برابر با '{self.target_sum}' باشد!"
        )

        # ساخت خانه‌های ورودی جدول (Entryها)
        for r in range(self.grid_size):
            row_cells = []
            for c in range(self.grid_size):
                e = tk.Entry(
                    self.board_frame, 
                    font=("Arial", 18, "bold"), 
                    width=4, 
                    justify="center",
                    bg="#ffffff",
                    fg="#2f3640"
                )
                e.grid(row=r, column=c, padx=8, pady=8, ipady=8)
                
                # به صورت تصادفی برخی خانه‌ها را پر می‌کنیم یا خالی می‌گذاریم
                if random.choice([True, False]):
                    val = random.randint(1, 9)
                    e.insert(0, str(val))
                    e.config(state="disabled", disabledbackground="#dfe4ea", disabledforeground="#2f3640")
                
                row_cells.append(e)
            self.cells.append(row_cells)

    def start_new_game(self):
        """شروع یا ریست کردن یک راند جدید از بازی"""
        self.generate_puzzle()
        self.time_left = 60
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        """مدیریت تایمر معکوس بازی"""
        if self.timer_running and self.time_left > 0:
            self.timer_label.config(text=f"زمان: {self.time_left} ثانیه")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.timer_running:
            self.timer_running = False
            messagebox.showinfo("پایان زمان!", "زمان شما به اتمام رسید رفیق! دوباره تلاش کن.")
            self.start_new_game()

    def check_solution(self):
        """بررسی صحت پاسخ وارد شده توسط کاربر"""
        try:
            matrix = []
            for r in range(self.grid_size):
                row_vals = []
                for c in range(self.grid_size):
                    val_str = self.cells[r][c].get()
                    if not val_str.isdigit():
                        raise ValueError("لطفاً همه خانه‌ها را با اعداد معتبر پر کنید!")
                    row_vals.append(int(val_str))
                matrix.append(row_vals)

            # بررسی مجموع سطرها
            for r in range(self.grid_size):
                if sum(matrix[r]) != self.target_sum:
                    messagebox.showerror("خطا", f"مجموع اعداد سطر {r+1} اشتباه است!")
                    return

            # بررسی مجموع ستون‌ها
            for c in range(self.grid_size):
                col_sum = sum(matrix[r][c] for r in range(self.grid_size))
                if col_sum != self.target_sum:
                    messagebox.showerror("خطا", f"مجموع اعداد ستون {c+1} اشتباه است!")
                    return

            # اگر همه چیز درست بود
            self.timer_running = False
            earned_score = 10 + self.time_left // 2
            self.score += earned_score
            self.score_label.config(text=f"امتیاز: {self.score}")
            
            messagebox.تبریک = messagebox.showinfo(
                "آفرین رفیق! 🎉", 
                f"معما با موفقیت حل شد!\nامتیاز کسب شده این مرحله: {earned_score}"
            )
            self.start_new_game()

        except ValueError as e:
            messagebox.showwarning("خطای ورودی", str(e))

    def give_hint(self):
        """سیستم راهنمای هوشمند برای کمک به بازیکن"""
        self.score = max(0, self.score - 5)  # کسر امتیاز جزئی برای راهنما
        self.score_label.config(text=f"امتیاز: {self.score}")
        messagebox.showinfo(
            "راهنمای ماتریکس 💡", 
            f"یادآوری: هدف این است که جمع هر سطر و ستون عدد '{self.target_sum}' شود. به اعداد ثابت جدول دقت کن!"
        )

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixMindGame(root)
    root.mainloop()