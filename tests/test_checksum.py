import unittest
from lc29h.utils.checksum import compute_checksum, validate_checksum


class TestNMEAChecksum(unittest.TestCase):

    def test_valid_checksum(self):
        self.assertEqual(
            compute_checksum("GNRMC,093316.000,A,3149.332558,N,11706.912570,E,0.00,237.67,140122,,,A,V"), "0B"
        )
        self.assertEqual(compute_checksum("$GNZDA,093316.000,14,01,2022,,"), "40")
        self.assertEqual(compute_checksum("$GNGLL,3149.332558,N,11706.912570,E,093316.000,A,A"), "45")

    def test_empty_string(self):
        self.assertEqual(compute_checksum(""), "00")


class TestNMEAValidate(unittest.TestCase):
    def test_valid_sentence(self):
        self.assertEqual(
            validate_checksum("$GNRMC,093316.000,A,3149.332558,N,11706.912570,E,0.00,237.67,140122,,,A,V*0B"),
            "GNRMC,093316.000,A,3149.332558,N,11706.912570,E,0.00,237.67,140122,,,A,V",
        )
        self.assertEqual(
            validate_checksum("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"),
            "GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,",
        )
        self.assertEqual(
            validate_checksum("$GPGSV,2,2,08,27,45,037,33,09,28,244,28,04,20,206,26,30,,,27,8*5E"),
            "GPGSV,2,2,08,27,45,037,33,09,28,244,28,04,20,206,26,30,,,27,8",
        )

    def test_invalid_sentence(self):
        with self.assertRaises(ValueError):
            validate_checksum("$GNRMC,093316.000,A,3149.332558,N,11706.912570,E,0.00,237.67,140122,,,A,V*00")
        with self.assertRaises(ValueError):
            validate_checksum("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*00")
        with self.assertRaises(ValueError):
            validate_checksum("$GPGLL,4916.45,N,12311.12,W,225444,A*00")

    def test_missing_checksum(self):
        with self.assertRaises(ValueError):
            validate_checksum("$GNRMC,093316.000,A,3149.332558,N,11706.912570,E,0.00,237.67,140122,,,A,V")
        with self.assertRaises(ValueError):
            validate_checksum("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
        with self.assertRaises(ValueError):
            validate_checksum("$GPGLL,4916.45,N,12311.12,W,225444,A")

    def test_quectel(self):
        self.assertEqual(validate_checksum("$PAIR004*3E"), "PAIR004")
        self.assertEqual(validate_checksum("$PAIR001,004,0*3F"), "PAIR001,004,0")
        self.assertEqual(validate_checksum("$PAIR010,0,0,2044,369413*33"), "PAIR010,0,0,2044,369413")


if __name__ == "__main__":
    unittest.main()
