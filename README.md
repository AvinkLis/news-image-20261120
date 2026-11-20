# The Daily Picture — Friday, 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/AvinkLis/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/AvinkLis/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page that sums up 20 November 2026's world news in a
single image — drawn entirely in code with Pillow, no photographs, no
external assets. Entry for the
[make.fun news-image-20261120 competition](https://make.fun/bounty/news-image-20261120).

## The stories on the page

- **Lead — The Hague:** The UN's International Court of Justice rules
  Myanmar committed genocide against the Rohingya — the court's first
  such finding against a state — over the 2017 military campaign in
  Rakhine. Rohingya refugees in Bangladesh cheered the verdict.
- **Second lead — Kyiv:** Russian ballistic missiles rock Kyiv overnight,
  retaliation after Ukraine hit the Crimean Bridge a third time in four
  days. Air alerts across the capital; the Austrian and Dutch embassies
  were damaged.
- **Riyadh:** A Houthi missile hits Riyadh's tallest tower; strikes on
  four Saudi targets.
- **Genoa:** Unidentified drones shut the airport; flights suspended.
- **Strait of Hormuz:** A tanker catches fire after hitting a mine east
  of the strait.
- **India:** More than 80,000 people evacuated as Tropical Storm Dana
  approaches.
- **Lebanon:** An Israeli airstrike hits a Hezbollah missile facility in
  eastern Lebanon.
- **Markets:** Anthropic's record $81.3 billion IPO — shares close up 17%
  on debut, briefly valuing the firm past $2 trillion — while Wall Street
  falls for a fifth straight day (S&P 500 down 2.0%).
- **COP31:** The draft climate deal drops any mention of fossil fuels,
  drawing an outcry.

## Run it

Requires Python 3 and Pillow (standard library + Pillow only):

```bash
python3 main.py
```

This draws `entry.png` (1024×1024) in the repository directory and copies
it deterministically to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as
`entry.png`. Two runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
