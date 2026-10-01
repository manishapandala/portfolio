"""Validate the static portfolio's required structure and published project links."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "manisha_pandala_portfolio.html"
EXPECTED_REPOSITORIES = {
    "automated-reporting-workflow",
    "battery-anomaly-detection",
    "cyberguard-zero-trust",
    "demand-forecasting-backtest",
    "model-reliability-lab",
    "operational-data-quality",
    "semantic-search-similarity",
}


class PortfolioParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.hrefs.append(str(values["href"]))
        if tag == "h1":
            self.h1_count += 1


def main() -> None:
    text = PORTFOLIO.read_text(encoding="utf-8")
    parser = PortfolioParser()
    parser.feed(text)
    if parser.h1_count != 1:
        raise SystemExit(f"Expected exactly one h1, found {parser.h1_count}")
    if "TODO" in text or 'href=""' in text:
        raise SystemExit("Portfolio contains a placeholder or empty link")
    for repository in EXPECTED_REPOSITORIES:
        source = f"https://github.com/manishapandala/{repository}"
        live = f"https://manishapandala.github.io/{repository}/"
        if source not in parser.hrefs:
            raise SystemExit(f"Missing source link for {repository}")
        if live not in parser.hrefs:
            raise SystemExit(f"Missing live link for {repository}")
    print(f"Validated {len(EXPECTED_REPOSITORIES)} projects and {len(parser.hrefs)} links")


if __name__ == "__main__":
    main()
