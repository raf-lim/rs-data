import pandas as pd
from libs import cleaners


def test_remove_longer_not_reoprted():
    data = pd.DataFrame({
        "col1": [1, 1, 1, 1, pd.NA, pd.NA, pd.NA],
        "col2": [1, 1, 1, 1, 1, 1, 1],
    })
    
    assert len(data.columns) == 2

    # case: last not reported = 2, col1 should be removed
    cleaned_data = cleaners.remove_longer_not_reported(data, last_not_reported=2)
    assert len(cleaned_data.columns) == 1

    # case: last not reported = 3, col1 should be removed
    cleaned_data = cleaners.remove_longer_not_reported(data, last_not_reported=3)
    assert len(cleaned_data.columns) == 1

    # case: last not reported = 4, col1 should not be removed
    cleaned_data = cleaners.remove_longer_not_reported(data, last_not_reported=4)
    assert len(cleaned_data.columns) == 2