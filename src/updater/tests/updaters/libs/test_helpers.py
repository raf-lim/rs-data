import pandas as pd
from updaters.libs import helpers
from updaters.us.interfaces import Frequency, UsMetric


def test_full_year_readings_number():
    assert helpers.set_full_year_readings_number(Frequency.QUARTERLY) == 4
    assert helpers.set_full_year_readings_number(Frequency.MONTHLY) == 12
    assert helpers.set_full_year_readings_number(Frequency.WEEKLY) == 52
    assert helpers.set_full_year_readings_number(Frequency.DAILY) == 252


def test_compute_period_to_period_change_frequency_quarter():
    
    class TestMetric:
        frequency = Frequency.QUARTERLY

    metric = TestMetric()

    data = pd.DataFrame({
        "const1": [i for i in range(1, 53)],
        "const2": [i for i in range(53, 105)],
    })

    result = helpers.compute_period_to_period_change(metric, data)
    
    assert len(result.columns) == 4
    assert "const1_qtq" and "const2_qtq" in result.columns
    assert "const1_yoy" and "const2_yoy" in result.columns
    assert result["const1_qtq"][1] == data["const1"].pct_change()[1]
    assert result["const1_qtq"][2] == data["const1"].pct_change()[2]
    

def test_compute_period_to_period_change_frequency_month():
    
    class TestMetric:
        frequency = Frequency.MONTHLY

    metric = TestMetric

    data = pd.DataFrame({
        "const1": [i for i in range(1, 53)],
        "const2": [i for i in range(53, 105)],
    })

    result = helpers.compute_period_to_period_change(metric, data)
    
    assert len(result.columns) == 4
    assert "const1_mtm" and "const2_mtm" in result.columns
    assert "const1_yoy" and "const2_yoy" in result.columns
    assert result["const1_mtm"].iloc[1] == data["const1"].pct_change().iloc[1]
    assert result["const1_yoy"].iloc[12] == data["const1"].pct_change(12).iloc[12]


def test_compute_period_to_period_change_frequency_week():
    
    class TestMetric:
        frequency = Frequency.WEEKLY

    metric = TestMetric

    data = pd.DataFrame({
        "const1": [i for i in range(1, 55)],
        "const2": [i for i in range(55, 109)],
        "const3": [i for i in range(1, 55)],
    })

    result = helpers.compute_period_to_period_change(metric, data)

    assert len(result.columns) == 6
    assert "const1_mtm" and "const2_mtm" in result.columns
    assert "const1_yoy" and "const2_yoy" in result.columns
    assert result["const1_mtm"].iloc[4] == data["const1"].pct_change(4).iloc[4]
    assert result["const1_yoy"].iloc[-1] == data["const1"].pct_change(52).iloc[-1]
