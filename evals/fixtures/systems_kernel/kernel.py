def aggregate_notional(events, active_symbols):
    totals = {}
    for event in events:
        symbol = event["symbol"]
        is_active = False
        for candidate in active_symbols:
            if candidate == symbol:
                is_active = True
                break
        if not is_active:
            continue
        side = event["side"]
        qty = event["qty"]
        if qty <= 0 or (side != "B" and side != "S"):
            continue
        tag = f"{side}:{symbol}"
        sign = 1 if tag.startswith("B:") else -1
        signed_notional = sign * event["price"] * qty
        if symbol not in totals:
            totals[symbol] = [0, 0]
        totals[symbol][0] += signed_notional
        totals[symbol][1] += qty
    return {sym: (pair[0], pair[1]) for sym, pair in totals.items()}
