# DeepSeek Decision Input Spec v1 (Source of Truth)

## Tujuan
DeepSeek adalah **final judge**. Semua data untuk keputusan BUY/SELL/HOLD harus memenuhi kontrak ini.

## Urutan Evaluasi DeepSeek (WAJIB)
1. **Direction Context** (Analysis)
2. **Entry Quality** (Core + Bot D Position)
3. **Macro/Flow Context** (Market Intelligence)
4. **Execution Safety** (Risk)

Jika salah satu blok kritis tidak valid/kurang -> default **HOLD**.

---

## A) Required Fields per Block

### 1) Analysis (Direction Context)
- signal
- confidence
- trend
- market_structure
- regime
- candle_anatomy
- volume_profile
- key_levels
- reasoning

### 2) Core (Entry Quality)
- signal
- confidence
- risk_reward
- entry_quality
- fakeout_risk
- reasoning

### 3) Bot D Position (Price/Level Reaction)
- signal
- confidence
- price_position
- entry_zone
- wick_signal
- reasoning

### 4) Market Intelligence (Macro/Flow Context)
- sentiment
- context_score
- market_condition
- funding
- data_stale
- reasoning

### 5) Risk (Execution Safety)
- approved
- veto
- risk_level
- risk_score
- position_size
- entry
- stop_loss
- take_profit
- reasoning

---

## B) DeepSeek Final Output (Fixed)
- signal (BUY|SELL|HOLD)
- confidence (0-100)
- entry
- stop_loss
- take_profit
- position_size
- reasoning

---

## C) Acceptance Rules
- Semua required field tersedia dan type valid.
- Data tidak stale untuk market-intel (`data_stale=false`) kecuali explicit degrade mode.
- Jika conflict keras antar blok (mis. Analysis BUY vs Risk veto=true), final harus HOLD.
