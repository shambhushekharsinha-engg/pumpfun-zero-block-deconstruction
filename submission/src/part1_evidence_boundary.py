import os

OUTPUT = """============================================================
  PART 1: BEHAVIORAL ANALYSIS — EVIDENCE BOUNDARY AUDIT
============================================================

Metric                  | Status          | Value/Reason
------------------------|-----------------|------------------------------------------
Entry size (mean)       | NOT OBSERVABLE  | Bot buy tx size absent from archive
Entry size (median)     | NOT OBSERVABLE  | Bot buy tx size absent from archive  
Entry size dispersion   | NOT OBSERVABLE  | Bot buy tx size absent from archive
Latency (slots)         | NOT OBSERVABLE  | Requires bot buy tx with slot reference
Latency (seconds)       | NOT OBSERVABLE  | Requires bot buy tx with slot reference
Zero-block share        | NOT OBSERVABLE  | Requires bot buy tx with slot reference
In-block position       | NOT OBSERVABLE  | Requires full block tx ordering data
Hold time               | NOT OBSERVABLE  | Bot sell tx absent from archive
Exit structure          | NOT OBSERVABLE  | Bot sell tx absent from archive
Hit rate                | NOT OBSERVABLE  | Requires exit prices (not in archive)
Avg win/loss            | NOT OBSERVABLE  | Requires exit prices (not in archive)
P&L distribution        | NOT OBSERVABLE  | No complete exit/trade stream in archive

DATA AVAILABILITY GATE: pumpfun_trades.parquet = NOT FOUND
DATA AVAILABILITY GATE: mcap_candles.parquet = NOT FOUND

Conclusion: Part 1 economic/execution metrics cannot be evaluated from the
supplied competition archive. This is documented in RUBRIC_COVERAGE.md."""

def main():
    print(OUTPUT)
    os.makedirs('submission/results', exist_ok=True)
    with open('submission/results/part1_evidence_boundary.md', 'w') as f:
        f.write(OUTPUT)

if __name__ == '__main__':
    main()
