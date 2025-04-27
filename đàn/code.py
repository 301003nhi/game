import tkinter as tk
import pygame

# Kích thước phím
WHITE_KEY_WIDTH = 60
WHITE_KEY_HEIGHT = 300
BLACK_KEY_WIDTH = 20
BLACK_KEY_HEIGHT = 180

# Khởi tạo pygame mixer
pygame.mixer.init()

# Hàm phát âm thanh
def play_sound(note):
    try:
        sound = pygame.mixer.Sound(f"sounds/{note}.wav")
        sound.play()
        note_label.config(text=f"Đang chơi: {note}")
    except Exception as e:
        print(f"Không tìm thấy âm thanh: {note}", e)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Piano 3 quãng")

# Cấu trúc nốt cơ bản
white_base = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_base = ['C#', 'D#', '', 'F#', 'G#', 'A#', '']

# Tạo danh sách nốt theo quãng
white_keys = []
black_keys = []
for octave in range(1, 4):  # 3 quãng tám
    white_keys += [note + str(octave) for note in white_base]
    black_keys += [note + str(octave) if note else '' for note in black_base]

# Tạo canvas theo số lượng phím trắng
canvas_width = len(white_keys) * WHITE_KEY_WIDTH
canvas = tk.Canvas(root, width=canvas_width, height=WHITE_KEY_HEIGHT)
canvas.pack()

# Hiển thị tên nốt
note_label = tk.Label(root, text="Chưa bấm nốt nào", font=("Arial", 16))
note_label.pack(pady=10)

# Vẽ phím trắng
for i, note in enumerate(white_keys):
    x = i * WHITE_KEY_WIDTH
    canvas.create_rectangle(x, 0, x + WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT, fill="white", outline="black", tags=note)

# Vẽ phím đen (chính giữa hai phím trắng, bỏ chỗ không có phím đen)
for i, note in enumerate(black_keys):
    if note != '':
        x = i * WHITE_KEY_WIDTH + (WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2)
        canvas.create_rectangle(x, 0, x + BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT, fill="black", tags=note)

# Bắt sự kiện click chuột
def on_click(event):
    clicked = canvas.find_closest(event.x, event.y)[0]
    note = canvas.gettags(clicked)[0]
    play_sound(note)

canvas.bind("<Button-1>", on_click)
# Bắt sự kiện click chuột
def on_click(event):
    clicked = canvas.find_closest(event.x, event.y)[0]
    note = canvas.gettags(clicked)[0]
    play_sound(note)
    note_label.config(text=f"Đang chơi: {note}")

    # Hiệu ứng trực tiếp: hiện chữ trên phím
    x1, y1, x2, y2 = canvas.coords(clicked)
    text_x = (x1 + x2) / 2
    text_y = (y1 + y2) / 2

    # Tạo dòng chữ trên phím
    text_id = canvas.create_text(text_x, text_y, text=note, fill="red", font=("Arial", 14, "bold"))

    # Đổi màu nền phím (tuỳ chọn)
    original_color = "white" if canvas.itemcget(clicked, "fill") == "white" else "black"
    canvas.itemconfig(clicked, fill="lightgrey")

    # Sau 300ms, xóa chữ và khôi phục màu
    def reset_key():
        canvas.delete(text_id)
        canvas.itemconfig(clicked, fill=original_color)
    canvas.after(300, reset_key)


root.mainloop()
