import scrapers.url_helpers as u


def test_build_craigslist_url(monkeypatch):
    monkeypatch.setattr(u, "CRITERIA", {"max_rent": 1500, "min_beds": 2})
    url = u.build_craigslist_url()
    assert "max_price=1500" in url
    assert "min_bedrooms=2" in url


def test_build_zillow_url(monkeypatch):
    monkeypatch.setattr(u, "CRITERIA", {"max_rent": 2000, "min_beds": 1})
    url = u.build_zillow_url()
    assert url.endswith("/1-_beds/0-2000_price/")
