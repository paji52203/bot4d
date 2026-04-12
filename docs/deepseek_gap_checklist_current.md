# Gap Checklist (Current Runtime Observation)

## Confirmed risks found in logs
- Prompt parser sempat gagal (SYSTEM_PROMPT terbaca "'''") -> FIXED via config_loader multiline parser.
- Setelah fix parser, perlu verifikasi 1-2 siklus untuk pastikan semua agent benar-benar output sesuai spec baru.

## Potential data gaps to monitor in live cycle
- analysis.candle_anatomy missing/null
- bot_d_position.wick_signal missing/null
- market_intelligence.context_score/funding missing
- core.risk_reward/entry_quality/fakeout_risk missing
- risk.approved/veto/risk_score/position_size missing

## Decision gate
Jika salah satu field kritis missing -> HOLD + reason `incomplete_or_invalid_reports`.
