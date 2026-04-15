from datetime import datetime, timezone, timedelta
from aggregation import aggregate_poi_wait_time, WaitSignal

def test_ttl_exclusion():
    now = datetime.now(timezone.utc)
    
    # 20 mins old -> should be dropped
    stale_signal = WaitSignal(waitMinutes=30, submitterRole="attendee", createdAt=now - timedelta(minutes=20))
    # 5 mins old -> should be kept
    fresh_signal = WaitSignal(waitMinutes=10, submitterRole="attendee", createdAt=now - timedelta(minutes=5))
    
    result = aggregate_poi_wait_time([stale_signal, fresh_signal], current_time=now)
    assert result["currentWaitMinutes"] == 10
    assert result["isStaffOverride"] is False

def test_time_decay_behavior():
    now = datetime.now(timezone.utc)
    
    # Almost expired signal (weight ~0.1), pulling toward 30m
    stale = WaitSignal(waitMinutes=30, submitterRole="attendee", createdAt=now - timedelta(minutes=14, seconds=30))
    # Brand new signal (weight 1.0), pulling toward 5m
    fresh = WaitSignal(waitMinutes=5, submitterRole="attendee", createdAt=now)
    
    result = aggregate_poi_wait_time([stale, fresh], current_time=now)
    
    # The outcome heavily favors the 5m signal due to freshness weight
    assert result["currentWaitMinutes"] < 10
    assert isinstance(result["currentWaitMinutes"], int)
    assert 0.0 <= result["confidenceScore"] <= 1.0

def test_confidence_behavior_deterministic():
    now = datetime.now(timezone.utc)
    
    # One single signal should give partial confidence
    one_signal = WaitSignal(waitMinutes=10, submitterRole="attendee", createdAt=now)
    result_low = aggregate_poi_wait_time([one_signal], current_time=now)
    assert 0.0 < result_low["confidenceScore"] < 1.0
    
    # Three identical fresh signals = weight 3.0 -> triggers 100% confidence threshold (1.0)
    three_signals = [WaitSignal(waitMinutes=10, submitterRole="attendee", createdAt=now) for _ in range(3)]
    result_high = aggregate_poi_wait_time(three_signals, current_time=now)
    assert result_high["confidenceScore"] == 1.0

def test_staff_override_behavior():
    now = datetime.now(timezone.utc)
    
    # Attendee says 50m wait
    attendee = WaitSignal(waitMinutes=50, submitterRole="attendee", createdAt=now)
    # Staff confirms 10m wait
    staff = WaitSignal(waitMinutes=10, submitterRole="staff", createdAt=now)
    
    result = aggregate_poi_wait_time([attendee, staff], current_time=now)
    
    # Result should completely mirror the staff's exact parameters
    assert result["currentWaitMinutes"] == 10
    assert result["confidenceScore"] == 1.0
    assert result["isStaffOverride"] is True
