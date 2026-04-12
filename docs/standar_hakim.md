# Standar Hakim (Manager) - Source of Truth

Hakim final membaca 5 laporan dalam urutan:
1) Analysis (arah + struktur)
2) Core + Bot D (kualitas entry + posisi harga)
3) Market Intelligence (konteks makro/sentimen)
4) Risk (kelayakan eksekusi)

Jika data inti kurang/konflik -> HOLD.

## Field wajib yang harus dipenuhi 5 bot

### analysis
- signal, confidence, trend, market_structure, regime, candle_anatomy, volume_profile, key_levels, reasoning

### core
- signal, confidence, risk_reward, entry_quality, fakeout_risk, reasoning

### bot_d_position
- signal, confidence, price_position, entry_zone, wick_signal, reasoning

### market_intelligence
- sentiment, context_score, market_condition, funding, data_stale, reasoning

### risk
- approved, veto, risk_level, risk_score, position_size, entry, stop_loss, take_profit, reasoning

## Output final Hakim
- signal, confidence, entry, stop_loss, take_profit, position_size, reasoning
