dashboard.py (Final Combined Streamlit Layout: Visual Validator + Heatmap + Slippage Metrics)

import streamlit as st import pandas as pd import plotly.graph_objects as go from streamlit_autorefresh import st_autorefresh import time

Backend modules

from main import ws_manager, candle_builder, signal_validator, order_manager

=====================

Glassmorphism CSS

=====================

st.markdown("""

<style>
body {
    background: linear-gradient(135deg, #1e1e2f, #2c2c3e);
    color: white;
}
.frosted-panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: all 0.5s ease-in-out;
}
.progress-bar {
    width: 100%;
    background-color: rgba(255,255,255,0.2);
    border-radius: 5px;
    margin-bottom: 10px;
    overflow: hidden;
}
.progress-bar-inner {
    height: 10px;
    background-color: limegreen;
    border-radius: 5px;
    transition: width 0.5s linear;
}
</style>""", unsafe_allow_html=True)

=====================

Sidebar Navigation

=====================

st.sidebar.title("Pawan Master Algo System") page = st.sidebar.radio("Navigation", ['Visual Validator', 'Heatmap', 'Slippage Metrics'])

symbols = ['NIFTY', 'BANKNIFTY', 'BTCUSDT', 'ETHUSDT'] timeframes = ['1m','5m','15m','1h'] REFRESH_INTERVAL = 1 ROTATE_INTERVAL = 5 st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="datarefresh")

=====================

LTP Smoothing

=====================

prev_ltp = {} def get_display_ltp(symbol, new_ltp, threshold=0.5): if symbol not in prev_ltp: prev_ltp[symbol] = new_ltp if abs(prev_ltp[symbol] - new_ltp) >= threshold: prev_ltp[symbol] = new_ltp return prev_ltp[symbol]

=====================

Visual Validator Page

=====================

if page == 'Visual Validator': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Visual Validator - Multi-Symbol Scroll")

for symbol in symbols:
    with st.expander(f"{symbol}", expanded=False):
        candles = candle_builder.get_candles(symbol, '1m')
        if not candles.empty:
            signals = signal_validator.validate_signal(candles)
            last_idx = len(candles)-1
            ltp_display = get_display_ltp(symbol, candles['close'].iloc[last_idx])

            fig = go.Figure(data=[go.Candlestick(
                x=candles.index[-200:],
                open=candles['open'][-200:],
                high=candles['high'][-200:],
                low=candles['low'][-200:],
                close=candles['close'][-200:]
            )])

            last_n = 3
            highlight_candles = candles.iloc[-last_n:]
            pulse_base = 0.3 + 0.7 * ((time.time() % 1))

            for idx, row in highlight_candles.iterrows():
                ai_conf = signals['ai_confidence'].iloc[idx]
                intensity = min(max(pulse_base * ai_conf, 0.3), 1.0)

                if signals['buy_signal_final'].iloc[idx]:
                    color = f'rgba(0,255,0,{intensity})'
                    glow_color = f'rgba(0,255,0,{intensity*0.3})'
                    label_color = 'lime'
                elif signals['sell_signal_final'].iloc[idx]:
                    color = f'rgba(255,0,0,{intensity})'
                    glow_color = f'rgba(255,0,0,{intensity*0.3})'
                    label_color = 'red'
                else:
                    color = f'rgba(0,255,255,{intensity})'
                    glow_color = f'rgba(0,255,255,{intensity*0.2})'
                    label_color = 'cyan'

                fig.add_shape(type='rect', x0=idx - pd.Timedelta('0.5min'), x1=idx + pd.Timedelta('0.5min'),
                              y0=row['low'], y1=row['high'], fillcolor=color, line_width=0)

                fig.add_shape(type='rect', x0=idx - pd.Timedelta('0.55min'), x1=idx + pd.Timedelta('0.55min'),
                              y0=row['low']*0.998, y1=row['high']*1.002, fillcolor=glow_color, line_width=0)

                fig.add_trace(go.Scatter(x=[idx], y=[row['high']*1.01], text=[f'{ai_conf:.2f}'],
                                         mode='text', textfont=dict(color=label_color, size=10, family='Arial'),
                                         showlegend=False))

            st.plotly_chart(fig, use_container_width=True)

=====================

Heatmap Page

=====================

if page == 'Heatmap': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("AI Confidence Heatmap") # Placeholder table; connect real-time scanner data here data = pd.DataFrame({ 'Symbol': symbols, 'AI Confidence': [0.7,0.85,0.65,0.9] }) st.dataframe(data.style.background_gradient(cmap='Viridis'))

=====================

Slippage Metrics Page

=====================

if page == 'Slippage Metrics': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Slippage & Execution Metrics") # Placeholder table; integrate live slippage tracking data = pd.DataFrame({ 'Symbol': symbols, 'Expected Price': [100,200,300,400], 'Executed Price': [100.5,199.8,300.2,399.9], 'Slippage': [0.5,-0.2,0.2,-0.1] }) st.dataframe(data)
