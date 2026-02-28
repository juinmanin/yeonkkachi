# Privacy Policy

**Last updated: 2024-01-01**

## 1. Overview

The Yeonkkachi project ("we", "our", or "the project") is an open-source AI trading research
initiative. This Privacy Policy explains how we handle any information in the context of this
project.

## 2. Information We Collect

### 2.1 No Personal Data Collection

The Yeonkkachi trading bot itself does **not** collect, store, or process any personally
identifiable information (PII) about users or third parties.

### 2.2 Public Twitter / X Data

The bot interacts with the Twitter / X platform to:
- Post trade announcements from the project's own account.
- Fetch publicly available tweets for research purposes.

All data fetched from Twitter / X is subject to Twitter's own
[Privacy Policy](https://twitter.com/en/privacy).

### 2.3 Trade Logs

Trade activity is logged locally in the `data/` directory and published to Twitter / X for
transparency. These logs contain only market data (symbol, price, quantity, timestamp) and
contain no personal information.

## 3. How We Use Information

Any data collected is used solely for:
- Executing and logging paper trades.
- Publishing transparent trade announcements.
- Improving the trading research model.

## 4. Data Sharing

We do **not** sell, rent, or share any data with third parties for marketing purposes.
Trade logs are published publicly on Twitter / X and GitHub as part of our transparency
commitment.

## 5. Data Retention

Local trade log files are retained for a maximum of **30 days** by default (configurable via
`MAX_DRAWDOWN_PCT` and log rotation settings).

## 6. Security

We take reasonable precautions to protect API keys and other credentials. We strongly advise
all users to:
- Store secrets in a `.env` file that is excluded from version control via `.gitignore`.
- Rotate API keys regularly.
- Never commit credentials to any public repository.

## 7. Children's Privacy

This project is intended for researchers and adults. We do not knowingly collect data from
anyone under the age of 18.

## 8. Changes to This Policy

We may update this Privacy Policy from time to time. Changes will be reflected by the
"Last updated" date at the top of this document.

## 9. Contact

For questions about this Privacy Policy, please open an issue on the
[GitHub repository](https://github.com/juinmanin/yeonkkachi/issues).

---

*This document is provided for informational purposes only and does not constitute legal advice.*
