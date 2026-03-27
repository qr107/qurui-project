import tkinter as tk  # 与桌面窗口、图形界面相关的库
from PIL import Image, ImageTk  # 与图像处理相关的库、模块
import itertools  # 与迭代、循环相关的库

class DesktopPet:
    def __init__(self, target_size=120):
        self.gif_paths = ["cat3.gif","cat2.gif","luo2.gif","cat1.gif","luo3.gif"]
        self.current_gif_idx = 0
        self.window = tk.Tk()  # 创建一个窗口属性
        self.window.overrideredirect(True)  # 用overrideredirect方法去掉边框
        self.window.attributes("-topmost", True)  # 让窗口永远在最前面
        self.window.config(bg="white")  # 设置窗口背景颜色，方便后续设透明
        self.window.wm_attributes("-transparentcolor", "white")  # 把指定颜色白色变透明
        self.target_size = target_size
        self.startx = 0
        self.starty = 0  # 初始化坐标变量

        # 加载初始GIF（从列表取第一个）
        self.frames = []  # 创建一个frames属性，初始化为空列表
        self.load_gif(self.gif_paths[self.current_gif_idx], target_size)  # 实现启动时加载首张GIF
        self.loop = itertools.cycle(self.frames)  # 无限循环
        self.label = tk.Label(self.window, bd=0, bg="white")  # 创建标签控件，属性用来显示图片
        self.label.pack()  # 把label布局到窗口中

        # 拖动+双击换图
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<Double-Button-1>", self.switch_gif)  # 绑定操作和函数

        # 播放
        self.update_frame()  # 显示第一帧GIF，启动动画循环
        self.window.geometry(f"+500+500")  # 初始窗口出现在屏幕(500,500)位置
        self.window.mainloop()  # 窗口保持显示，监听拖动/双击等事件，持续播放动画

    # 自动等比例缩放 GIF
    def load_gif(self, gif_path, target_size):
        self.frames.clear()  # 清空旧帧
        try:
            im = Image.open(gif_path)  # 打开图片，把这张图片的每一帧装进变量 im 里存起来
            while True:
                frame = im.copy().convert("RGBA")  # 复制图片并转化为透明模式
                w, h = frame.size  # 用w、h 拿到图片原来的大小
                scale = target_size / max(w, h)  # scale 算出要缩小多少倍
                new_w = int(w * scale)
                new_h = int(h * scale)  # 得到新的等比例大小
                frame_resized = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)  # 保证高清改大小
                self.frames.append(ImageTk.PhotoImage(frame_resized))  # 将改好的帧追加到列表中
                im.seek(len(self.frames))  # 定位到下一帧
        except EOFError:
            pass

    def update_frame(self):

        self.label.config(image=next(self.loop))  # 显示下一帧
        self.window.after(100, self.update_frame)  # 120 = 播放速度，越大越慢

    def start_drag(self, event):
        self.startx = event.x
        self.starty = event.y

    def drag(self, event):
        x = self.window.winfo_x() + event.x - self.startx
        # 新窗口x坐标 = 原窗口x坐标 + (拖动时鼠标在控件内的x - 按下时鼠标在控件内的x)
        y = self.window.winfo_y() + event.y - self.starty
        self.window.geometry(f"+{x}+{y}")

    def switch_gif(self, event):
        self.current_gif_idx = (self.current_gif_idx + 1) % len(self.gif_paths)  # 循环切换索引（取余：到最后自动回到第一张）
        self.load_gif(self.gif_paths[self.current_gif_idx], self.target_size)  # 加载新GIF
        self.loop = itertools.cycle(self.frames)  # 重置迭代器
        self.label.config(image=next(self.loop))  # 立即显示新帧

if __name__ == "__main__":  # 程序入口判断
    DesktopPet( target_size=130)
