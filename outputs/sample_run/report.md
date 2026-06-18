# Lab 16 Benchmark Report

## Metadata
- Dataset: hotpot_test.json
- Mode: mock
- Records: 200
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.93 | 0.95 | 0.02 |
| Avg attempts | 1 | 1.13 | 0.13 |
| Avg token estimate | 1828.85 | 2405.96 | 577.11 |
| Avg latency (ms) | 5590.45 | 14514 | 8923.55 |

## Failure modes
```json
{
  "react": {
    "none": 93,
    "wrong_final_answer": 7
  },
  "reflexion": {
    "none": 95,
    "wrong_final_answer": 5
  }
}
```

## Extensions implemented
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding

## Discussion
Reflexion helps when the first attempt stops after the first hop or drifts to a wrong second-hop entity. The tradeoff is higher attempts, token cost, and latency. In a real report, students should explain when the reflection memory was useful, which failure modes remained, and whether evaluator quality limited gains.
