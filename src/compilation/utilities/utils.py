from datetime import datetime


def get_timestamp(use_ms: bool = False) -> str:
    now = datetime.now()
    if use_ms:
        # Truncate microseconds to 3 digits for milliseconds
        return now.strftime("%Y%m%d_%H%M%S_%f")[:18]
    return now.strftime("%Y%m%d_%H%M%S")


def get_duration_s(start_hh_mm_ss: str, end_hh_mm_ss: str) -> int:
    start_seconds = sum(
        x * int(t) for x, t in zip([3600, 60, 1], start_hh_mm_ss.split(":"))
    )
    end_seconds = sum(
        x * int(t) for x, t in zip([3600, 60, 1], end_hh_mm_ss.split(":"))
    )
    return end_seconds - start_seconds
