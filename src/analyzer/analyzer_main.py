# src/analyzer/analyzer_main.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer.return_generator import load_signals, add_forward_returns

df = load_signals()
df = add_forward_returns(df)

# Show last few rows of returns
print(df[["timestamp", "btc_price", "return_1h", "return_2h", "return_4h"]].tail(10))

from analyzer.rule_tester import test_rule

rule = "score > 0.0"  # adjust as needed
result = test_rule(df, rule, return_col="return_1h", threshold=0.001)

print("\n📊 Rule Test Result:")
for k, v in result.items():
    print(f"{k}: {v}")
