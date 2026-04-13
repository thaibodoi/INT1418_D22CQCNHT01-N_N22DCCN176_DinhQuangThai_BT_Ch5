# =============================================================================
# CÂU (b): COST FUNCTION SERVER (CFS)
# =============================================================================

class CostFunctionServer:
    """
    [MÁY CHỦ HÀM CHI PHÍ - CFS]
    Nhiệm vụ: Phát triển cú pháp biểu diễn chi phí và cung cấp giá trị chi phí cho hệ thống.
    Đạt yêu cầu: Có hàm Costinsert và EvaluateCall.
    """
    def __init__(self):
        # Lưu trữ cặp (Tên_toán_tử, Giá_trị_chi_phí)
        self.costs = {}

    def Costinsert(self, operator_name, value):
        """
        [Costinsert]: Nhận tên toán tử và định nghĩa chi phí của nó.
        Giúp đăng ký cấu hình giá vào hệ thống.
        """
        self.costs[operator_name] = value
        # print(f"[CFS] Đã nạp chi phí cho {operator_name}: {value}")

    def EvaluateCall(self, operator_name):
        """
        [EvaluateCall]: Nhận một phép biến đổi và trả về chi phí của nó.
        Đầu vào là toán tử, đầu ra là giá trị số tương ứng.
        """
        # Trả về giá trị chi phí đã đăng ký, nếu không tìm thấy mặc định là 1 đơn vị
        return self.costs.get(operator_name, 1)
