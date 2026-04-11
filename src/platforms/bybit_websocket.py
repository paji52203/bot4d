import logging
import threading
import time
from typing import Optional, Dict, Any
from pybit.unified_trading import WebSocket

class BybitWebSocketManager:
    """
    Manages real-time data from Bybit V5 WebSocket.
    Focuses on the "trade" topic to provide the absolute latest market price.
    Includes automatic reconnection with exponential backoff.
    """
    
    def __init__(self, logger: logging.Logger, symbol: str = "BTCUSDT", testnet: bool = False):
        self.logger = logger
        self.symbol = symbol.replace("/", "").split(":")[0]  # Convert BTC/USDT:USDT to BTCUSDT
        self.testnet = testnet
        
        self.latest_price: Optional[float] = None
        self.last_side: Optional[str] = None
        self.last_tick_direction: Optional[str] = None
        self._lock = threading.Lock()
        
        self.ws: Optional[WebSocket] = None
        self._active = False
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 10
        self._reconnect_delay = 5  # seconds
        self._reconnect_thread: Optional[threading.Thread] = None

    def start(self):
        """Start the WebSocket connection and subscribe to trades."""
        if self._active:
            return
            
        self._active = True
        self._reconnect_thread = threading.Thread(target=self._run_connection, daemon=True)
        self._reconnect_thread.start()

    def _run_connection(self):
        """Main connection loop with reconnection logic."""
        while self._active:
            try:
                self._connect()
                if self.ws:
                    # Keep alive - check connection periodically
                    while self._active and self.ws:
                        time.sleep(1)
            except Exception as e:
                if not self._active:
                    break
                self.logger.error(f"WebSocket connection error: {e}")
                self._reconnect_attempts += 1
                if self._reconnect_attempts >= self._max_reconnect_attempts:
                    self.logger.error(f"Max reconnection attempts ({self._max_reconnect_attempts}) reached")
                    break
                delay = self._reconnect_delay * (2 ** (self._reconnect_attempts - 1))
                self.logger.info(f"Attempting reconnect in {delay}s (attempt {self._reconnect_attempts}/{self._max_reconnect_attempts})")
                time.sleep(delay)

    def _connect(self):
        """Establish WebSocket connection."""
        try:
            self.logger.info(f"Starting Bybit WebSocket for {self.symbol}...")
            self.ws = WebSocket(
                testnet=self.testnet,
                channel_type="linear",
                domain="bytick"
            )
            
            self.ws.trade_stream(
                symbol=self.symbol,
                callback=self._handle_message
            )
            self._reconnect_attempts = 0  # Reset on successful connection
            self.logger.info(f"Subscribed to trade stream for {self.symbol}")
        except Exception as e:
            self.logger.error(f"Failed to start Bybit WebSocket: {e}")
            raise

    def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming trade messages from Bybit V5."""
        try:
            data_list = message.get("data", [])
            if not data_list:
                return
                
            latest_trade = data_list[-1]
            
            if latest_trade.get("BT", False):
                return

            with self._lock:
                self.latest_price = float(latest_trade.get("p", self.latest_price))
                self.last_side = latest_trade.get("S")
                self.last_tick_direction = latest_trade.get("L")
                
        except Exception as e:
            self.logger.error(f"Error processing Bybit WS message: {e}")

    def get_latest_price(self) -> Optional[float]:
        """Thread-safe access to the latest trade price."""
        with self._lock:
            return self.latest_price

    def stop(self):
        """Stop the WebSocket connection and cleanup."""
        self.logger.info("Stopping Bybit WebSocket...")
        self._active = False
        
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            self._reconnect_thread.join(timeout=5)
        
        if self.ws:
            try:
                self.ws.exit()
                self.logger.info("Bybit WebSocket successfully exited.")
            except Exception as e:
                self.logger.error(f"Error stopping Bybit WebSocket: {e}")
        
        self.ws = None
