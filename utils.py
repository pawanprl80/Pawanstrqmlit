# utils.py
def get_display_ltp(symbol, ltp):
    return round(ltp,2)

def get_signal_color(buy_signal, sell_signal, intensity):
    if buy_signal:
        return f'rgba(0,255,0,{intensity})'
    elif sell_signal:
        return f'rgba(255,0,0,{intensity})'
    else:
        return f'rgba(0,255,255,{intensity})'
