"""Minimal Google Trends scraper tutorial using Thordata Python SDK."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from thordata import ThordataClient, load_env_file


def build_client() -> ThordataClient:
    """Create an authenticated Thordata client from environment variables."""
    load_dotenv()
    load_env_file()

    token = os.getenv("THORDATA_SCRAPER_TOKEN")
    if not token:
        raise ValueError(
            "Missing THORDATA_SCRAPER_TOKEN. Add it to .env or your system environment."
        )

    return ThordataClient(scraper_token=token)


def fetch_trends(
    client: ThordataClient,
    query: str,
    geo: str | None,
    date: str,
    hl: str,
    data_type: str,
) -> dict[str, Any]:
    """Send one Google Trends request via SERP API."""
    extra_params: dict[str, Any] = {
        "data_type": data_type,
        "date": date,
        "hl": hl,
    }

    if geo:
        extra_params["geo"] = geo

    # Use the high-level Google namespace for clarity.
    # This maps to engine="google_trends" under the hood.
    return client.serp.google.trends(query, **extra_params)


def normalize_timeseries_rows(response: dict[str, Any], query: str) -> list[dict[str, Any]]:
    """Normalize TIMESERIES Google Trends response into CSV-ready rows.

    Based on real API tests, the payload is currently returned in `trends_results` with fields
    like `date`, `timestamp`, and `value`.
    """
    rows: list[dict[str, Any]] = []
    trends_results = response.get("trends_results", [])

    if not isinstance(trends_results, list):
        return rows

    for item in trends_results:
        if not isinstance(item, dict):
            continue

        raw_value = item.get("value")
        try:
            value = int(str(raw_value).replace(",", "")) if raw_value is not None else None
        except ValueError:
            value = None

        rows.append(
            {
                "query": query,
                "date": item.get("date", ""),
                "timestamp": item.get("timestamp", ""),
                "value": value,
            }
        )

    return rows


def save_rows_to_csv(rows: list[dict[str, Any]], output_file: Path) -> None:
    """Write normalized rows to CSV."""
    if not rows:
        # Nothing to write; avoid creating empty files silently.
        raise RuntimeError("No rows to save. Nothing was written to disk.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Use keys from the first row to keep this helper reusable
    fieldnames = list(rows[0].keys())

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape Google Trends data with Thordata and export to CSV."
    )
    parser.add_argument(
        "--query",
        default="python",
        help="Search query, for example: python or artificial intelligence",
    )
    parser.add_argument(
        "--geo",
        default="",
        help="Optional location, for example: US, CN, India",
    )
    parser.add_argument(
        "--date",
        default="today 12-m",
        help='Date range, for example: "today 12-m", "today 5-y", "now 7-d"',
    )
    parser.add_argument(
        "--hl",
        default="en",
        help="Interface language, for example: en, es, zh-CN",
    )
    parser.add_argument(
        "--data-type",
        default="TIMESERIES",
        help="Google Trends data_type, default TIMESERIES",
    )
    parser.add_argument(
        "--output",
        default="output/google_trends.csv",
        help="Output CSV path",
    )

    args = parser.parse_args()

    client = build_client()
    response = fetch_trends(
        client=client,
        query=args.query,
        geo=args.geo or None,
        date=args.date,
        hl=args.hl,
        data_type=args.data_type,
    )

    rows = normalize_timeseries_rows(response=response, query=args.query)

    if not rows:
        metadata = response.get("search_metadata", {})
        status = metadata.get("status", "unknown")
        raise RuntimeError(
            "No trend rows returned. API status: {status}. "
            "Try a different query/date/geo combination."
        )

    output_path = Path(args.output)
    save_rows_to_csv(rows=rows, output_file=output_path)

    spider_params = response.get("spider_parameter", {})
    requested_data_type = args.data_type
    actual_data_type = spider_params.get("data_type")

    print(f"Saved {len(rows)} rows to {output_path}")
    print(f"Requested data_type: {requested_data_type}")
    print(f"API response data_type: {actual_data_type}")
    print("Done.")


if __name__ == "__main__":
    main()
