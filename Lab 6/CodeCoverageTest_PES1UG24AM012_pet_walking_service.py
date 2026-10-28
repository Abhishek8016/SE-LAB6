import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars

def test_single_standard_30_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"

def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_walking_routes("not_a_list", 5.0)
    with pytest.raises(ValueError):
        process_walking_routes([], -1.0)

def test_route_unconfirmed_and_invalid_session():
    routes = [
        {"route_confirmed": False},
        {
            "route_confirmed": True,
            "session_type": "invalid_session",
            "walks": [{"num_pets": 2}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"

def test_session_types_and_walk_branches():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": True,
            "walks": [
                {"num_pets": 0},
                {"num_pets": 2, "aggression_alert": True, "needs_meds": True},
            ]
        },
        {
            "route_confirmed": True,
            "session_type": "express_15",
            "is_weekend": False,
            "walks": [
                {"num_pets": 4, "aggression_alert": False, "needs_meds": True},
                {"num_pets": 2, "aggression_alert": False, "needs_meds": False}
            ]
        }
    ]
    result = process_walking_routes(routes, 10.0)
    assert result["status"] == "COMPLETED"

def test_incident_audit_status():
    routes = [
        {"route_confirmed": True, "session_type": "inv_1", "walks": []},
        {"route_confirmed": True, "session_type": "inv_2", "walks": []},
        {"route_confirmed": True, "session_type": "inv_3", "walks": []},
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "walks": [{"num_pets": 0}, {"num_pets": -1}]
        }
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["status"] == "INCIDENT_AUDIT"

def test_inspect_gps_collars_branches():
    assert inspect_gps_collars([]) == "NO_DATA"
    assert inspect_gps_collars([[25, 10, 10]]) == "LOST_SIGNAL_ALERT"
    assert inspect_gps_collars([[10, 25, 10]]) == "ONLINE"
    assert inspect_gps_collars([[25, 30, 40]]) == "ONLINE"
