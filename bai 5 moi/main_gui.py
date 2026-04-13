import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sys
import io

# Import các thành phần đã tách ra theo câu a, b, c
from tlm_manager import TransformationLibraryManager
from cfs_server import CostFunctionServer
from search_engine import ObjectConvertor, spread, multiply

# =============================================================================
# CẤU HÌNH GIAO DIỆN CHÍNH
# =============================================================================

# Setup UTF-8 cho Windows Terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class IntegratedMatrixApp(ctk.CTk):
    """
    [GIAO DIỆN TỔNG HỢP (CÂU D)]
    Kết hợp toàn bộ các module a, b, c để trình diễn ví dụ thực tế.
    """
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Biến đổi Ma trận Tối ưu (Module-based)")
        self.geometry("1100x850")

        self.history = []
        self.current_idx = -1

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar: Câu (a) và (b) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # UI Câu (a) - Thư viện
        self.label_a = ctk.CTkLabel(self.sidebar, text="(a) QUẢN LÝ TOÁN TỬ (TLM)", 
                                    font=ctk.CTkFont(size=14, weight="bold"), text_color="#3a7ebf")
        self.label_a.pack(pady=(10, 5))
        
        self.tlm_frame = ctk.CTkFrame(self.sidebar, fg_color="gray20")
        self.tlm_frame.pack(fill="x", padx=10, pady=5)
        
        self.op_vars = {}
        for op in ["LÊN", "XUỐNG", "TRÁI", "PHẢI", "NHÂN"]:
            var = tk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.tlm_frame, text=f"Kích hoạt: {op}", variable=var)
            cb.pack(anchor="w", padx=15, pady=5)
            self.op_vars[op] = var

        self.lbl_tlm_status = ctk.CTkLabel(self.sidebar, text="Thư viện: Đang trống", 
                                           font=("Arial", 12, "italic"), text_color="gray")
        self.lbl_tlm_status.pack(pady=(0, 10))

        # UI Câu (b) - Chi phí
        self.label_b = ctk.CTkLabel(self.sidebar, text="(b) MÁY CHỦ CHI PHÍ (CFS)", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_b.pack(pady=(20, 5))
        
        self.cost_entries = {}
        for op in ["LÊN", "XUỐNG", "TRÁI", "PHẢI", "NHÂN"]:
            frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            frame.pack(fill="x", padx=20)
            ctk.CTkLabel(frame, text=f"Phí {op}:", width=80).pack(side="left")
            ent = ctk.CTkEntry(frame, width=80)
            ent.insert(0, "5" if op != "NHÂN" else "10")
            ent.pack(side="right", pady=2)
            self.cost_entries[op] = ent

        ctk.CTkLabel(self.sidebar, text="Hệ số K:").pack(pady=(10, 0))
        self.ent_k = ctk.CTkEntry(self.sidebar, width=160)
        self.ent_k.insert(0, "2")
        self.ent_k.pack(pady=5)

        # --- Main Layout: Câu (c) và (d) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # UI Câu (c) - Nhập ma trận
        self.input_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_container.pack(fill="x", pady=10)
        self.start_entries = self.create_grid(self.input_container, "(c) MA TRẬN ĐẦU (O1)", 0)
        self.goal_entries = self.create_grid(self.input_container, "(c) MA TRẬN ĐÍCH (O2)", 1)

        self.run_btn = ctk.CTkButton(self.main_frame, text="CHẠY THUẬT TOÁN (DIJKSTRA)", 
                                     font=ctk.CTkFont(size=16, weight="bold"), height=50, command=self.run_process)
        self.run_btn.pack(pady=10)

        # UI Câu (d) - Trực quan hóa kết quả
        ctk.CTkLabel(self.main_frame, text="(d) KẾT QUẢ TRUY VẤN", font=ctk.CTkFont(size=14, weight="bold")).pack()
        self.canvas = tk.Canvas(self.main_frame, bg="#1a1a1a", height=350, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=40, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw_state())

        self.ctrl_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.ctrl_frame.pack(pady=10)
        ctk.CTkButton(self.ctrl_frame, text="< Trước", width=100, command=self.prev_step).pack(side="left", padx=10)
        self.lbl_step = ctk.CTkLabel(self.ctrl_frame, text="Bước: 0/0", font=ctk.CTkFont(weight="bold"))
        self.lbl_step.pack(side="left", padx=10)
        ctk.CTkButton(self.ctrl_frame, text="Sau >", width=100, command=self.next_step).pack(side="left", padx=10)

        self.lbl_log = ctk.CTkLabel(self.main_frame, text="Hệ thống sẵn sàng.", text_color="gray")
        self.lbl_log.pack(pady=5)

    def create_grid(self, parent, title, col):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=col, padx=20, pady=5)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4)
        entries = []
        for r in range(4):
            row = []
            for c in range(4):
                e = ctk.CTkEntry(frame, width=45, justify="center")
                e.grid(row=r+1, column=c, padx=2, pady=2)
                e.insert(0, "0")
                row.append(e)
            entries.append(row)
        return entries

    def get_matrix(self, ent_list):
        vals = []
        for r in range(4):
            for c in range(4):
                try: vals.append(int(ent_list[r][c].get()))
                except: vals.append(0)
        return tuple(vals)

    def run_process(self):
        # 1. Khởi tạo TLM (Câu a)
        tlm = TransformationLibraryManager()
        k = int(self.ent_k.get())
        registered_ops = []
        
        if self.op_vars["LÊN"].get(): 
            tlm.TLMinsert("LÊN", lambda m: spread(m, -1, 0))
            registered_ops.append("LÊN")
        if self.op_vars["XUỐNG"].get(): 
            tlm.TLMinsert("XUỐNG", lambda m: spread(m, 1, 0))
            registered_ops.append("XUỐNG")
        if self.op_vars["TRÁI"].get(): 
            tlm.TLMinsert("TRÁI", lambda m: spread(m, 0, -1))
            registered_ops.append("TRÁI")
        if self.op_vars["PHẢI"].get(): 
            tlm.TLMinsert("PHẢI", lambda m: spread(m, 0, 1))
            registered_ops.append("PHẢI")
        if self.op_vars["NHÂN"].get(): 
            tlm.TLMinsert("NHÂN", lambda m: multiply(m, k))
            registered_ops.append("NHÂN")

        # Cập nhật trạng thái hiển thị câu (a)
        if registered_ops:
            self.lbl_tlm_status.configure(text=f"Câu a có các toán tử sử dụng là: {', '.join(registered_ops)}", text_color="#00ff00")
        else:
            self.lbl_tlm_status.configure(text="Câu a chưa có toán tử nào được chọn", text_color="#ff4444")

        # 2. Khởi tạo CFS (Câu b)
        cfs = CostFunctionServer()
        for op in self.cost_entries:
            try: val = int(self.cost_entries[op].get())
            except: val = 1
            cfs.Costinsert(op, val)

        # 3. Lấy ma trận (Câu c)
        start = self.get_matrix(self.start_entries)
        goal = self.get_matrix(self.goal_entries)

        # 4. Tìm kiếm (Câu c engine)
        conv = ObjectConvertor(tlm, cfs)
        path, cost = conv.convert(start, goal)

        if path is not None:
            self.history = [("BẮT ĐẦU", start, 0)] + path
            self.current_idx = 0
            self.draw_state()
            self.lbl_log.configure(text=f"Thành công! Tổng chi phí: {cost}", text_color="green")
        else:
            self.history = []
            self.current_idx = -1
            self.lbl_log.configure(text="THẤT BẠI: Không thể biến đổi được!", text_color="#ff4444")
            self.canvas.delete("all")
            self.lbl_step.configure(text="Bước: 0/0")
            messagebox.showwarning("Thông báo", "Không tìm thấy con đường biến đổi hợp lệ!")

    def draw_state(self):
        if not self.history or self.current_idx == -1: return
        self.canvas.delete("all")
        desc, matrix, total_g = self.history[self.current_idx]
        self.lbl_step.configure(text=f"Bước: {self.current_idx} / {len(self.history)-1}")
        
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 50: w, h = 600, 300
        size = min(w, h) - 60
        cell_size = size // 4
        ox, oy = (w - size)//2, (h - size)//2

        for i in range(16):
            r, c = divmod(i, 4)
            val = matrix[i]
            x1, y1 = ox + c * cell_size, oy + r * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = "#1f538d" if val != 0 else "#2b2b2b"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", width=2)
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val), fill="white", font=("Arial", 16, "bold"))
        
        self.canvas.create_text(w//2, h - 25, text=f"Hành động hiện tại: {desc}", fill="cyan", font=("Arial", 14, "italic"))

    def next_step(self):
        if self.current_idx < len(self.history) - 1:
            self.current_idx += 1
            self.draw_state()

    def prev_step(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.draw_state()

if __name__ == "__main__":
    app = IntegratedMatrixApp()
    app.mainloop()
