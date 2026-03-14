import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# ==================== متغيرات المشروع ====================
current_img = None
original_img = None

# ==================== دوال تحديث الصورة ====================

def update_image():
    global current_img
    if current_img is None: return
    
    img_pil = Image.fromarray(current_img)
    img_pil = img_pil.resize((550, 350)) 
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk)
    label.image = img_tk

# ==================== دوال الفلاتر ====================

def apply_filter(filter_type):
    global current_img
    if current_img is None:
        messagebox.showwarning("تنبيه", "الرجاء رفع صورة أولاً!")
        return

    if filter_type == "gray":
        gray = cv2.cvtColor(current_img, cv2.COLOR_RGB2GRAY)
        current_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    elif filter_type == "blur":
        current_img = cv2.GaussianBlur(current_img, (15, 15), 0)
    elif filter_type == "edge":
        gray = cv2.cvtColor(current_img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        current_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    elif filter_type == "cool":
        current_img = cv2.transform(current_img, np.array([[0.8, 0, 0.2], [0, 1.0, 0], [0.1, 0, 1.2]]))
        current_img = np.clip(current_img, 0, 255).astype(np.uint8)
    elif filter_type == "warm":
        current_img = cv2.transform(current_img, np.array([[1.2, 0, 0.1], [0, 1.0, 0], [0.2, 0, 0.8]]))
        current_img = np.clip(current_img, 0, 255).astype(np.uint8)
    elif filter_type == "neon":
        current_img = cv2.convertScaleAbs(current_img, alpha=1.5, beta=10)
    elif filter_type == "pixel":
        h, w = current_img.shape[:2]
        temp = cv2.resize(current_img, (w//20, h//20), interpolation=cv2.INTER_LINEAR)
        current_img = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    elif filter_type == "dark":
        current_img = cv2.convertScaleAbs(current_img, alpha=0.6, beta=-20)
    elif filter_type == "poster":
        n = 4
        current_img = np.uint8(np.floor_divide(current_img, 256//n) * (256//n))
    elif filter_type == "cartoon":
        color = current_img.copy()
        gray = cv2.cvtColor(current_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(color, 9, 250, 250)
        current_img = cv2.bitwise_and(color, color, mask=edges)

    update_image()

def rotate_image():
    global current_img
    if current_img is not None:
        current_img = cv2.rotate(current_img, cv2.ROTATE_90_CLOCKWISE)
        update_image()

def reset_image():
    global current_img, original_img
    if original_img is not None:
        current_img = original_img.copy()
        update_image()

# ==================== دالة الحفظ المعدلة ====================
def save_image():
    global current_img
    if current_img is None: 
        messagebox.showerror("خطأ", "لا توجد صورة لحفظها!")
        return
    
    # إضافة أنواع الملفات والامتداد التلقائي
    file_path = filedialog.asksaveasfilename(
        initialdir="/",
        title="حفظ الصورة باسم",
        defaultextension=".png",
        filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
    )
    
    if file_path:
        # OpenCV يستخدم BGR، لذا نحولها قبل الحفظ لضمان دقة الألوان
        final_img = cv2.cvtColor(current_img, cv2.COLOR_RGB2BGR)
        success = cv2.imwrite(file_path, final_img)
        if success:
            messagebox.showinfo("نجاح", f"تم الحفظ بنجاح في:\n{file_path}")
        else:
            messagebox.showerror("خطأ", "فشل في حفظ الصورة، تأكد من المسار.")

def load_default_image():
    global current_img, original_img
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    img[:, :] = [44, 34, 24] 
    cv2.putText(img, "IMAGE EDITOR", (150, 200), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (210, 180, 140), 3)
    cv2.circle(img, (500, 100), 40, (139, 69, 19), -1)
    current_img = img
    original_img = img.copy()
    update_image()

# ==================== إنشاء الواجهة ====================

root = tk.Tk()
root.title("محرر الصور البني - Brown Photo Editor")
root.geometry("1000x820") 
root.configure(bg="#3E2723") 

btn_style = {"font": ("Segoe UI", 9, "bold"), "relief": "flat", "padx": 10, "pady": 5, "cursor": "hand2", "width": 12}

Label(root, text="BROWN EDITOR", font=("Impact", 30), bg="#3E2723", fg="#D7CCC8").pack(pady=10)

image_frame = Frame(root, bg="#D7CCC8", bd=3, relief="solid")
image_frame.pack(pady=5)
label = Label(image_frame, bg="#D7CCC8")
label.pack(padx=5, pady=5)

btn_container = Frame(root, bg="#3E2723")
btn_container.pack(pady=10, fill="x", padx=50)

# --- الصفوف ---
row1 = Frame(btn_container, bg="#3E2723"); row1.pack(pady=2)
Button(row1, text="رمادي", command=lambda: apply_filter("gray"), bg="#5D4037", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row1, text="سيبيا", command=lambda: apply_filter("warm"), bg="#8D6E63", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row1, text="بارد", command=lambda: apply_filter("cool"), bg="#795548", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row1, text="نيون توهج", command=lambda: apply_filter("neon"), bg="#A1887F", fg="black", **btn_style).pack(side="left", padx=5) 

row2 = Frame(btn_container, bg="#3E2723"); row2.pack(pady=2)
Button(row2, text="تمويه", command=lambda: apply_filter("blur"), bg="#4E342E", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row2, text="حواف", command=lambda: apply_filter("edge"), bg="#6D4C41", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row2, text="كرتون", command=lambda: apply_filter("cartoon"), bg="#8D6E63", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row2, text="بيكسل", command=lambda: apply_filter("pixel"), bg="#A1887F", fg="black", **btn_style).pack(side="left", padx=5) 

row3 = Frame(btn_container, bg="#3E2723"); row3.pack(pady=2)
Button(row3, text="عتمة", command=lambda: apply_filter("dark"), bg="#212121", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row3, text="بوستر", command=lambda: apply_filter("poster"), bg="#BF360C", fg="white", **btn_style).pack(side="left", padx=5) 
Button(row3, text="تدوير", command=rotate_image, bg="#558B2F", fg="white", **btn_style).pack(side="left", padx=5) 

row4 = Frame(btn_container, bg="#3E2723"); row4.pack(pady=15)
Button(row4, text="إعادة تعيين 🔄", command=reset_image, bg="#D84315", fg="white", width=15, font=("Arial", 10, "bold")).pack(side="left", padx=10) 
Button(row4, text="حفظ الصورة 💾", command=save_image, bg="#2E7D32", fg="white", width=15, font=("Arial", 10, "bold")).pack(side="left", padx=10) 

root.after(300, load_default_image)
root.mainloop()