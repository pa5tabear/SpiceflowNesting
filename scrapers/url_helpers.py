from __future__ import annotations
from pathlib import Path
from urllib.parse import urlencode

try:
    import yaml
except Exception:  # pragma: no cover - fallback when PyYAML missing
    yaml = None

CRITERIA_PATH = Path(__file__).resolve().parents[1] / "search_criteria.yaml"


def load_criteria(path: Path = CRITERIA_PATH) -> dict:
    if yaml:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    data: dict[str, object] = {}
    key = None
    for line in path.read_text().splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  -") and key:
            data.setdefault(key, []).append(line.split("-", 1)[1].strip())
            continue
        if ":" in line:
            key, val = [x.strip() for x in line.split(":", 1)]
            if not val:
                data[key] = []
            else:
                try:
                    data[key] = int(val)
                except ValueError:
                    try:
                        data[key] = float(val)
                    except ValueError:
                        data[key] = val
    return data


CRITERIA = load_criteria()


def build_craigslist_url() -> str:
    base = "https://annarbor.craigslist.org/search/apa"
    params = {}
    if CRITERIA.get("max_rent"):
        params["max_price"] = int(CRITERIA["max_rent"])
    if CRITERIA.get("min_beds"):
        params["min_bedrooms"] = int(CRITERIA["min_beds"])
    return f"{base}?{urlencode(params)}" if params else base


def build_zillow_url() -> str:
    base = "https://www.zillow.com/homes/for_rent/Ann-Arbor-MI_rb"
    parts = []
    if CRITERIA.get("min_beds"):
        parts.append(f"{int(CRITERIA['min_beds'])}-_beds")
    if CRITERIA.get("max_rent"):
        parts.append(f"0-{int(CRITERIA['max_rent'])}_price")
    return base + "/" + "/".join(parts) + "/" if parts else base + "/"
