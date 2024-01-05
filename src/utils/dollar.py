from cachetools import TTLCache
from pyDolarVenezuela import Monitor
from pyDolarVenezuela.pages import (
    Monitor as Page,
    ExchangeMonitor
)
from pyDolarVenezuela import (
    getdate,
    currency_converter
)

cache = TTLCache(ttl=240, maxsize=1024)

def get_value_dollar(key: str, provider: Page):
    if key not in cache:
        page_monitors = Monitor(provider, currency='USD')
        response = page_monitors.get_value_monitors()
    
        cache[key] = response
    return cache[key]