import tkinter as tk
import random
import time

class RockPaperScissorsGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("剪刀石头布游戏")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        
        # 游戏数据
        self.player_score = 0
        self.computer_score = 0
        self.round_num = 1
        self.player_choice = None
        self.computer_choice = None
        self.game_active = True
        
        # 手势映射
        self.gestures = {
            "rock": {"name": "石头", "emoji": "✊", "color": "#FF6B6B"},
            "paper": {"name": "布", "emoji": "✋", "color": "#4ECDC4"},
            "scissors": {"name": "剪刀", "emoji": "✌️", "color": "#FFD166"}
        }
        
        # 游戏结果矩阵
        self.results = {
            "rock": {"rock": "平局", "paper": "电脑胜", "scissors": "玩家胜"},
            "paper": {"rock": "玩家胜", "paper": "平局", "scissors": "电脑胜"},
            "scissors": {"rock": "电脑胜", "paper": "玩家胜", "scissors": "平局"}
        }
        
        self.setup_ui()
        self.root.mainloop()
    
    def setup_ui(self):
        # 设置窗口背景
        self.root.configure(bg="#2D3047")
        
        # ==================== 1. 标题区域 (y=0-80) ====================
        # 主标题
        title_label = tk.Label(
            self.root,
            text="✊ ✋ ✌️ 剪刀石头布游戏 ✌️ ✋ ✊",
            font=("Microsoft YaHei", 24, "bold"),
            fg="white",
            bg="#2D3047"
        )
        title_label.place(x=0, y=20, width=1000, height=50)
        
        # 说明文字
        instruction_label = tk.Label(
            self.root,
            text="点击下方手势按钮直接出拳！",
            font=("Microsoft YaHei", 14),
            fg="#FFD166",
            bg="#2D3047"
        )
        instruction_label.place(x=0, y=70, width=1000, height=20)
        
        # ==================== 2. 分数区域 (y=100-180) ====================
        # 玩家分数框
        player_score_frame = tk.Frame(self.root, bg="#2D3047")
        player_score_frame.place(x=100, y=100, width=220, height=80)
        
        tk.Label(
            player_score_frame,
            text="玩家分数",
            font=("Microsoft YaHei", 16),
            fg="#4ECDC4",
            bg="#2D3047"
        ).place(x=0, y=0, width=220, height=30)
        
        self.player_score_label = tk.Label(
            player_score_frame,
            text="0",
            font=("Microsoft YaHei", 36, "bold"),
            fg="#4ECDC4",
            bg="#2D3047"
        )
        self.player_score_label.place(x=0, y=30, width=220, height=50)
        
        # 回合框
        round_frame = tk.Frame(self.root, bg="#2D3047")
        round_frame.place(x=390, y=100, width=220, height=80)
        
        tk.Label(
            round_frame,
            text="当前回合",
            font=("Microsoft YaHei", 16),
            fg="white",
            bg="#2D3047"
        ).place(x=0, y=0, width=220, height=30)
        
        self.round_label = tk.Label(
            round_frame,
            text="第 1 回合",
            font=("Microsoft YaHei", 28, "bold"),
            fg="white",
            bg="#2D3047"
        )
        self.round_label.place(x=0, y=30, width=220, height=50)
        
        # 电脑分数框
        computer_score_frame = tk.Frame(self.root, bg="#2D3047")
        computer_score_frame.place(x=680, y=100, width=220, height=80)
        
        tk.Label(
            computer_score_frame,
            text="电脑分数",
            font=("Microsoft YaHei", 16),
            fg="#FF6B6B",
            bg="#2D3047"
        ).place(x=0, y=0, width=220, height=20)
        
        self.computer_score_label = tk.Label(
            computer_score_frame,
            text="0",
            font=("Microsoft YaHei", 36, "bold"),
            fg="#FF6B6B",
            bg="#2D3047"
        )
        self.computer_score_label.place(x=0, y=30, width=220, height=50)
        
        # ==================== 3. 对战区域 (y=190-380) ====================
        # 玩家对战框 - 使用LabelFrame添加普通框线
        player_battle_frame = tk.LabelFrame(
            self.root,
            text="你的选择",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#4ECDC4",  # 使用玩家颜色
            bg="#2D3047",
            relief="ridge",  # 边框样式
            bd=3,           # 边框宽度
            labelanchor="n"  # 标题在上方
        )
        player_battle_frame.place(x=100, y=190, width=350, height=210)
        
        self.player_display = tk.Label(
            player_battle_frame,
            text="?",
            font=("Segoe UI Emoji", 50),
            fg="gray",
            bg="#2D3047"
        )
        self.player_display.place(x=25, y=30, width=300, height=100)  # y坐标向下调整
        
        self.player_name_label = tk.Label(
            player_battle_frame,
            text="等待出拳...",
            font=("Microsoft YaHei", 16),
            fg="gray",
            bg="#2D3047"
        )
        self.player_name_label.place(x=25, y=130, width=300, height=40)  # y坐标向下调整
        
        # VS标签
        vs_label = tk.Label(
            self.root,
            text="VS",
            font=("Microsoft YaHei", 36, "bold"),
            fg="white",
            bg="#2D3047"
        )
        vs_label.place(x=450, y=240, width=100, height=80)
        
        # 电脑对战框 - 使用LabelFrame添加普通框线
        computer_battle_frame = tk.LabelFrame(
            self.root,
            text="电脑选择",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#FF6B6B",  # 使用电脑颜色
            bg="#2D3047",
            relief="ridge",  # 边框样式
            bd=3,           # 边框宽度
            labelanchor="n"  # 标题在上方
        )
        computer_battle_frame.place(x=550, y=190, width=350, height=210)
        
        self.computer_display = tk.Label(
            computer_battle_frame,
            text="?",
            font=("Segoe UI Emoji", 50),
            fg="gray",
            bg="#2D3047"
        )
        self.computer_display.place(x=25, y=30, width=300, height=100)  # y坐标向下调整
        
        self.computer_name_label = tk.Label(
            computer_battle_frame,
            text="等待中...",
            font=("Microsoft YaHei", 16),
            fg="gray",
            bg="#2D3047"
        )
        self.computer_name_label.place(x=25, y=130, width=300, height=40)  # y坐标向下调整
        
        # ==================== 4. 按钮区域 (y=390-520) ====================
        # 按钮标题
        button_title = tk.Label(
            self.root,
            text="选择你的出拳：",
            font=("Microsoft YaHei", 18),
            fg="white",
            bg="#2D3047"
        )
        button_title.place(x=0, y=400, width=1000, height=30)
        
        # 计算按钮位置，使其均分x轴
        total_width = 1000
        button_width = 160
        button_height = 100
        button_y = 440
        
        # 石头按钮
        self.rock_button = tk.Button(
            self.root,
            text="✊\n石头",
            font=("Segoe UI Emoji", 18, "bold"),
            bg="#FF6B6B",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.immediate_play("rock")
        )
        rock_x = (total_width // 6) - (button_width // 2)
        self.rock_button.place(x=rock_x, y=button_y, width=button_width, height=button_height)
        
        # 布按钮
        self.paper_button = tk.Button(
            self.root,
            text="✋\n布",
            font=("Segoe UI Emoji", 18, "bold"),
            bg="#4ECDC4",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.immediate_play("paper")
        )
        paper_x = (total_width // 2) - (button_width // 2)
        self.paper_button.place(x=paper_x, y=button_y, width=button_width, height=button_height)
        
        # 剪刀按钮
        self.scissors_button = tk.Button(
            self.root,
            text="✌️\n剪刀",
            font=("Segoe UI Emoji", 18, "bold"),
            bg="#FFD166",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.immediate_play("scissors")
        )
        scissors_x = (5 * total_width // 6) - (button_width // 2)
        self.scissors_button.place(x=scissors_x, y=button_y, width=button_width, height=button_height)
        
        # ==================== 5. 结果区域 (y=550-590) ====================
        # 结果区域
        result_frame = tk.Frame(self.root, bg="#1A1C2B")
        result_frame.place(x=100, y=550, width=800, height=40)
        
        self.result_label = tk.Label(
            result_frame,
            text="点击上方按钮开始游戏！",
            font=("Microsoft YaHei", 16),
            bg="#1A1C2B",
            fg="#FFD166"
        )
        self.result_label.place(x=0, y=0, width=800, height=40)
        
        # ==================== 6. 历史记录区域 (y=600-700) ====================
        # 历史记录区域
        history_frame = tk.Frame(self.root, bg="#2D3047")
        history_frame.place(x=100, y=600, width=800, height=100)
        
        tk.Label(
            history_frame,
            text="游戏记录：",
            font=("Microsoft YaHei", 14, "bold"),
            fg="white",
            bg="#2D3047"
        ).place(x=0, y=-10, width=800, height=40)
        
        # 创建文本框和滚动条
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.place(x=780, y=25, width=20, height=70)
        
        self.history_text = tk.Text(
            history_frame,
            font=("Microsoft YaHei", 10),
            bg="#1A1C2B",
            fg="white",
            state="disabled",
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.history_text.place(x=0, y=25, width=780, height=70)
        
        scrollbar.config(command=self.history_text.yview)
        
        # ==================== 7. 控制区域 (y=710-780) ====================
        # 控制区域
        control_frame = tk.Frame(self.root, bg="#2D3047")
        control_frame.place(x=100, y=710, width=800, height=70)
        
        # 游戏规则说明
        rule_label = tk.Label(
            control_frame,
            text="游戏规则：石头赢剪刀，剪刀赢布，布赢石头。先得5分者获胜！",
            font=("Microsoft YaHei", 10),
            fg="#A0A0A0",
            bg="#2D3047"
        )
        rule_label.place(x=0, y=5, width=800, height=20)
        
        # 重新开始按钮（左对齐）
        self.reset_button = tk.Button(
            control_frame,
            text="🔄 重新开始游戏",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#118AB2",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.reset_game
        )
        self.reset_button.place(x=50, y=30, width=180, height=35)
        
        # 退出按钮（右对齐）
        quit_button = tk.Button(
            control_frame,
            text="❌ 退出游戏",
            font=("Microsoft YaHei", 12),
            bg="#EF476F",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.root.quit
        )
        quit_button.place(x=570, y=30, width=180, height=35)
    
    def immediate_play(self, gesture):
        """立即出拳：选择手势并立即与电脑对决"""
        if not self.game_active:
            return
        
        # 禁用所有出拳按钮，防止重复点击
        self.rock_button.config(state="disabled")
        self.paper_button.config(state="disabled")
        self.scissors_button.config(state="disabled")
        
        # 显示玩家选择
        self.player_choice = gesture
        player_info = self.gestures[gesture]
        
        self.player_display.config(
            text=player_info["emoji"],
            fg=player_info["color"]
        )
        self.player_name_label.config(
            text=player_info["name"],
            fg=player_info["color"]
        )
        
        # 同时进行电脑选择（删除倒计时，直接出结果）
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        computer_info = self.gestures[self.computer_choice]
        
        # 立即显示电脑选择
        self.computer_display.config(
            text=computer_info["emoji"],
            fg=computer_info["color"]
        )
        self.computer_name_label.config(
            text=computer_info["name"],
            fg=computer_info["color"]
        )
        
        self.root.update()
        time.sleep(0.2)  # 短暂延迟，让用户能看到结果
        
        # 判断胜负
        result = self.results[self.player_choice][self.computer_choice]
        self.show_result(result)
        
        # 启用所有出拳按钮
        self.rock_button.config(state="normal")
        self.paper_button.config(state="normal")
        self.scissors_button.config(state="normal")
    
    def show_result(self, result):
        """显示游戏结果"""
        if result == "玩家胜":
            result_text = "🎉 恭喜！你赢了！ 🎉"
            result_color = "#4ECDC4"
            self.player_score += 1
            self.player_score_label.config(text=f"{self.player_score}")
        elif result == "电脑胜":
            result_text = "😔 电脑赢了，下次加油！"
            result_color = "#FF6B6B"
            self.computer_score += 1
            self.computer_score_label.config(text=f"{self.computer_score}")
        else:
            result_text = "🤝 平局！再来一次！"
            result_color = "#FFD166"
        
        self.result_label.config(text=result_text, fg=result_color)
        
        # 添加游戏记录
        player_name = self.gestures[self.player_choice]["name"]
        computer_name = self.gestures[self.computer_choice]["name"]
        
        history_entry = f"回合 {self.round_num}: {player_name} vs {computer_name} → {result_text}\n"
        
        self.history_text.config(state="normal")
        self.history_text.insert("1.0", history_entry)
        self.history_text.config(state="disabled")
        
        # 更新回合数
        self.round_num += 1
        self.round_label.config(text=f"第 {self.round_num} 回合")
        
        # 检查是否有人获胜
        if self.player_score >= 5:
            self.show_final_result("玩家")
            self.game_active = False
            self.result_label.config(text="🎉 游戏结束！玩家获胜！ 🎉", fg="#4ECDC4")
        elif self.computer_score >= 5:
            self.show_final_result("电脑")
            self.game_active = False
            self.result_label.config(text="😔 游戏结束！电脑获胜！ 😔", fg="#FF6B6B")
    
    def show_final_result(self, winner):
        """显示最终结果"""
        if winner == "玩家":
            message = "🎉 恭喜！你获得了最终胜利！ 🎉"
            color = "#4ECDC4"
        else:
            message = "😔 电脑获得了最终胜利，下次加油！"
            color = "#FF6B6B"
        
        final_window = tk.Toplevel(self.root)
        final_window.title("游戏结束")
        final_window.geometry("500x250")
        final_window.configure(bg="#2D3047")
        final_window.resizable(False, False)
        final_window.transient(self.root)
        final_window.grab_set()
        
        # 居中显示
        final_window.update_idletasks()
        width = final_window.winfo_width()
        height = final_window.winfo_height()
        x = (final_window.winfo_screenwidth() // 2) - (width // 2)
        y = (final_window.winfo_screenheight() // 2) - (height // 2)
        final_window.geometry(f'{width}x{height}+{x}+{y}')
        
        tk.Label(
            final_window,
            text="游戏结束",
            font=("Microsoft YaHei", 24, "bold"),
            fg=color,
            bg="#2D3047"
        ).pack(pady=20)
        
        tk.Label(
            final_window,
            text=message,
            font=("Microsoft YaHei", 14),
            fg="white",
            bg="#2D3047",
            wraplength=450
        ).pack(pady=10)
        
        tk.Label(
            final_window,
            text=f"最终比分: {self.player_score} - {self.computer_score}",
            font=("Microsoft YaHei", 12),
            fg="white",
            bg="#2D3047"
        ).pack(pady=10)
        
        tk.Button(
            final_window,
            text="确定",
            font=("Microsoft YaHei", 12),
            bg=color,
            fg="white",
            width=10,
            relief="flat",
            command=final_window.destroy
        ).pack(pady=15)
    
    def reset_game(self):
        """重置游戏"""
        self.player_score = 0
        self.computer_score = 0
        self.round_num = 1
        self.player_choice = None
        self.computer_choice = None
        self.game_active = True
        
        # 更新分数显示
        self.player_score_label.config(text=f"{self.player_score}")
        self.computer_score_label.config(text=f"{self.computer_score}")
        
        # 更新回合显示
        self.round_label.config(text=f"第 {self.round_num} 回合")
        
        # 重置玩家显示
        self.player_display.config(text="?", fg="gray")
        self.player_name_label.config(text="等待出拳...", fg="gray")
        
        # 重置电脑显示
        self.computer_display.config(text="?", fg="gray")
        self.computer_name_label.config(text="等待中...", fg="gray")
        
        # 重置结果提示
        self.result_label.config(text="点击上方按钮开始游戏！", fg="#FFD166")
        
        # 清空历史记录
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state="disabled")
        
        # 启用所有按钮
        self.rock_button.config(state="normal")
        self.paper_button.config(state="normal")
        self.scissors_button.config(state="normal")

if __name__ == "__main__":
    game = RockPaperScissorsGame()