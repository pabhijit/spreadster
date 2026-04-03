def compute_vwap_signal(vwap_flips: int, close_price: float, current_vwap: float, session_range: float) -> dict:
    dist_from_vwap = abs(close_price - current_vwap)
    vwap_test_pass = (vwap_flips >= 2) and (dist_from_vwap <= max(session_range * 0.20, 5.0))
    return {"dist_from_vwap": dist_from_vwap, "vwap_test_pass": vwap_test_pass}
