import unittest

import pandas as pd

from src import utils


class TestHotspotsByUser(unittest.TestCase):
    def setUp(self) -> None:
        # some data to work with
        self.df = df = pd.DataFrame(
            {
                "owner_id": [1, 1, 2, 3],
                "name": [
                    "home",
                    "office",
                    "hotel damien",
                    "T800",
                ],
            }
        )

    def test_missing_column(self):
        df = pd.DataFrame(
            {
                "Name": [
                    "Braund, Mr. Owen Harris",
                    "Bonnell, Miss. Elizabeth",
                ],
                "Age": [22, 35],
                "Sex": ["male", "female"],
            }
        )

        with self.assertRaises(AssertionError):
            utils.hotspots_by_user(42, df)

    def test_user_has_records(self):
        uid = 1
        udf = utils.hotspots_by_user(uid, self.df)
        self.assertEqual(len(udf), 2)

    def test_user_is_missing(self):
        uid = 10
        udf = utils.hotspots_by_user(uid, self.df)
        self.assertEqual(len(udf), 0)


class TestHotspotsWithLocation(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame()

    def test_foursquare_location_present(self):
        self.df["foursquare_id"] = ["f1", "f2", None]
        self.df["google_place_id"] = [None] * 3
        selection = utils.hotspots_with_location(self.df)
        self.assertEqual(len(selection), 2)

    def test_google_place_location_present(self):
        self.df["foursquare_id"] = [None] * 4
        self.df["google_place_id"] = [None, "g2", "g3", "g4"]
        selection = utils.hotspots_with_location(self.df)
        self.assertEqual(len(selection), 3)

    def test_no_location_present(self):
        self.df["foursquare_id"] = [None] * 5
        self.df["google_place_id"] = [None] * 5
        selection = utils.hotspots_with_location(self.df)
        self.assertEqual(len(selection), 0)


class TestHotspotsSince(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame(
            pd.to_datetime(["2020-01-01", "2020-02-01", "2020-03-01"], utc=True),
            columns=["created_at"],
        )

    def test_basic(self):
        since = pd.to_datetime("2020-01-05", utc=True)
        selection = utils.hotspots_since(self.df, since)
        self.assertEqual(len(selection), 2)


class TestHotspotsWithScore(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame(
            [0.2, 0.4, 0.6, 0.8, 1.0],
            columns=["score_v4"],
        )

    def test_lower_bound(self):
        selection = utils.hotspots_with_score(self.df, lower=0.5)
        self.assertEqual(len(selection), 3)

    def test_upper_bound(self):
        selection = utils.hotspots_with_score(self.df, upper=0.43)
        self.assertEqual(len(selection), 2)

    def test_lower_upper(self):
        selection = utils.hotspots_with_score(self.df, lower=0.27, upper=0.64)
        self.assertEqual(len(selection), 2)


if __name__ == "__main__":
    unittest.main()
