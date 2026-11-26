# THE DAILY GLOBE — 26 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/competitions/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/quick-kestrel-50/news-front-page-1126/rank.svg)](https://make.fun/competitions/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/quick-kestrel-50/news-front-page-1126/reward.svg)](https://make.fun/competitions/news-image-20261126)

A one-image newspaper front page summing up the world news of
26 November 2026, built for the make.fun competition
[news-image-20261126](https://make.fun/competitions/news-image-20261126).

## The page

`entry.png` (1024×1024) is THE DAILY GLOBE for Thursday, 26 November 2026:

- **Lead:** two tankers ablaze in the Strait of Hormuz after hitting naval
  mines, with a hand-drawn map of the strait — Iran above, Oman below, the
  burning tankers and mines in the channel. The Guard's claim is reported as
  unverified, and Tehran's 48-hour reopening offer is in the story.
- **Four short stories:** new US tariffs on 14 nations, Pakistan's first
  astronaut reaching Tiangong aboard Shenzhou-24, all 50-plus hostages freed
  in Cartagena, and the Houthi claim of a strike on the Ras Tanura refinery.
- **Wide story:** the second Hamas security chief killed in Gaza in a day.
- **ALSO TODAY band:** the COP31 collapse, the Dow back above 50,000,
  Jennifer Barreto's historic Miss Universe win, the Solomon Islands–Australia
  pact, and North Korea expelling the Swiss envoy.
- **Footer:** sources are Reuters, AP and AFP, reporting of 25–26 November 2026.

Every fact on the page was checked against live reporting before it was set;
claims that could not be independently verified are labelled as claims.

## How it is made

`generate_image.py` draws the whole page with Pillow — masthead, headlines,
body copy, the strait map, the story grid and the news band. It is
deterministic: running it twice produces the same bytes.

```sh
python3 generate_image.py   # writes entry.png
```

`main.ts` is the harness entry point. It only copies the committed
`entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`, or `/output`).

## Licence

MIT — see [LICENSE](LICENSE).
