# Security Policy

## Reporting a vulnerability

The CS2 Skin Price Sniper holds Steam session cookies and marketplace API keys.
Please report suspected vulnerabilities privately to security@cs2sniper.local.

Do not open public issues for:

- Session/token leakage in logs
- Arbitrary code execution via crafted listing payloads
- Bypass of the buy-confirmation guard

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| < 0.6   | no        |

## Handling credentials

All marketplace credentials live in `.env` and are loaded via
`cs2_sniper/config/settings.py`. Never log raw tokens — use
`utils.redaction.mask_secret()`.