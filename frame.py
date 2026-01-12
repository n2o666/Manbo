import tkinter as tk
import random
import time
import os
import threading
from datetime import datetime

class RockPaperScissorsGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("剪刀石头布游戏 - 手势识别版")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        
        # 游戏模式
        self.game_mode = "button"  # 初始为按钮模式: "button" 或 "gesture"
        
        # 游戏数据
        self.player_score = 0
        self.computer_score = 0
        self.round_num = 1
        self.player_choice = None
        self.computer_choice = None
        self.game_active = True
        
        # 手势识别相关
        self.external_input_enabled = True  # 是否启用外部文件输入
        self.gesture_input_file = "gesture_input.txt"
        self.current_gesture_id = None  # 当前手势ID
        self.last_gesture_time = 0  # 最后检测到手势的时间
        self.gesture_checking = False  # 是否正在检测手势
        self.gesture_countdown_active = False  # 倒计时是否激活
        self.countdown_value = 0  # 当前倒计时值
        
        # 手势ID映射
        self.gesture_id_map = {
            5: "rock",      # 石头
            4: "paper",     # 布
            6: "scissors",  # 剪刀
            -1: None        # 无手势
        }
        
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
        self.start_gesture_monitor()  # 启动手势监控线程
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
        
        # 模式显示
        self.mode_label = tk.Label(
            self.root,
            text="当前模式: 按钮模式",
            font=("Microsoft YaHei", 14),
            fg="#FFD166",
            bg="#2D3047"
        )
        self.mode_label.place(x=0, y=70, width=1000, height=20)
        
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
        # 玩家对战框 - 增加高度以容纳更多内容
        player_battle_frame = tk.LabelFrame(
            self.root,
            text="你的选择",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#4ECDC4",
            bg="#2D3047",
            relief="ridge",
            bd=3,
            labelanchor="n"
        )
        player_battle_frame.place(x=100, y=190, width=350, height=210)
        
        self.player_display = tk.Label(
            player_battle_frame,
            text="?",
            font=("Segoe UI Emoji", 50),
            fg="gray",
            bg="#2D3047"
        )
        self.player_display.place(x=25, y=20, width=300, height=100)
        
        self.player_name_label = tk.Label(
            player_battle_frame,
            text="等待出拳...",
            font=("Microsoft YaHei", 16),
            fg="gray",
            bg="#2D3047"
        )
        self.player_name_label.place(x=25, y=130, width=300, height=40)
        
        # VS标签
        vs_label = tk.Label(
            self.root,
            text="VS",
            font=("Microsoft YaHei", 36, "bold"),
            fg="white",
            bg="#2D3047"
        )
        vs_label.place(x=450, y=240, width=100, height=80)
        
        # 电脑对战框
        computer_battle_frame = tk.LabelFrame(
            self.root,
            text="电脑选择",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#FF6B6B",
            bg="#2D3047",
            relief="ridge",
            bd=3,
            labelanchor="n"
        )
        computer_battle_frame.place(x=550, y=190, width=350, height=210)
        
        self.computer_display = tk.Label(
            computer_battle_frame,
            text="?",
            font=("Segoe UI Emoji", 50),
            fg="gray",
            bg="#2D3047"
        )
        self.computer_display.place(x=25, y=30, width=300, height=100)
        
        self.computer_name_label = tk.Label(
            computer_battle_frame,
            text="等待中...",
            font=("Microsoft YaHei", 16),
            fg="gray",
            bg="#2D3047"
        )
        self.computer_name_label.place(x=25, y=130, width=300, height=40)
        
        # ==================== 4. 按钮区域 (y=390-520) ====================
        # 按钮标题
        self.button_title = tk.Label(
            self.root,
            text="选择你的出拳：",
            font=("Microsoft YaHei", 18),
            fg="white",
            bg="#2D3047"
        )
        self.button_title.place(x=0, y=400, width=1000, height=30)
        
        # 按钮容器
        self.button_frame = tk.Frame(self.root, bg="#2D3047")
        self.button_frame.place(x=0, y=440, width=1000, height=100)
        
        # 创建按钮
        self.create_buttons()
        
        # ==================== 5. 结果区域 (y=550-590) ====================
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
        history_frame = tk.Frame(self.root, bg="#2D3047")
        history_frame.place(x=100, y=600, width=800, height=100)
        
        tk.Label(
            history_frame,
            text="游戏记录：",
            font=("Microsoft YaHei", 14, "bold"),
            fg="white",
            bg="#2D3047"
        ).place(x=0, y=-10, width=800, height=40)
        
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
        control_frame = tk.Frame(self.root, bg="#2D3047")
        control_frame.place(x=100, y=710, width=800, height=70)
        
        # 模式切换按钮
        self.mode_button = tk.Button(
            control_frame,
            text="🔄 切换到手势模式",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#9D4EDD",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.toggle_game_mode
        )
        self.mode_button.place(x=50, y=10, width=180, height=35)
        
        # 手势开始按钮（初始隐藏）
        self.gesture_start_button = tk.Button(
            control_frame,
            text="🤚 开始手势猜拳",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#FF9E00",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.start_gesture_countdown
        )
        self.gesture_start_button.place(x=250, y=10, width=180, height=35)
        self.gesture_start_button.place_forget()  # 初始隐藏
        
        # 重新开始按钮
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
        self.reset_button.place(x=450, y=10, width=180, height=35)
        
        # 退出按钮
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
        quit_button.place(x=650, y=10, width=180, height=35)
        
        # 模式介绍标签
        self.mode_info_label = tk.Label(
            control_frame,
            text="游戏规则：石头赢剪刀，剪刀赢布，布赢石头。先得5分者获胜！",
            font=("Microsoft YaHei", 10),
            fg="#A0A0A0",
            bg="#2D3047"
        )
        self.mode_info_label.place(x=0, y=45, width=800, height=20)
    
    def create_buttons(self):
        """创建游戏按钮"""
        total_width = 1000
        button_width = 160
        button_height = 100
        
        # 清除之前的按钮
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        if self.game_mode == "button":
            # 按钮模式：显示三个手势按钮
            self.rock_button = tk.Button(
                self.button_frame,
                text="✊\n石头",
                font=("Segoe UI Emoji", 18, "bold"),
                bg="#FF6B6B",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda: self.immediate_play("rock")
            )
            rock_x = (total_width // 6) - (button_width // 2)
            self.rock_button.place(x=rock_x, y=0, width=button_width, height=button_height)
            
            self.paper_button = tk.Button(
                self.button_frame,
                text="✋\n布",
                font=("Segoe UI Emoji", 18, "bold"),
                bg="#4ECDC4",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda: self.immediate_play("paper")
            )
            paper_x = (total_width // 2) - (button_width // 2)
            self.paper_button.place(x=paper_x, y=0, width=button_width, height=button_height)
            
            self.scissors_button = tk.Button(
                self.button_frame,
                text="✌️\n剪刀",
                font=("Segoe UI Emoji", 18, "bold"),
                bg="#FFD166",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda: self.immediate_play("scissors")
            )
            scissors_x = (5 * total_width // 6) - (button_width // 2)
            self.scissors_button.place(x=scissors_x, y=0, width=button_width, height=button_height)
            
            self.button_title.config(text="选择你的出拳：")
            
        else:
            # 手势模式：只显示一个开始按钮
            self.gesture_action_button = tk.Button(
                self.button_frame,
                text="点击开始手势游戏\n（3秒倒计时）",
                font=("Microsoft YaHei", 14, "bold"),
                bg="#9D4EDD",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=self.start_gesture_countdown
            )
            gesture_x = (total_width // 2) - (button_width * 1.5 // 2)
            self.gesture_action_button.place(x=gesture_x, y=0, width=button_width*1.5, height=button_height)
            
            self.button_title.config(text="手势模式：点击开始按钮后做出手势")
    
    def toggle_game_mode(self):
        """切换游戏模式"""
        if self.game_mode == "button":
            self.game_mode = "gesture"
            self.mode_label.config(text="当前模式: 手势模式", fg="#9D4EDD")
            self.mode_button.config(text="🔄 切换到按钮模式")
            self.mode_info_label.config(
                text="手势模式：做出石头(5)、布(4)、剪刀(6)手势，点击开始按钮后3秒内识别",
                fg="#A0A0A0"
            )
            self.gesture_start_button.place(x=250, y=10, width=180, height=35)
            self.reset_button.place(x=450, y=10, width=180, height=35)
        else:
            self.game_mode = "button"
            self.mode_label.config(text="当前模式: 按钮模式", fg="#FFD166")
            self.mode_button.config(text="🔄 切换到手势模式")
            self.mode_info_label.config(
                text="游戏规则：石头赢剪刀，剪刀赢布，布赢石头。先得5分者获胜！",
                fg="#A0A0A0"
            )
            self.gesture_start_button.place_forget()
            self.reset_button.place(x=450, y=10, width=180, height=35)
            
            # 重置手势相关状态
            self.gesture_countdown_active = False
            self.gesture_checking = False
        
        # 重置玩家显示
        self.player_display.config(text="?", fg="gray")
        self.player_name_label.config(
            text="等待出拳..." if self.game_mode == "button" else "等待手势...", 
            fg="gray"
        )
        
        # 重置结果提示
        if self.game_mode == "button":
            self.result_label.config(text="点击上方按钮开始游戏！", fg="#FFD166")
        else:
            self.result_label.config(text="切换到手势模式，请点击开始按钮", fg="#9D4EDD")
        
        # 重新创建按钮
        self.create_buttons()
        
        # 确保游戏处于激活状态
        self.game_active = True
    
    def start_gesture_countdown(self):
        """开始手势模式倒计时"""
        if not self.game_active or self.gesture_countdown_active:
            return
        
        self.gesture_countdown_active = True
        self.gesture_checking = True
        
        # 重置显示
        self.player_display.config(text="?", fg="gray")
        self.player_name_label.config(text="准备手势...", fg="#FFD166")
        self.result_label.config(text="请做出手势...", fg="#FFD166")
        
        # 禁用按钮
        self.gesture_action_button.config(state="disabled")
        self.gesture_start_button.config(state="disabled")
        
        # 开始倒计时
        self.countdown_value = 3
        self.update_countdown()
    
    def update_countdown(self):
        """更新倒计时"""
        if not self.gesture_countdown_active:
            return
        
        if self.countdown_value > 0:
            # 显示倒计时
            self.player_name_label.config(
                text=f"倒计时: {self.countdown_value} 秒", 
                fg="#FF6B6B"
            )
            
            self.countdown_value -= 1
            self.root.after(1000, self.update_countdown)
        else:
            # 倒计时结束，检查手势
            self.check_gesture_input()
    
    def check_gesture_input(self):
        """检查手势输入"""
        if not self.gesture_checking:
            return
        
        # 获取当前手势
        gesture_id = self.current_gesture_id
        gesture_name = self.gesture_id_map.get(gesture_id)
        
        if gesture_name:
            # 手势识别成功
            self.player_choice = gesture_name
            player_info = self.gestures[gesture_name]
            
            self.player_display.config(
                text=player_info["emoji"],
                fg=player_info["color"]
            )
            self.player_name_label.config(
                text=player_info["name"],
                fg=player_info["color"]
            )
            
            # 电脑选择
            self.computer_choice = random.choice(["rock", "paper", "scissors"])
            computer_info = self.gestures[self.computer_choice]
            
            self.computer_display.config(
                text=computer_info["emoji"],
                fg=computer_info["color"]
            )
            self.computer_name_label.config(
                text=computer_info["name"],
                fg=computer_info["color"]
            )
            
            # 判断胜负
            result = self.results[self.player_choice][self.computer_choice]
            self.show_result(result)
            
        else:
            # 手势识别失败
            self.player_name_label.config(text="未检测到有效手势", fg="#FF6B6B")
            self.result_label.config(text="未检测到有效手势，请重试", fg="#FF6B6B")
            
            # 重置电脑显示
            self.computer_display.config(text="?", fg="gray")
            self.computer_name_label.config(text="等待中...", fg="gray")
        
        # 重置状态
        self.gesture_countdown_active = False
        self.gesture_checking = False
        
        # 启用按钮
        self.gesture_action_button.config(state="normal")
        self.gesture_start_button.config(state="normal")
        
        # 等待2秒后重置玩家显示
        self.root.after(2000, self.reset_gesture_display)
    
    def reset_gesture_display(self):
        """重置手势显示"""
        if self.game_mode == "gesture" and not self.gesture_countdown_active:
            self.player_display.config(text="?", fg="gray")
            self.player_name_label.config(text="等待手势...", fg="gray")
            if not self.gesture_checking:
                self.result_label.config(text="点击开始按钮进行手势猜拳", fg="#9D4EDD")
    
    def start_gesture_monitor(self):
        """启动手势监控线程"""
        def monitor_gesture():
            while True:
                if self.game_mode == "gesture" and self.external_input_enabled:
                    self.read_gesture_from_file()
                time.sleep(0.1)  # 每100毫秒检查一次
        
        thread = threading.Thread(target=monitor_gesture, daemon=True)
        thread.start()
    
    def read_gesture_from_file(self):
        """从文件读取手势"""
        try:
            if os.path.exists(self.gesture_input_file):
                with open(self.gesture_input_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        try:
                            gesture_id = int(content)
                            # 只接受有效的手势ID
                            if gesture_id in [4, 5, 6, -1]:
                                self.current_gesture_id = gesture_id
                                self.last_gesture_time = time.time()
                                
                                # 如果在检测手势中，更新显示
                                if self.gesture_checking and self.gesture_countdown_active:
                                    gesture_name = self.gesture_id_map.get(gesture_id)
                                    if gesture_name:
                                        gesture_info = self.gestures[gesture_name]
                                        self.player_name_label.config(
                                            text=f"检测到: {gesture_info['name']}",
                                            fg=gesture_info["color"]
                                        )
                        except ValueError:
                            pass
        except Exception as e:
            print(f"读取手势文件错误: {e}")
    
    def immediate_play(self, gesture):
        """按钮模式：立即出拳"""
        if not self.game_active or self.game_mode != "button":
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
        
        # 电脑选择
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        computer_info = self.gestures[self.computer_choice]
        
        # 显示电脑选择
        self.computer_display.config(
            text=computer_info["emoji"],
            fg=computer_info["color"]
        )
        self.computer_name_label.config(
            text=computer_info["name"],
            fg=computer_info["color"]
        )
        
        self.root.update()
        time.sleep(0.2)
        
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
        
        mode_text = "手势" if self.game_mode == "gesture" else "按钮"
        history_entry = f"回合 {self.round_num} ({mode_text}): {player_name} vs {computer_name} → {result_text}\n"
        
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
        if self.game_mode == "button":
            self.player_name_label.config(text="等待出拳...", fg="gray")
        else:
            self.player_name_label.config(text="等待手势...", fg="gray")
        
        # 重置电脑显示
        self.computer_display.config(text="?", fg="gray")
        self.computer_name_label.config(text="等待中...", fg="gray")
        
        # 重置结果提示
        if self.game_mode == "button":
            self.result_label.config(text="点击上方按钮开始游戏！", fg="#FFD166")
        else:
            self.result_label.config(text="点击开始按钮进行手势猜拳", fg="#9D4EDD")
        
        # 清空历史记录
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state="disabled")
        
        # 重置手势状态
        self.gesture_countdown_active = False
        self.gesture_checking = False
        
        # 启用所有按钮
        if self.game_mode == "button":
            self.rock_button.config(state="normal")
            self.paper_button.config(state="normal")
            self.scissors_button.config(state="normal")
        else:
            self.gesture_action_button.config(state="normal")
            self.gesture_start_button.config(state="normal")

if __name__ == "__main__":
    game = RockPaperScissorsGame()