def calculate_highest_iv_calls(calls_data):
    """Call opsiyonları için en yüksek implied volatiliteyi hesaplar."""
    if calls_data is None or len(calls_data) == 0:
        return 0
    return calls_data['implied_volatility'].max()

def calculate_lowest_iv_puts(puts_data):
    """Put opsiyonları için en düşük implied volatiliteyi hesaplar."""
    if puts_data is None or len(puts_data) == 0:
        return 0
    return puts_data['implied_volatility'].min()

def filter_options_data(options_data, condition):
    """Belirtilen koşula göre opsiyon verilerini filtreler."""
    if options_data is None:
        return None
    return options_data[condition]

def format_percentage(value):
    """Bir değeri yüzde olarak iki ondalık basamakla biçimlendirir."""
    if value is None:
        return "N/A"
    return f"{value:.2f}%"

def format_currency(value):
    """Bir değeri para birimi olarak iki ondalık basamakla biçimlendirir."""
    if value is None:
        return "N/A"
    return f"${value:.2f}"

def format_contract_count(value):
    """Bir değeri virgüllü kontrat sayısı olarak biçimlendirir."""
    if value is None:
        return "N/A"
    return f"{int(value):,}"

def calculate_change_percentage(current, previous):
    """İki değer arasındaki yüzde değişimini hesaplar."""
    if previous == 0:
        return float('inf') if current > 0 else float('-inf') if current < 0 else 0
    return ((current - previous) / previous) * 100