from datetime import datetime, timedelta

class SeatStore:
    def __init__(self, seat_ids, timeout_seconds=30):
        # 구조 변경: seat_id -> {"name": name, "reserved_at": datetime} 또는 None
        self._seats = {seat_id: None for seat_id in seat_ids}
        self.timeout = timedelta(seconds=timeout_seconds)

    def _cleanup_expired_reservations(self):
        """명령어가 실행될 때마다 호출되어 만료된 예약을 자동으로 취소."""
        now = datetime.now()
        for seat_id, info in list(self._seats.items()):
            if info is not None:
                # 예약 시간 + 제한 시간이 현재 시간보다 과거라면 만료 대상
                if info["reserved_at"] + self.timeout < now:
                    self._seats[seat_id] = None
                    print(f"\n[시스템 알림] 좌석 {seat_id}({info['name']})의 예약 시간이 만료되어 자동 취소되었습니다.")

    def list_seats(self):
        self._cleanup_expired_reservations()
        # CLI에서 깨지지 않도록 (seat_id, name) 튜플 형태로 변환해서 반환
        return [(seat_id, info["name"] if info else None) for seat_id, info in self._seats.items()]

    def reserve(self, seat_id, name):
        self._cleanup_expired_reservations()
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        
        # 예약할 때 현재 시간을 함께 저장
        self._seats[seat_id] = {
            "name": name,
            "reserved_at": datetime.now()
        }
        return seat_id, name

    def cancel(self, seat_id, name=None):
        self._cleanup_expired_reservations()
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name and current["name"] != name:
            raise ValueError("Name does not match the reservation.")
        
        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        self._cleanup_expired_reservations()
        info = self._get(seat_id)
        return seat_id, (info["name"] if info else None)

    def stats(self):
        self._cleanup_expired_reservations()
        reserved = sum(1 for info in self._seats.values() if info)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]