import heapq

# =============================================================================
# CÂU (c): OBJECT CONVERTOR (SEARCH ENGINE)
# =============================================================================

class ObjectConvertor:
    """
    [BỘ CHUYỂN ĐỔI ĐỐI TƯỢNG]
    Nhiệm vụ: Tìm kiếm chuỗi biến đổi có CHI PHÍ THẤP NHẤT.
    Sử dụng trình quản lý thư viện (TLM) và máy chủ chi phí (CFS).
    """
    def __init__(self, tlm, cfs):
        self.tlm = tlm
        self.cfs = cfs

    def convert(self, start, goal):
        """
        [ALGORITHM]: Sử dụng thuật toán Dijkstra để tìm lộ trình tối ưu.
        Đầu vào: Hai đối tượng O1 và O2.
        Đầu ra: Chuỗi biến đổi giữa O1 và O2 với chi phí thấp nhất.
        """
        # Xác định giá trị lớn nhất trong đích để cắt tỉa nhánh (Pruning)
        max_goal_val = max(goal) if goal else 0
        
        # Priority Queue: (Tổng_chi_phí, Trạng_thái_ma_trận, Lịch_sử_các_bước)
        open_set = [(0, start, [])]
        visited = {start: 0}
        states_explored = 0
        MAX_STATES = 15000 # Giới hạn an toàn

        while open_set:
            g, current, path = heapq.heappop(open_set)
            states_explored += 1
            
            # Kiểm tra trạng thái đích
            if current == goal:
                return path, g
            
            # Ngăn chặn vòng lặp vô hạn hoặc treo máy
            if states_explored > MAX_STATES:
                return None, float('inf')

            # Duyệt qua các toán tử có trong thư viện TLM
            for name, operator in self.tlm.library.items():
                next_state = operator.apply(current)
                
                if next_state != current:
                    # Cắt tỉa (Pruning): Nếu giá trị vượt ngưỡng đích, bỏ qua nhánh này
                    if any(v > max_goal_val for v in next_state):
                        continue
                        
                    # Lấy chi phí từ CFS
                    cost = self.cfs.EvaluateCall(name)
                    new_g = g + cost
                    
                    # Nếu tìm thấy đường đi rẻ hơn tới cùng một trạng thái
                    if next_state not in visited or visited[next_state] > new_g:
                        visited[next_state] = new_g
                        # Đưa vào hàng đợi ưu tiên để xét tiếp
                        heapq.heappush(open_set, (new_g, next_state, path + [(name, next_state, new_g)]))
        
        return None, float('inf')

# =============================================================================
# TOÁN TỬ BIẾN ĐỔI (Dùng cho Câu a)
# =============================================================================

def spread(matrix, dr, dc):
    """Tính toán trạng thái ma trận sau khi lan tỏa hướng (dr, dc)."""
    new_m = list(matrix)
    for r in range(4):
        for c in range(4):
            idx = r * 4 + c
            if matrix[idx] != 0:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 4 and 0 <= nc < 4:
                    nidx = nr * 4 + nc
                    new_m[nidx] = matrix[idx]
    return tuple(new_m)

def multiply(matrix, k):
    """Tính toán trạng thái ma trận sau khi nhân với hệ số K."""
    return tuple(val * k if val != 0 else 0 for val in matrix)
