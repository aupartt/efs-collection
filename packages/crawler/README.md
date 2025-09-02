## Web Crawler for Event Data Collection

A Python-based async crawler that extracts structured event information from specified URLs.

### Features
- Async scraping for efficient data collection
- Structured data output using Pydantic models
- Date parsing and normalization
- Slot availability tracking

### Installation
```bash
uv sync
```

### Usage
```python
import asyncio
from crawler import get_event_data

urls = [
    "https://efs.link/FNh76",
    "https://efs.link/RE2rS"
]

async def main():
    results = await get_event_data(urls)
    # Process results...

asyncio.run(main())
```

### Data Format
The crawler returns a list of `EventCollection` objects with this structure:
```json
[
    {
        "url": "https://efs.link/RE2rS",
        "events": [
            {
                "date": "2025-10-13",
                "slots": 86,
                "type": "blood",
                "schedules": {
                    "12h00": 1,
                    "12h05": 2,
                    // ... more time slots
                }
            }
        ]
    }
]
```

### Key Components
- `get_event_data()`: Main entry point for crawling with parameters:
  - `urls`: list[str] - URLs to crawl
  - `max_requests_per_crawl`: int = 10 - Maximum concurrent requests
  - `headless`: bool = True - Run browser in headless mode
  - `browser_type`: str = "firefox" - Browser to use ("firefox"|"chrome")
  - `keep_alive`: bool = False - Keep browser open after crawling (WIP)
- `Event`/`LocationEvents`: Data models (crawler/models.py)

