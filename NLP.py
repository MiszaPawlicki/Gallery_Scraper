import re


def findPrices(price_elements):
    prices = []
    free_occurrences = []

    for element in price_elements:
        text = element.get_text(strip=True)

        # Check for "free" keyword
        if re.search(r'\bfree\b', text, re.IGNORECASE):
            free_occurrences.append(text)

        # Find prices following the pound symbol
        price_matches = re.findall(r'£\s*(\d+(\.\d+)?)', text)
        for price in price_matches:
            try:
                prices.append(float(price[0]))  # price[0] because re.findall returns tuples
            except ValueError:
                continue

    # Determine minimum and maximum prices
    if free_occurrences and not prices:
        min_price = 'free'
        max_price = 'free'
    elif prices:
        min_price = min(prices) if not free_occurrences else 'free'
        max_price = max(prices)
    else:
        min_price = 'Not listed'
        max_price = 'Not listed'

    return min_price, max_price


def findLocations(postcode_elements):
    for element in postcode_elements:
        text = element.get_text().strip()

        # Regular expression pattern to match UK postcodes in various formats
        postcode_pattern = r'[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}'

        # Find the first match of postcode pattern in the text
        postcode_match = re.search(postcode_pattern, text)
        if postcode_match:
            return postcode_match.group()

    return None

