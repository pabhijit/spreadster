from spreadster.providers.provider_factory import get_provider
from spreadster.selector.candidate_loader import choose_default_expiration

def load_market_context(symbol: str, sample: bool = True) -> dict:
    provider = get_provider(sample=sample)
    bars = provider.get_intraday_bars(symbol)
    previous_close = provider.get_previous_close(symbol)
    open_price = provider.get_open_price(symbol)
    spot = provider.get_spot_price(symbol)
    chain = provider.get_option_chain(symbol)
    expiration = choose_default_expiration(chain)
    expected_move = provider.get_expected_move(symbol, expiration, spot, chain)
    return {"provider": provider, "bars": bars, "previous_close": previous_close, "open_price": open_price, "spot": spot, "chain": chain, "expiration": expiration, "expected_move": expected_move}
