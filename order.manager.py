# order_manager.py - Order Management for Pawan Master Algo

import requests
import time
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

# =========================
# AngelOne Order Management
# =========================
def place_angelone_order(api_key, client_id, pin, totp, symbol, quantity, transaction_type, product_type='INTRADAY', order_type='MARKET'):
    try:
        # Initialize AngelOne API connection
        from SmartApi import SmartConnect
        import pyotp

        # Setup credentials
        smart = SmartConnect(api_key=api_key)
        totp = pyotp.TOTP(totp).now()
        session = smart.generateSession(client_id, pin, totp)
        auth_token = session["data"]["jwtToken"]

        # Place the order
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "transactiontype": transaction_type,
            "exchange": "NFO",
            "ordertype": order_type,
            "producttype": product_type,
            "quantity": quantity
        }
        response = smart.placeOrder(order_params)
        if response['status']:
            logging.info(f"Order placed successfully: {response}")
            return response
        else:
            logging.error(f"Order placement failed: {response}")
            return None
    except Exception as e:
        logging.error(f"Error in placing AngelOne order: {e}")
        return None

# =========================
# CoinSwitch Order Management
# =========================
def place_coinswitch_order(api_key, api_secret, symbol, quantity, transaction_type):
    try:
        # Setup CoinSwitch DMA API connection
        from cryptography.hazmat.primitives.asymmetric import ed25519

        base_url = "https://dma.coinswitch.co"
        epoch = str(int(time.time() * 1000))
        endpoint = "/v5/market/order"

        # Generate headers
        msg = f"{transaction_type}{symbol}{epoch}"
        pk = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(api_secret))
        sig = pk.sign(msg.encode()).hex()
        headers = {
            "X-AUTH-SIGNATURE": sig,
            "X-AUTH-APIKEY": api_key,
            "X-AUTH-EPOCH": epoch,
            "Content-Type": "application/json"
        }

        # Order payload
        order_payload = {
            "symbol": symbol,
            "quantity": quantity,
            "transactionType": transaction_type,
            "orderType": "MARKET"
        }

        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=order_payload)
        if response.status_code == 200:
            logging.info(f"CoinSwitch order placed: {response.json()}")
            return response.json()
        else:
            logging.error(f"CoinSwitch order failed: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error in placing CoinSwitch order: {e}")
        return None

# =========================
# Helper Function
# =========================
def place_order(api_type, **kwargs):
    if api_type == "angelone":
        return place_angelone_order(**kwargs)
    elif api_type == "coinswitch":
        return place_coinswitch_order(**kwargs)
    else:
        logging.error("Unsupported API type.")
        return None

# =========================
# Example Usage
# =========================
if __name__ == "__main__":
    # Example parameters (replace with actual values)
    api_type = "angelone"  # or "coinswitch"
    api_key = "YOUR_API_KEY"
    client_id = "YOUR_CLIENT_ID"
    pin = "YOUR_PIN"
    totp = "YOUR_TOTP_SECRET"
    symbol = "NIFTY21JUN15000CE"
    quantity = 1
    transaction_type = "BUY"

    # Place order
    response = place_order(api_type, api_key=api_key, client_id=client_id, pin=pin, totp=totp, symbol=symbol, quantity=quantity, transaction_type=transaction_type)
    if response:
        print("Order Response:", response)
    else:
        print("Order placement failed.")
