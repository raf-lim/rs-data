from updaters.dbmf import collectors


class TestFetchAndParseData:

    def test_positive(self):
        DBMF_URL = "tests/updaters/dbmf/DBMF-Holdings.xlsx"
        data = collectors.fetch_data(DBMF_URL)
        data = collectors.parse_data(data)

        assert data.loc[0, "DATE"] == 20240125
        assert "TICKER" in data.columns

    def test_negative_wrong_path(self):
        DBMF_URL = "tests/updaters/dbmf/DBMF-Holdings"
        collectors.fetch_data(DBMF_URL)
        
        assert FileNotFoundError

    def test_negative_file_empty(self):
        DBMF_URL = "tests/updaters/dbmf/DBMF-Holdings_empty.xlsx"
        data = collectors.fetch_data(DBMF_URL)
        data = collectors.parse_data(data)

        assert IndexError