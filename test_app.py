from app import human_readable_last_seen, fetch_users_last_seen
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

def test_human_readable_last_seen():
    now = datetime.utcnow()  # Use UTC time for 'now'
    timestamp_now = now.isoformat()
    timestamp_20s = (now - timedelta(seconds=20)).isoformat()
    timestamp_40s = (now - timedelta(seconds=40)).isoformat()
    timestamp_50m = (now - timedelta(minutes=50)).isoformat()
    timestamp_110m = (now - timedelta(minutes=110)).isoformat()
    timestamp_1day = (now - timedelta(days=1)).isoformat()
    timestamp_5days = (now - timedelta(days=5)).isoformat()
    timestamp_10days = (now - timedelta(days=10)).isoformat()

    assert human_readable_last_seen(timestamp_now, now) == "just now"
    assert human_readable_last_seen(timestamp_20s, now) == "just now"
    assert human_readable_last_seen(timestamp_40s, now) == "less than a minute ago"
    assert human_readable_last_seen(timestamp_50m, now) == "couple of minutes ago"
    assert human_readable_last_seen(timestamp_110m, now) == "hour ago"
    assert human_readable_last_seen(timestamp_1day, now) == "yesterday"
    assert human_readable_last_seen(timestamp_5days, now) == "this week"
    assert human_readable_last_seen(timestamp_10days, now) == "long time ago"
    assert human_readable_last_seen(None, now) == "Unknown"  # Test the null/None scenario

@patch('app.requests.get')
def test_fetch_users_last_seen(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"data": [{"nickname": "John", "lastSeenDate": "2023-09-28T12:00:00Z", "isOnline": True}]}
    mock_get.return_value = mock_response

    result = fetch_users_last_seen()
    assert result == {"data": [{"nickname": "John", "lastSeenDate": "2023-09-28T12:00:00Z", "isOnline": True}]}
