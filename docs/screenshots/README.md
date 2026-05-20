# Screenshots

Drop production-quality PNGs here. Names are referenced from the root [README](../../README.md).

| File | What to capture |
|---|---|
| `merchant-chat.png` | Assistant page mid-conversation, with a freshly generated payment card visible |
| `dashboard.png` | Dashboard with non-zero KPIs (run a few sample charges first) |
| `analytics.png` | Urgency + category bars populated, activity feed on the right |
| `payment-flow.png` | Single payment card showing link, WhatsApp draft, status badge, follow-up button |
| `escalation-alerts.png` | Payment(s) with the `escalation` badge + escalation activity events |

## Quick capture script

1. `docker compose up --build`
2. Open `http://localhost:3000`
3. Run the four suggestion chips on the Assistant page (creates varied payments).
4. Click *Mark paid* on one, *AI follow-up* on another.
5. Screenshot each tab at 1440×900 with the dock hidden.

Tip: macOS `Cmd+Shift+4 + Space` for clean window captures.
