# 教程：跑基准

```bash
python -m clmforge bench --n 200        # 五组基准
python -m clmforge speedup --n 500      # 延迟加速
python scripts/run_benchmarks.py        # 汇总（含延迟）
```

指标：accuracy（正确率）、avg_latency_ms（延迟）、fast_ratio（快路径占比）、
cache_hit_rate（缓存命中率）。
