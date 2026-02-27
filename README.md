# How to Scrape Google Trends Data with Python (Step-by-Step)

This repository is a **minimal, runnable tutorial** for scraping Google Trends data through the **Thordata Python SDK**.

You will learn how to:

- send a Google Trends request with one keyword,
- parse the API response,
- export clean data to CSV,
- quickly compare interest over time across locations.

By the end, you can run one command and get a ready-to-use file like `output/google_trends.csv`.

---

## 1. What You Will Build

A single script `scraper.py` that:

1. reads your API token from `.env`,
2. requests Google Trends data from Thordata SERP API (Google Trends engine),
3. normalizes rows from `trends_results`,
4. saves them to CSV.

Run example (you can paste this after finishing section 4 and 5):

```bash
python scraper.py --query "python" --date "today 12-m" --geo "US"
```

You will get a file like:

```text
output/google_trends.csv
```

---

## 2. Prerequisites

- Python 3.9+
- A Thordata account
- Your `THORDATA_SCRAPER_TOKEN` from the [Thordata Dashboard](https://dashboard.thordata.com/account-settings)

You can start with the **Dashboard trial** and test this tutorial with real requests using a live `THORDATA_SCRAPER_TOKEN`.

---

## 3. Project Structure

```text
how-to-scrape-google-trends/
├── .env.example
├── README.md
├── requirements.txt
└── scraper.py
```

After running the script, you will also get an `output/` folder with CSV results (created automatically the first time you run).

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies are intentionally minimal:

- `thordata-sdk`
- `python-dotenv`

---

## 5. Configure API Credentials

1. Copy `.env.example` to `.env`
2. Fill in your token

```env
THORDATA_SCRAPER_TOKEN=your_real_token_here
```

Do not commit `.env`.

---

## 6. First Run: Single Keyword, Single Country

Basic command (paste this in your terminal after activating the virtualenv, if any):

```bash
python scraper.py --query "python"
```

This uses the defaults:

- `geo` – empty (Worldwide)
- `date` – `today 12-m` (past 12 months)
- `hl` – `en`
- `data_type` – `TIMESERIES`
- `output` – `output/google_trends.csv`

You can also be explicit about all parameters:

```bash
python scraper.py \
  --query "python" \
  --geo "US" \
  --date "today 12-m" \
  --hl "en" \
  --data-type "TIMESERIES" \
  --output "output/google_trends.csv"
```

If successful, you should see logs like:

```text
Saved 53 rows to output/google_trends.csv
Requested data_type: TIMESERIES
API response data_type: TIMESERIES
Done.
```

---

## 7. Output Format (What the CSV Looks Like)

Generated CSV columns:

- `query` – the keyword you requested
- `date` – human-readable time bucket from API
- `timestamp` – Unix timestamp
- `value` – trend score (0-100)

Example rows (your exact dates and values will differ):

```text
query,date,timestamp,value
python,"Feb 23–Mar 1, 2025",1740268800,94
python,"Mar 2–8, 2025",1740873600,86
```

---

## 8. Parameters You Can Try (and Copy-Paste)

From Thordata Google Trends parameters, the most useful ones for this tutorial are:

- `q` via `--query` (required)
- `geo` via `--geo` (optional)
- `hl` via `--hl` (optional)
- `date` via `--date` (optional)
- `data_type` via `--data-type` (optional, keep `TIMESERIES` in this tutorial)

Common `date` values you can try:

- `now 1-H`
- `now 7-d`
- `today 1-m`
- `today 12-m`
- `today 5-y`

All of them work with the same script; only the time range of rows changes.

### Example: Long-term view (5 years)

```bash
python scraper.py --query "python" --date "today 5-y" --output "output/google_trends_5y.csv"
```

### Example: Short-term view (last 7 days)

```bash
python scraper.py --query "python" --date "now 7-d" --output "output/google_trends_7d.csv"
```

---

## 9. Compare Interest Across Locations (US vs India)

You can compare the same keyword across different `geo` values by running the script multiple times with different `--geo` options.

### Step 1: US data

```bash
python scraper.py \
  --query "python" \
  --geo "US" \
  --date "today 12-m" \
  --output "output/google_trends_us.csv"
```

### Step 2: India data

```bash
python scraper.py \
  --query "python" \
  --geo "India" \
  --date "today 12-m" \
  --output "output/google_trends_india.csv"
```

Both files have the same columns (`query,date,timestamp,value`) and the same time buckets. You can:

- open them in Excel/Sheets and create a chart for each country, or
- load them in a notebook with pandas and merge on `timestamp` to plot a single comparison chart.

This keeps the script minimal while still letting you do practical analysis.

---

## 10. Notes from Real API Testing

This tutorial is tested with real API calls using the live Thordata SERP API.

Current observed response shape includes:

- top-level `trends_results` list,
- metadata in `search_metadata`,
- request echo in `spider_parameter` (for example, `data_type`).

In practice there are more `data_type` options such as `GEO_MAP` or `RELATED_QUERIES`. To keep the repository simple and robust, this tutorial focuses on **TIMESERIES** export only, which is the most common starting point for dashboards and reporting.

---

## 11. Troubleshooting

### Missing token

If you see an error about `THORDATA_SCRAPER_TOKEN`, check `.env` and retry.

### Empty rows

Try a broader query or different time range:

```bash
python scraper.py --query "pizza" --date "today 5-y"
```

You can also temporarily remove `--geo` to fall back to Worldwide and see if that returns data.

### Non-UTF8 terminal issues on Windows

This script avoids special symbols in logs to prevent common encoding errors.

---

## 12. Why Thordata for Production Workflows

For one-off learning scripts, this repository intentionally stays minimal and close to the wire format of the API.

When moving to production, Thordata helps with:

- reliable scraping infrastructure that hides browser and proxy complexity,
- a unified API + SDK experience across Google, e-commerce, social, and custom scraping,
- Dashboard-based token, usage, and team management.

You can start from the Dashboard trial, validate your Google Trends flow with this repo, and only then decide what to automate and scale.

---

## License

MIT
