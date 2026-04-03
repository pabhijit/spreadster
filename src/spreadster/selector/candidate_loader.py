def choose_default_expiration(chain):
    expiries = sorted(chain["expiration"].astype(str).dropna().unique().tolist())
    if not expiries:
        raise ValueError("No expirations available.")
    return expiries[0]
