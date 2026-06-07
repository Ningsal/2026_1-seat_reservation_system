from datetime import datetime

class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}
        # 로그를 저장할 리스트 초기화
        self._history = []

    def _add_log(self, action, seat_id, details=""):
        """내부 메서드: 현재 시간과 함께 행동 로그를 기록합니다."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [Seat {seat_id}] {action} - {details}"
        self._history.append(log_entry)

    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        current = self._get(seat_id)
        if current is not None:
            self._add_log("RESERVE_FAIL", seat_id, f"Already reserved by {current} (Attempted by {name})")
            raise ValueError("Seat is already reserved.")
        
        self._seats[seat_id] = name
        self._add_log("RESERVE_SUCCESS", seat_id, f"Reserved by {name}")
        return seat_id, name

    def cancel(self, seat_id, name=None):
        try:
            current = self._get(seat_id)
        except ValueError as exc:
            # 존재하지 않는 좌석 번호일 때도 로그를 남기고 싶다면 처리
            self._add_log("CANCEL_FAIL", seat_id, "Seat does not exist.")
            raise exc

        if current is None:
            self._add_log("CANCEL_FAIL", seat_id, "Seat is not reserved.")
            raise ValueError("Seat is not reserved.")
            
        if name and current != name:
            self._add_log("CANCEL_FAIL", seat_id, f"Name mismatch (Expected: {current}, Given: {name})")
            raise ValueError("Name does not match the reservation.")
        
        self._seats[seat_id] = None
        self._add_log("CANCEL_SUCCESS", seat_id, f"Reservation for {current} cancelled.")
        return seat_id, None

    def status(self, seat_id):
        # 상태 조회 시에도 로그를 남깁니다.
        seat_id, name = seat_id, self._get(seat_id)
        status_str = f"Reserved by {name}" if name else "Available"
        self._add_log("STATUS_CHECK", seat_id, f"Status: {status_str}")
        return seat_id, name

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def get_history(self):
        """저장된 전체 히스토리 로그를 반환합니다."""
        return self._history

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]