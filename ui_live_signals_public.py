import json
import streamlit as st
import time
import os

st.set_page_config(page_title="Live Sentiment Signals", layout="wide")

st.title("\U0001F4CA Live Crypto Sentiment Signals")
st.markdown("""
This dashboard displays live crypto sentiment.
""")

SIGNAL_COLORS = {
    "Strong Buy": "#27ae60",
    "Buy": "#2ecc71",
    "Hold": "#f1c40f",
    "Sell": "#e67e22",
    "Strong Sell": "#e74c3c"
}
CONFIDENCE_COLORS = {
    "High": "#27ae60",
    "Medium": "#f1c40f",
    "Low": "#e74c3c"
}

# Helper to load JSON safely
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# Main UI loop
def main():
    # Use absolute path to gpt_structured_response.json in the LiveChatFetcher folder
    json_path = os.path.join(os.path.dirname(__file__), "gpt_structured_response.json")
    last_data = None
    placeholder = st.empty()
    while True:
        data = load_json(json_path)
        if data != last_data:
            last_data = data
            with placeholder.container():
                st.subheader("Live Crypto Signals")
                # Partition by confidence (case-insensitive, exact match)
                high_conf = [f for f in data if f.get("confidence", "").strip().lower() == "high"]
                med_conf = [f for f in data if f.get("confidence", "").strip().lower() == "medium"]
                low_conf = [f for f in data if f.get("confidence", "").strip().lower() == "low"]
                def sort_key(fund_data):
                    pos = fund_data.get("positive_count", 0)
                    neg = fund_data.get("negative_count", 0)
                    return (-(pos - neg), -pos)
                # Show High Confidence in a horizontal row
                if high_conf:
                    st.markdown("<h2 style='color:#27ae60'>High Confidence</h2>", unsafe_allow_html=True)
                    cols = st.columns(len(high_conf))
                    for idx, fund_data in enumerate(sorted(high_conf, key=sort_key)):
                        with cols[idx]:
                            fund = fund_data.get("crypto", "?")
                            signal = fund_data.get("signal", "?")
                            confidence = fund_data.get("confidence", "?")
                            explanation = fund_data.get("explanation", "")
                            minute_candle = fund_data.get("1_minute_candlestick_signal", "")
                            safe_leverage = fund_data.get("safe_leverage_isolate_future_perpetual", "")
                            pos = fund_data.get("positive_count", 0)
                            neg = fund_data.get("negative_count", 0)
                            neu = fund_data.get("neutral_count", 0)
                            comments = fund_data.get("representative_opinions", [])
                            color = SIGNAL_COLORS.get(signal, "#bdc3c7")
                            conf_color = CONFIDENCE_COLORS.get(confidence, "#bdc3c7")
                            st.markdown(f"<div style='border:1px solid #27ae60;border-radius:8px;padding:12px;margin:4px;background:#f9fff9;min-width:260px;display:inline-block'>" +
                                f"<h4 style='color:{color}'>{fund}: {signal}</h4>" +
                                f"<span style='color:{conf_color};font-weight:bold'>Confidence: {confidence}</span><br>" +
                                f"<span style='font-size:13px'>{explanation}</span><br>" +
                                f"<b>Positive:</b> {pos} &nbsp;&nbsp; <b>Negative:</b> {neg} &nbsp;&nbsp; <b>Neutral:</b> {neu}<br> <b>1 minuite:</b> {minute_candle} &nbsp;&nbsp; <b>safe_leverage:</b> {safe_leverage} &nbsp;&nbsp;" +
                                "<b>Comments:</b><ul style='padding-left:18px'>" + ''.join([f"<li style='color:#555'>{c}</li>" for c in comments]) + "</ul>" +
                                "</div>", unsafe_allow_html=True)
                # Show Medium Confidence in a horizontal row
                if med_conf:
                    st.markdown("<h2 style='color:#f1c40f'>Medium Confidence</h2>", unsafe_allow_html=True)
                    cols = st.columns(len(med_conf))
                    for idx, fund_data in enumerate(sorted(med_conf, key=sort_key)):
                        with cols[idx]:
                            fund = fund_data.get("crypto", "?")
                            signal = fund_data.get("signal", "?")
                            confidence = fund_data.get("confidence", "?")
                            explanation = fund_data.get("explanation", "")
                            pos = fund_data.get("positive_count", 0)
                            neg = fund_data.get("negative_count", 0)
                            neu = fund_data.get("neutral_count", 0)
                            comments = fund_data.get("representative_opinions", [])
                            color = SIGNAL_COLORS.get(signal, "#bdc3c7")
                            conf_color = CONFIDENCE_COLORS.get(confidence, "#bdc3c7")
                            st.markdown(f"<div style='border:1px solid #f1c40f;border-radius:8px;padding:12px;margin:4px;background:#fffef9;min-width:260px;display:inline-block'>" +
                                f"<h4 style='color:{color}'>{fund}: {signal}</h4>" +
                                f"<span style='color:{conf_color};font-weight:bold'>Confidence: {confidence}</span><br>" +
                                f"<span style='font-size:13px'>{explanation}</span><br>" +
                                f"<b>Positive:</b> {pos} &nbsp;&nbsp; <b>Negative:</b> {neg} &nbsp;&nbsp; <b>Neutral:</b> {neu}<br>" +
                                "<b>Comments:</b><ul style='padding-left:18px'>" + ''.join([f"<li style='color:#555'>{c}</li>" for c in comments]) + "</ul>" +
                                "</div>", unsafe_allow_html=True)
                # Show Low Confidence in a horizontal row
                if low_conf:
                    st.markdown("<h2 style='color:#e74c3c'>Low Confidence</h2>", unsafe_allow_html=True)
                    cols = st.columns(len(low_conf))
                    for idx, fund_data in enumerate(sorted(low_conf, key=sort_key)):
                        with cols[idx]:
                            fund = fund_data.get("crypto", "?")
                            signal = fund_data.get("signal", "?")
                            confidence = fund_data.get("confidence", "?")
                            explanation = fund_data.get("explanation", "")
                            pos = fund_data.get("positive_count", 0)
                            neg = fund_data.get("negative_count", 0)
                            neu = fund_data.get("neutral_count", 0)
                            comments = fund_data.get("representative_opinions", [])
                            color = SIGNAL_COLORS.get(signal, "#bdc3c7")
                            conf_color = CONFIDENCE_COLORS.get(confidence, "#bdc3c7")
                            st.markdown(f"<div style='border:1px solid #e74c3c;border-radius:8px;padding:12px;margin:4px;background:#fff9f9;min-width:260px;display:inline-block'>" +
                                f"<h4 style='color:{color}'>{fund}: {signal}</h4>" +
                                f"<span style='color:{conf_color};font-weight:bold'>Confidence: {confidence}</span><br>" +
                                f"<span style='font-size:13px'>{explanation}</span><br>" +
                                f"<b>Positive:</b> {pos} &nbsp;&nbsp; <b>Negative:</b> {neg} &nbsp;&nbsp; <b>Neutral:</b> {neu}<br>" +
                                "<b>Comments:</b><ul style='padding-left:18px'>" + ''.join([f"<li style='color:#555'>{c}</li>" for c in comments]) + "</ul>" +
                                "</div>", unsafe_allow_html=True)
        time.sleep(5)

if __name__ == "__main__":
    main()
