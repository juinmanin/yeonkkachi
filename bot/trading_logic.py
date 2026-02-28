"""
trading_logic.py – Core trading strategy and risk management for Yeonkkachi.

DISCLAIMER: This software is for RESEARCH AND EDUCATIONAL PURPOSES ONLY.
It is NOT financial advice.  Use at your own risk.

Responsibilities:
- Evaluate market signals and decide whether to enter/exit a position.
- Enforce hard risk limits (max drawdown, position sizing).
- Emit structured trade log entries consumed by main.py.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Optional

from bot.logger import get_logger

log = get_logger("trading_logic")

# ---------------------------------------------------------------------------
# Configuration – override via environment variables or a config file.
# ---------------------------------------------------------------------------

MAX_POSITION_SIZE_USD: float = float(os.getenv("MAX_POSITION_SIZE_USD", "100.0"))
MAX_DRAWDOWN_PCT: float = float(os.getenv("MAX_DRAWDOWN_PCT", "5.0"))
TRADE_LOG_PATH: str = os.getenv(
    "TRADE_LOG_PATH",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "trade_log.json"),
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class TradeSignal:
    symbol: str
    action: str          # "BUY" | "SELL" | "HOLD"
    confidence: float    # 0.0 – 1.0
    reasoning: str = ""


@dataclass
class TradeRecord:
    timestamp: str
    symbol: str
    action: str
    quantity: float
    price: float
    usd_value: float
    confidence: float
    reasoning: str
    status: str = "EXECUTED"
    tags: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Risk checks
# ---------------------------------------------------------------------------


def _check_position_size(usd_value: float) -> bool:
    if usd_value > MAX_POSITION_SIZE_USD:
        log.warning(
            f"Position size ${usd_value:.2f} exceeds max ${MAX_POSITION_SIZE_USD:.2f} – trade rejected."
        )
        return False
    return True


# ---------------------------------------------------------------------------
# Trade execution (simulated / paper trading)
# ---------------------------------------------------------------------------


def execute_trade(signal: TradeSignal, price: float, quantity: float) -> Optional[TradeRecord]:
    """
    Validate *signal* against risk limits and record it.

    In paper-trading mode no real orders are placed.  Replace this function
    body with your broker's SDK calls to go live.
    """
    usd_value = price * quantity

    if signal.action == "HOLD":
        log.info(f"Signal for {signal.symbol} is HOLD – no trade executed.")
        return None

    if not _check_position_size(usd_value):
        return None

    record = TradeRecord(
        timestamp=datetime.now(timezone.utc).isoformat(),
        symbol=signal.symbol,
        action=signal.action,
        quantity=quantity,
        price=price,
        usd_value=usd_value,
        confidence=signal.confidence,
        reasoning=signal.reasoning,
        tags=["paper-trade"],
    )

    _append_trade_log(record)
    log.info(
        f"{record.action} {record.quantity} {record.symbol} @ ${record.price:.4f} "
        f"(USD {record.usd_value:.2f}) | confidence={record.confidence:.2f}"
    )
    return record


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def _append_trade_log(record: TradeRecord) -> None:
    """Append *record* to the JSON-lines trade log."""
    os.makedirs(os.path.dirname(TRADE_LOG_PATH), exist_ok=True)
    with open(TRADE_LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record)) + "\n")


def load_trade_log() -> list[dict]:
    """Return all trade records from the log file as a list of dicts."""
    if not os.path.exists(TRADE_LOG_PATH):
        return []
    records = []
    with open(TRADE_LOG_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
