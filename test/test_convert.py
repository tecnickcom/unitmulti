"""Tests for Convert class."""

from unittest import TestCase
from unitmulti.convert import Convert


class TestProcess(TestCase):

    cnv = Convert()

    def test_get_value_multiple(self):
        data = [
            (0, 1000, 0, ""),
            (1, 1000, 1, ""),
            (123, 1000, 123, ""),
            (10 ** 3, 1000, 1, "K"),
            (10 ** 6, 1000, 1, "M"),
            (10 ** 9, 1000, 1, "G"),
            (10 ** 12, 1000, 1, "T"),
            (10 ** 15, 1000, 1, "P"),
            (10 ** 18, 1000, 1, "E"),
            (10 ** 21, 1000, 1, "Z"),
            (10 ** 24, 1000, 1, "Y"),
            (2 ** 10, 1024, 1, "K"),
            (2 ** 20, 1024, 1, "M"),
            (2 ** 30, 1024, 1, "G"),
            (2 ** 40, 1024, 1, "T"),
            (2 ** 50, 1024, 1, "P"),
            (2 ** 60, 1024, 1, "E"),
            (2 ** 70, 1024, 1, "Z"),
            (2 ** 80, 1024, 1, "Y"),
            (2 ** 90, 1024, 1024.0, "Y"),
        ]
        for value, step, expvalue, expmultiple in data:
            self.assertEqual(
                self.cnv.get_value_multiple(value, step), (expvalue, expmultiple)
            )

    def test_get_iec_value_multiple(self):
        data = [
            (0, 0, "B"),
            (1, 1, "B"),
            (123, 123, "B"),
            (2 ** 10, 1, "KiB"),
            (2 ** 20, 1, "MiB"),
            (2 ** 30, 1, "GiB"),
            (2 ** 40, 1, "TiB"),
            (2 ** 50, 1, "PiB"),
            (2 ** 60, 1, "EiB"),
            (2 ** 70, 1, "ZiB"),
            (2 ** 80, 1, "YiB"),
        ]
        for value, expvalue, expmultiple in data:
            self.assertEqual(
                self.cnv.get_iec_value_multiple(value), (expvalue, expmultiple)
            )

    def test_get_si_value_multiple(self):
        data = [
            (0, "s", 0, "s"),
            (1, "s", 1, "s"),
            (123, "s", 123, "s"),
            (10 ** 3, "s", 1, "Ks"),
            (10 ** 6, "s", 1, "Ms"),
            (10 ** 9, "s", 1, "Gs"),
            (10 ** 12, "s", 1, "Ts"),
            (10 ** 15, "s", 1, "Ps"),
            (10 ** 18, "s", 1, "Es"),
            (10 ** 21, "s", 1, "Zs"),
            (10 ** 24, "s", 1, "Ys"),
        ]
        for value, unit, expvalue, expunit in data:
            self.assertEqual(
                self.cnv.get_si_value_multiple(value, unit), (expvalue, expunit)
            )

    def test_get_value_submultiple(self):
        data = [
            (0, "s", 0, "s"),
            (1, "s", 1, "s"),
            (123, "s", 123, "s"),
            (10 ** -3, "s", 1, "ms"),
            (10 ** -6, "s", 1, "us"),
            (10 ** -9, "s", 1, "ns"),
            (10 ** -12, "s", 1, "ps"),
            (10 ** -15, "s", 1, "fs"),
            (10 ** -18, "s", 1, "as"),
            (10 ** -21, "s", 1, "zs"),
            (10 ** -24, "s", 1, "ys"),
            (10 ** -27, "s", 0.001, "ys"),
        ]
        for value, unit, expvalue, expunit in data:
            self.assertEqual(
                self.cnv.get_value_submultiple(value, unit), (expvalue, expunit)
            )

    def test_format_unit_value(self):
        data = [
            (0, "s", "  0.0 s"),
            (1, "s", "  1.0 s"),
            (123, "B", "  123 B"),
            (123.456, "KiB", "123.5 KiB"),
        ]
        for value, unit, exp in data:
            self.assertEqual(self.cnv.format_unit_value(value, unit), exp)


class TestBenchmarkProcess(object):

    cnv = Convert()

    def test_get_value_multiple(self, benchmark):
        benchmark(self.cnv.get_value_multiple, 2 ** 80, 1024)

    def test_get_iec_value_multiple(self, benchmark):
        benchmark(self.cnv.get_iec_value_multiple, 2 ** 80)

    def test_get_si_value_multiple(self, benchmark):
        benchmark(self.cnv.get_si_value_multiple, 10 ** 24, "s")

    def test_get_value_submultiple(self, benchmark):
        benchmark(self.cnv.get_value_submultiple, 10 ** -24, "s")
