# =============================================================================
# CÂU (a): TRANSFORMATION LIBRARY MANAGER (TLM)
# =============================================================================

class TransformationOperator:
    """
    [CÚ PHÁP BIỂN DIỄN TOÁN TỬ]
    Lớp này dùng để định nghĩa cấu trúc của một phép biến đổi.
    Mọi toán tử trong hệ thống đều phải tuân theo cấu trúc này.
    """
    def __init__(self, name, function):
        self.name = name
        self.function = function  # Logic thực thi (hàm xử lý ma trận)

    def apply(self, state):
        """Thực thi phép biến đổi trên trạng thái hiện tại."""
        return self.function(state)

class TransformationLibraryManager:
    """
    [TRÌNH QUẢN LÝ THƯ VIỆN BIẾN ĐỔI - TLM]
    Nhiệm vụ: Nhận đầu vào, lưu trữ và cung cấp các toán tử cho hệ thống.
    Đạt yêu cầu: Có hàm TLMinsert và TLMsearch.
    """
    def __init__(self):
        # Thư viện lưu trữ dưới dạng Dictionary (Key: Tên, Value: Đối tượng toán tử)
        self.library = {}

    def TLMinsert(self, name, function):
        """
        [TLMinsert]: Nhận tên và hàm logic để thêm vào thư viện.
        Thỏa mãn yêu cầu nạp toán tử vào hệ thống.
        """
        operator = TransformationOperator(name, function)
        self.library[name] = operator
        # print(f"[TLM] Đã đăng ký toán tử: {name}")

    def TLMsearch(self, name):
        """
        [TLMsearch]: Cung cấp tên, trả về phiên bản khởi tạo của toán tử.
        Thỏa mãn yêu cầu truy xuất toán tử để sử dụng.
        """
        if name in self.library:
            return self.library[name]
        return None
