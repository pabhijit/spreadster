from spreadster.models import TradeCandidate
from spreadster.formatting.tos_formatter import open_code, close_code

def test_put_credit_spread_tos_codes():
    c = TradeCandidate(strategy_type="PUT_CREDIT_SPREAD", symbol="SPX", expiration="2026-03-27", short_put=5550, long_put=5500, estimated_credit=1.2, quantity=10)
    assert "VERTICAL" in open_code(c)
    assert "@0.84" in close_code(c, 0.30, quantity=5)
