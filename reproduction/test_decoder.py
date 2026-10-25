"""Synthetic tests only; no historic transcription or cipher key embedded."""
import unittest

from decoder import STOP, decode, partitions, render


class DecoderTests(unittest.TestCase):
    def setUp(self):
        self.key = {"1": "a", "2": "b", "12": "c"}

    def test_counts(self):
        report = decode("# header\n1 2 [word] 300 4?\n", self.key)
        self.assertEqual(report["numeric_denominator"], 4)
        self.assertEqual(report["alphabet_coverage"], 0.5)
        self.assertEqual(report["counts"], {
            "assigned_numeric": 2, "clear_spans": 1,
            "unresolved_numeric": 1, "uncertain_numeric": 1,
        })
        self.assertIsNone(report["accuracy"])

    def test_no_silent_repairs(self):
        self.assertEqual(render("1?", self.key), "<1?>")
        self.assertEqual(render("121", self.key), "<121>")

    def test_all_exact_partitions(self):
        self.assertEqual(partitions("121", self.key), [["1", "2", "1"], ["12", "1"]])
        self.assertEqual(partitions("100", self.key), [])
        self.assertEqual(partitions("01", self.key), [])

    def test_stops_before_other_cipher(self):
        report = decode("1\n" + STOP + "\n2\n", self.key)
        self.assertEqual(len(report["lines"]), 1)

    def test_physical_lines_and_repeat_retained(self):
        report = decode("# source\n\n1\n1 (repetition)\n", self.key)
        self.assertEqual([r["line"] for r in report["lines"]], [3, 4])
        self.assertEqual(report["numeric_denominator"], 2)

    def test_unsupported_notation_fails(self):
        with self.assertRaises(ValueError):
            decode("1 + 2", self.key)

    def test_empty_coverage(self):
        self.assertIsNone(decode("[word]\n", self.key)["alphabet_coverage"])


if __name__ == "__main__":
    unittest.main()
