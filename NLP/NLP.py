from dateutil import parser
from datetime import datetime, timedelta
import parsedatetime as pdt
import re

cal = pdt.Calendar()

from dateutil import parser
from datetime import datetime
import parsedatetime as pdt
import re

cal = pdt.Calendar()


def parseDateString(time_string):
    try:
        # Check for date ranges
        if '–' in time_string or '-' in time_string:
            date_parts = re.split(r'\s*[-–]\s*', time_string)
            if len(date_parts) == 2:
                start_date = parser.parse(date_parts[0])
                end_date = parser.parse(date_parts[1])
                return start_date, end_date
            else:
                return None, None

        # Check for relative dates like "Third Tuesday of the month at 10.00–11.00"
        if 'of the month' in time_string:
            event_parts = re.split(r'\s+at\s+', time_string, 1)
            date_str = event_parts[0]
            time_str = event_parts[1] if len(event_parts) > 1 else ''

            time_range = re.split(r'\s*[-–]\s*', time_str)
            if len(time_range) == 2:
                start_time = parser.parse(time_range[0]).time()
                end_time = parser.parse(time_range[1]).time()
            else:
                return None, None

            time_struct, parse_status = cal.parse(date_str)
            if parse_status == 1:
                start_date = datetime(*time_struct[:6])
                end_date = start_date.replace(hour=end_time.hour, minute=end_time.minute)
                start_date = start_date.replace(hour=start_time.hour, minute=start_time.minute)
                return start_date, end_date
            else:
                return None, None

        # General case
        parsed_date = parser.parse(time_string)
        return parsed_date, parsed_date
    except Exception as e:
        return None, None


def main():
    # Test the function with the provided date strings
    date_test_strings = [
        'July 12th',
        '12th of July',
        '12/7/24',
        '12/07/2024',
        'Thursday, 12th of July',
        '29 May 2024 – 26 January 2025',
        'Third Tuesday of the month at 10.00–11.00'
    ]

    parsed_dates = [parseDateString(date_str) for date_str in date_test_strings]
    for date_str, parsed_date in zip(date_test_strings, parsed_dates):
        print(f"Original: {date_str} -> Parsed: {parsed_date}")


if __name__ == "__main__":
    main()