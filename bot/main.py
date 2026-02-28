"""
main.py – Entry point for the Yeonkkachi AI trading bot.

Usage:
    python -m bot.main          # run continuously on a schedule
    python -m bot.main --once   # run one cycle and exit (useful for testing)

DISCLAIMER: This software is for RESEARCH AND EDUCATIONAL PURPOSES ONLY.
It is NOT financial advice.  The bot runs in paper-trading mode by default.
"""

from __future__ import annotations

import argparse
import time

import schedule

from bot.logger import get_logger
from bot.trading_logic import TradeSignal, execute_trade, load_trade_log
from bot.twitter_api import post_tweet

log = get_logger("main")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _format_trade_tweet(record: dict) -> str:
    return (
        f"[Yeonkkachi] {record['action']} {record['quantity']} {record['symbol']} "
        f"@ ${record['price']:.4f} (${record['usd_value']:.2f} USD) | "
        f"confidence={record['confidence']:.0%} | {record['reasoning']} "
        f"#AITrading #NotFinancialAdvice"
    )


# ---------------------------------------------------------------------------
# Main cycle
# ---------------------------------------------------------------------------


def run_cycle() -> None:
    """Execute one full analysis-and-trade cycle."""
    log.info("=== Starting trading cycle ===")

    # ------------------------------------------------------------------
    # 1. Gather signals (placeholder – replace with your model/strategy)
    # ------------------------------------------------------------------
    signal = TradeSignal(
        symbol="BTC/USD",
        action="BUY",
        confidence=0.72,
        reasoning="Momentum indicator crossed above 50-day MA",
    )
    log.info(f"Signal generated: {signal}")

    # ------------------------------------------------------------------
    # 2. Execute trade (paper-trading by default)
    # ------------------------------------------------------------------
    record = execute_trade(signal, price=65_000.00, quantity=0.001)

    # ------------------------------------------------------------------
    # 3. Announce on Twitter for transparency
    # ------------------------------------------------------------------
    if record:
        tweet_text = _format_trade_tweet(record.__dict__ if hasattr(record, "__dict__") else record)
        post_tweet(tweet_text)

    log.info("=== Trading cycle complete ===")


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


def start_scheduler(interval_minutes: int = 60) -> None:
    log.info(f"Scheduler started – cycle every {interval_minutes} minute(s).")
    schedule.every(interval_minutes).minutes.do(run_cycle)
    run_cycle()  # run immediately on start
    while True:
        schedule.run_pending()
        time.sleep(10)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yeonkkachi AI Trading Bot")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single cycle and exit instead of looping.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        metavar="MINUTES",
        help="How often to run the trading cycle (default: 60).",
    )
    args = parser.parse_args()

    if args.once:
        run_cycle()
    else:
        start_scheduler(interval_minutes=args.interval)
