import re
import unittest
from base_to_base_number.main import get_base_regex, BaseNumber
from base_to_base_number.alphabet import CHAR_TO_DIGIT_MAP, DIGIT_TO_CHAR_MAP

NUMBERS_BASE2 = [
    { 'number': "1111", 'base': 2, 'result': "15", 'precision': 2 },
    { 'number': "0001", 'base': 2, 'result': "1", 'precision': 2 },
    { 'number': "+11.11", 'base': 2, 'result': "+3.75", 'precision': 2 },
    { 'number': "-110.11", 'base': 2, 'result': "-6.75", 'precision': 2 },
    { 'number': "0.111", 'base': 2, 'result': "0.87", 'precision': 2 },
    { 'number': "0.111", 'base': 2, 'result': "0.87500", 'precision': 5 },
]
NUMBERS_BASE3 = [
    { 'number': "2222", 'base': 3, 'result': "80", 'precision': 2 },
    { 'number': "1111", 'base': 3, 'result': "40", 'precision': 2 },
    { 'number': "+21.11", 'base': 3, 'result': "+7.44", 'precision': 2 },
    { 'number': "-210.12", 'base': 3, 'result': "-21.55", 'precision': 2 },
    { 'number': "0.121", 'base': 3, 'result': "0.59", 'precision': 2 },
    { 'number': "0.121", 'base': 3, 'result': "0.5925", 'precision': 4 },
]
NUMBERS_BASE4 = [
    { 'number': "3333", 'base': 4, 'result': "255", 'precision': 2 },
    { 'number': "1111", 'base': 4, 'result': "85", 'precision': 2 },
    { 'number': "+31.11", 'base': 4, 'result': "+13.31", 'precision': 2 },
    { 'number': "-310.13", 'base': 4, 'result': "-52.43", 'precision': 2 },
    { 'number': "0.231", 'base': 4, 'result': "0.70", 'precision': 2 },
    { 'number': "0.231", 'base': 4, 'result': "0.7031", 'precision': 4 },
]
NUMBERS_BASE5 = [
    { 'number': "4444", 'base': 5, 'result': "624", 'precision': 2 },
    { 'number': "1111", 'base': 5, 'result': "156", 'precision': 2 },
    { 'number': "+41.21", 'base': 5, 'result': "+21.43", 'precision': 2 },
    { 'number': "-410.14", 'base': 5, 'result': "-105.35", 'precision': 2 },
    { 'number': "0.341", 'base': 5, 'result': "0.76", 'precision': 2 },
    { 'number': "0.341", 'base': 5, 'result': "0.7680", 'precision': 4 },
]
NUMBERS_BASE6 = [
    { 'number': "5555", 'base': 6, 'result': "1295", 'precision': 2 },
    { 'number': "1111", 'base': 6, 'result': "259", 'precision': 2 },
    { 'number': "+51.31", 'base': 6, 'result': "+31.52", 'precision': 2 },
    { 'number': "-510.15", 'base': 6, 'result': "-186.30", 'precision': 2 },
    { 'number': "0.451", 'base': 6, 'result': "0.81", 'precision': 2 },
    { 'number': "0.451", 'base': 6, 'result': "0.8101", 'precision': 4 },
]
NUMBERS_BASE7 = [
    { 'number': "6666", 'base': 7, 'result': "2400", 'precision': 2 },
    { 'number': "1111", 'base': 7, 'result': "400", 'precision': 2 },
    { 'number': "+61.41", 'base': 7, 'result': "+43.59", 'precision': 2 },
    { 'number': "-610.16", 'base': 7, 'result': "-301.26", 'precision': 2 },
    { 'number': "0.561", 'base': 7, 'result': "0.83", 'precision': 2 },
    { 'number': "0.561", 'base': 7, 'result': "0.8396", 'precision': 4 },
]
NUMBERS_BASE8 = [
    { 'number': "7777", 'base': 8, 'result': "4095", 'precision': 2 },
    { 'number': "1111", 'base': 8, 'result': "585", 'precision': 2 },
    { 'number': "+71.41", 'base': 8, 'result': "+57.51", 'precision': 2 },
    { 'number': "-710.17", 'base': 8, 'result': "-456.23", 'precision': 2 },
    { 'number': "0.471", 'base': 8, 'result': "0.61", 'precision': 2 },
    { 'number': "0.471", 'base': 8, 'result': "0.6113", 'precision': 4 },
]
NUMBERS_BASE9 = [
    { 'number': "8888", 'base': 9, 'result': "6560", 'precision': 2 },
    { 'number': "1111", 'base': 9, 'result': "820", 'precision': 2 },
    { 'number': "+81.61", 'base': 9, 'result': "+73.67", 'precision': 2 },
    { 'number': "-810.18", 'base': 9, 'result': "-657.20", 'precision': 2 },
    { 'number': "0.781", 'base': 9, 'result': "0.87", 'precision': 2 },
    { 'number': "0.781", 'base': 9, 'result': "0.8779", 'precision': 4 },
]
NUMBERS_BASE10 = [
    { 'number': "9999", 'base': 10, 'result': "9999", 'precision': 2 },
    { 'number': "1111", 'base': 10, 'result': "1111", 'precision': 2 },
    { 'number': "+91.71", 'base': 10, 'result': "+91.71", 'precision': 2 },
    { 'number': "-910.19", 'base': 10, 'result': "-910.19", 'precision': 2 },
    { 'number': "0.891", 'base': 10, 'result': "0.89", 'precision': 2 },
    { 'number': "0.891", 'base': 10, 'result': "0.891", 'precision': 4 },
]
NUMBERS_BASE11 = [
    { 'number': "AAAA", 'base': 11, 'result': "14640", 'precision': 2 },
    { 'number': "1111", 'base': 11, 'result': "1464", 'precision': 2 },
    { 'number': "+A1.81", 'base': 11, 'result': "+111.73", 'precision': 2 },
    { 'number': "-A10.1A", 'base': 11, 'result': "-1221.17", 'precision': 2 },
    { 'number': "0.9A1", 'base': 11, 'result': "0.90", 'precision': 2 },
    { 'number': "0.9A1", 'base': 11, 'result': "0.9015", 'precision': 4 },
]
NUMBERS_BASE12 = [
    { 'number': "BBBB", 'base': 12, 'result': "20735", 'precision': 2 },
    { 'number': "1111", 'base': 12, 'result': "1885", 'precision': 2 },
    { 'number': "+B1.91", 'base': 12, 'result': "+133.75", 'precision': 2 },
    { 'number': "-B10.1B", 'base': 12, 'result': "-1596.15", 'precision': 2 },
    { 'number': "0.AB1", 'base': 12, 'result': "0.91", 'precision': 2 },
    { 'number': "0.AB1", 'base': 12, 'result': "0.9103", 'precision': 4 },
]
NUMBERS_BASE13 = [
    { 'number': "CCCC", 'base': 13, 'result': "28560", 'precision': 2 },
    { 'number': "1111", 'base': 13, 'result': "2380", 'precision': 2 },
    { 'number': "+C1.A1", 'base': 13, 'result': "+157.77", 'precision': 2 },
    { 'number': "-C10.1C", 'base': 13, 'result': "-2041.14", 'precision': 2 },
    { 'number': "0.BC1", 'base': 13, 'result': "0.91", 'precision': 2 },
    { 'number': "0.BC1", 'base': 13, 'result': "0.9176", 'precision': 4 },
]
NUMBERS_BASE14 = [
    { 'number': "DDDD", 'base': 14, 'result': "38415", 'precision': 2 },
    { 'number': "1111", 'base': 14, 'result': "2955", 'precision': 2 },
    { 'number': "+D1.B1", 'base': 14, 'result': "+183.79", 'precision': 2 },
    { 'number': "-D10.1D", 'base': 14, 'result': "-2562.13", 'precision': 2 },
    { 'number': "0.CD1", 'base': 14, 'result': "0.92", 'precision': 2 },
    { 'number': "0.CD1", 'base': 14, 'result': "0.9238", 'precision': 4 },
]
NUMBERS_BASE15 = [
    { 'number': "EEEE", 'base': 15, 'result': "50624", 'precision': 2 },
    { 'number': "1111", 'base': 15, 'result': "3616", 'precision': 2 },
    { 'number': "+E1.C1", 'base': 15, 'result': "+211.80", 'precision': 2 },
    { 'number': "-E10.1E", 'base': 15, 'result': "-3165.12", 'precision': 2 },
    { 'number': "0.DE1", 'base': 15, 'result': "0.92", 'precision': 2 },
    { 'number': "0.DE1", 'base': 15, 'result': "0.9291", 'precision': 4 },
]
NUMBERS_BASE16 = [
    { 'number': "FFFF", 'base': 16, 'result': "65535", 'precision': 2 },
    { 'number': "1111", 'base': 16, 'result': "4369", 'precision': 2 },
    { 'number': "+F1.81", 'base': 16, 'result': "+241.50", 'precision': 2 },
    { 'number': "-F10.1F", 'base': 16, 'result': "-3856.12", 'precision': 2 },
    { 'number': "0.8F1", 'base': 16, 'result': "0.55", 'precision': 2 },
    { 'number': "0.8F1", 'base': 16, 'result': "0.5588378906", 'precision': 10 },
]
NUMBERS_BASE17 = [
    { 'number': "GGGG", 'base': 17, 'result': "83520", 'precision': 2 },
    { 'number': "1111", 'base': 17, 'result': "5220", 'precision': 2 },
    { 'number': "+G1.E1", 'base': 17, 'result': "+273.82", 'precision': 2 },
    { 'number': "-G10.1G", 'base': 17, 'result': "-4641.11", 'precision': 2 },
    { 'number': "0.FG1", 'base': 17, 'result': "0.93", 'precision': 2 },
    { 'number': "0.FG1", 'base': 17, 'result': "0.9379", 'precision': 4 },
]
NUMBERS_BASE18 = [
    { 'number': "HHHH", 'base': 18, 'result': "104975", 'precision': 2 },
    { 'number': "1111", 'base': 18, 'result': "6175", 'precision': 2 },
    { 'number': "+H1.F1", 'base': 18, 'result': "+307.83", 'precision': 2 },
    { 'number': "-H10.1H", 'base': 18, 'result': "-5526.10", 'precision': 2 },
    { 'number': "0.GH1", 'base': 18, 'result': "0.94", 'precision': 2 },
    { 'number': "0.GH1", 'base': 18, 'result': "0.9415", 'precision': 4 },
]
NUMBERS_BASE19 = [
    { 'number': "IIII", 'base': 19, 'result': "130320", 'precision': 2 },
    { 'number': "1111", 'base': 19, 'result': "7240", 'precision': 2 },
    { 'number': "+I1.G1", 'base': 19, 'result': "+343.84", 'precision': 2 },
    { 'number': "-I10.1I", 'base': 19, 'result': "-6517.10", 'precision': 2 },
    { 'number': "0.HI1", 'base': 19, 'result': "0.94", 'precision': 2 },
    { 'number': "0.HI1", 'base': 19, 'result': "0.9447", 'precision': 4 },
]
NUMBERS_BASE20 = [
    { 'number': "JJJJ", 'base': 20, 'result': "159999", 'precision': 2 },
    { 'number': "1111", 'base': 20, 'result': "8421", 'precision': 2 },
    { 'number': "+J1.H1", 'base': 20, 'result': "+381.85", 'precision': 2 },
    { 'number': "-J10.1J", 'base': 20, 'result': "-7620.09", 'precision': 2 },
    { 'number': "0.IJ1", 'base': 20, 'result': "0.94", 'precision': 2 },
    { 'number': "0.IJ1", 'base': 20, 'result': "0.9476", 'precision': 4 },
]
NUMBERS_BASE21 = [
    { 'number': "KKKK", 'base': 21, 'result': "194480", 'precision': 2 },
    { 'number': "1111", 'base': 21, 'result': "9724", 'precision': 2 },
    { 'number': "+K1.I1", 'base': 21, 'result': "+421.85", 'precision': 2 },
    { 'number': "-K10.1K", 'base': 21, 'result': "-8841.09", 'precision': 2 },
    { 'number': "0.JK1", 'base': 21, 'result': "0.95", 'precision': 2 },
    { 'number': "0.JK1", 'base': 21, 'result': "0.9502", 'precision': 4 },
]
NUMBERS_BASE22 = [
    { 'number': "LLLL", 'base': 22, 'result': "234255", 'precision': 2 },
    { 'number': "1111", 'base': 22, 'result': "11155", 'precision': 2 },
    { 'number': "+L1.J1", 'base': 22, 'result': "+463.86", 'precision': 2 },
    { 'number': "-L10.1L", 'base': 22, 'result': "-10186.08", 'precision': 2 },
    { 'number': "0.KL1", 'base': 22, 'result': "0.95", 'precision': 2 },
    { 'number': "0.KL1", 'base': 22, 'result': "0.9525", 'precision': 4 },
]
NUMBERS_BASE23 = [
    { 'number': "MMMM", 'base': 23, 'result': "279840", 'precision': 2 },
    { 'number': "1111", 'base': 23, 'result': "12720", 'precision': 2 },
    { 'number': "+M1.K1", 'base': 23, 'result': "+507.87", 'precision': 2 },
    { 'number': "-M10.1M", 'base': 23, 'result': "-11661.08", 'precision': 2 },
    { 'number': "0.LM1", 'base': 23, 'result': "0.95", 'precision': 2 },
    { 'number': "0.LM1", 'base': 23, 'result': "0.9547", 'precision': 4 },
]
NUMBERS_BASE24 = [
    { 'number': "NNNN", 'base': 24, 'result': "331775", 'precision': 2 },
    { 'number': "1111", 'base': 24, 'result': "14425", 'precision': 2 },
    { 'number': "+N1.L1", 'base': 24, 'result': "+553.87", 'precision': 2 },
    { 'number': "-N10.1N", 'base': 24, 'result': "-13272.08", 'precision': 2 },
    { 'number': "0.MN1", 'base': 24, 'result': "0.95", 'precision': 2 },
    { 'number': "0.MN1", 'base': 24, 'result': "0.9566", 'precision': 4 },
]
NUMBERS_BASE25 = [
    { 'number': "OOOO", 'base': 25, 'result': "390624", 'precision': 2 },
    { 'number': "1111", 'base': 25, 'result': "16276", 'precision': 2 },
    { 'number': "+O1.M1", 'base': 25, 'result': "+601.88", 'precision': 2 },
    { 'number': "-O10.1O", 'base': 25, 'result': "-15025.07", 'precision': 2 },
    { 'number': "0.NO1", 'base': 25, 'result': "0.95", 'precision': 2 },
    { 'number': "0.NO1", 'base': 25, 'result': "0.9584", 'precision': 4 },
]
NUMBERS_BASE26 = [
    { 'number': "PPPP", 'base': 26, 'result': "456975", 'precision': 2 },
    { 'number': "1111", 'base': 26, 'result': "18279", 'precision': 2 },
    { 'number': "+P1.N1", 'base': 26, 'result': "+651.88", 'precision': 2 },
    { 'number': "-P10.1P", 'base': 26, 'result': "-16926.07", 'precision': 2 },
    { 'number': "0.OP1", 'base': 26, 'result': "0.96", 'precision': 2 },
    { 'number': "0.OP1", 'base': 26, 'result': "0.9601", 'precision': 4 },
]
NUMBERS_BASE27 = [
    { 'number': "QQQQ", 'base': 27, 'result': "531440", 'precision': 2 },
    { 'number': "1111", 'base': 27, 'result': "20440", 'precision': 2 },
    { 'number': "+Q1.O1", 'base': 27, 'result': "+703.89", 'precision': 2 },
    { 'number': "-Q10.1Q", 'base': 27, 'result': "-18981.07", 'precision': 2 },
    { 'number': "0.PQ1", 'base': 27, 'result': "0.96", 'precision': 2 },
    { 'number': "0.PQ1", 'base': 27, 'result': "0.9616", 'precision': 4 },
]
NUMBERS_BASE28 = [
    { 'number': "RRRR", 'base': 28, 'result': "614655", 'precision': 2 },
    { 'number': "1111", 'base': 28, 'result': "22765", 'precision': 2 },
    { 'number': "+R1.P1", 'base': 28, 'result': "+757.89", 'precision': 2 },
    { 'number': "-R10.1R", 'base': 28, 'result': "-21196.07", 'precision': 2 },
    { 'number': "0.QR1", 'base': 28, 'result': "0.96", 'precision': 2 },
    { 'number': "0.QR1", 'base': 28, 'result': "0.9630", 'precision': 4 },
]
NUMBERS_BASE29 = [
    { 'number': "SSSS", 'base': 29, 'result': "707280", 'precision': 2 },
    { 'number': "1111", 'base': 29, 'result': "25260", 'precision': 2 },
    { 'number': "+S1.Q1", 'base': 29, 'result': "+813.89", 'precision': 2 },
    { 'number': "-S10.1S", 'base': 29, 'result': "-23577.06", 'precision': 2 },
    { 'number': "0.RS1", 'base': 29, 'result': "0.96", 'precision': 2 },
    { 'number': "0.RS1", 'base': 29, 'result': "0.9643", 'precision': 4 },
]
NUMBERS_BASE30 = [
    { 'number': "TTTT", 'base': 30, 'result': "809999", 'precision': 2 },
    { 'number': "1111", 'base': 30, 'result': "27931", 'precision': 2 },
    { 'number': "+T1.R1", 'base': 30, 'result': "+871.90", 'precision': 2 },
    { 'number': "-T10.1T", 'base': 30, 'result': "-26130.06", 'precision': 2 },
    { 'number': "0.ST1", 'base': 30, 'result': "0.96", 'precision': 2 },
    { 'number': "0.ST1", 'base': 30, 'result': "0.9655", 'precision': 4 },
]
NUMBERS_BASE31 = [
    { 'number': "UUUU", 'base': 31, 'result': "923520", 'precision': 2 },
    { 'number': "1111", 'base': 31, 'result': "30784", 'precision': 2 },
    { 'number': "+U1.S1", 'base': 31, 'result': "+931.90", 'precision': 2 },
    { 'number': "-U10.1U", 'base': 31, 'result': "-28861.06", 'precision': 2 },
    { 'number': "0.TU1", 'base': 31, 'result': "0.96", 'precision': 2 },
    { 'number': "0.TU1", 'base': 31, 'result': "0.9667", 'precision': 4 },
]
NUMBERS_BASE32 = [
    { 'number': "VVVV", 'base': 32, 'result': "1048575", 'precision': 2 },
    { 'number': "1111", 'base': 32, 'result': "33825", 'precision': 2 },
    { 'number': "+V1.T1", 'base': 32, 'result': "+993.90", 'precision': 2 },
    { 'number': "-V10.1V", 'base': 32, 'result': "-31776.06", 'precision': 2 },
    { 'number': "0.UV1", 'base': 32, 'result': "0.96", 'precision': 2 },
    { 'number': "0.UV1", 'base': 32, 'result': "0.9678", 'precision': 4 },
]
NUMBERS_BASE33 = [
    { 'number': "WWWW", 'base': 33, 'result': "1185920", 'precision': 2 },
    { 'number': "1111", 'base': 33, 'result': "37060", 'precision': 2 },
    { 'number': "+W1.U1", 'base': 33, 'result': "+1057.91", 'precision': 2 },
    { 'number': "-W10.1W", 'base': 33, 'result': "-34881.05", 'precision': 2 },
    { 'number': "0.VW1", 'base': 33, 'result': "0.96", 'precision': 2 },
    { 'number': "0.VW1", 'base': 33, 'result': "0.9688", 'precision': 4 },
]
NUMBERS_BASE34 = [
    { 'number': "XXXX", 'base': 34, 'result': "1336335", 'precision': 2 },
    { 'number': "1111", 'base': 34, 'result': "40495", 'precision': 2 },
    { 'number': "+X1.V1", 'base': 34, 'result': "+1123.91", 'precision': 2 },
    { 'number': "-X10.1X", 'base': 34, 'result': "-38182.05", 'precision': 2 },
    { 'number': "0.WX1", 'base': 34, 'result': "0.96", 'precision': 2 },
    { 'number': "0.WX1", 'base': 34, 'result': "0.9697", 'precision': 4 },
]
NUMBERS_BASE35 = [
    { 'number': "YYYY", 'base': 35, 'result': "1500624", 'precision': 2 },
    { 'number': "1111", 'base': 35, 'result': "44136", 'precision': 2 },
    { 'number': "+Y1.W1", 'base': 35, 'result': "+1191.91", 'precision': 2 },
    { 'number': "-Y10.1Y", 'base': 35, 'result': "-41685.05", 'precision': 2 },
    { 'number': "0.XY1", 'base': 35, 'result': "0.97", 'precision': 2 },
    { 'number': "0.XY1", 'base': 35, 'result': "0.9706", 'precision': 4 },
]
NUMBERS_BASE36 = [
    { 'number': "ZZZZ", 'base': 36, 'result': "1679615", 'precision': 2 },
    { 'number': "1111", 'base': 36, 'result': "47989", 'precision': 2 },
    { 'number': "+Z1.X1", 'base': 36, 'result': "+1261.91", 'precision': 2 },
    { 'number': "-Z10.1Z", 'base': 36, 'result': "-45396.05", 'precision': 2 },
    { 'number': "0.YZ1", 'base': 36, 'result': "0.97", 'precision': 2 },
    { 'number': "0.YZ1", 'base': 36, 'result': "0.9714", 'precision': 4 },
]


class TestBaseRegex(unittest.TestCase):
    """Tests for the get_base_regex function."""

    def test_get_base_regex_valid_bases(self):
        # Test base 2 regex generation and matching
        regex_2 = get_base_regex(2)
        self.assertTrue(bool(re.match(regex_2, "1011")))
        self.assertFalse(bool(re.match(regex_2, "1021")))

        # Test base 10 regex generation and matching
        regex_10 = get_base_regex(10)
        self.assertTrue(bool(re.match(regex_10, "123.45")))
        self.assertFalse(bool(re.match(regex_10, "123a45")))

        # Test base 16 regex generation and matching
        regex_16 = get_base_regex(16)
        self.assertTrue(bool(re.match(regex_16, "4e7.8fabc")))
        self.assertFalse(bool(re.match(regex_16, "4e7.8fabcg")))

    def test_get_base_regex_invalid_bases(self):
        # Bases below 2 should raise ValueError
        with self.assertRaises(ValueError):
            get_base_regex(1)

        # Bases above 36 should raise ValueError
        with self.assertRaises(ValueError):
            get_base_regex(37)


class TestBaseNumber(unittest.TestCase):
    """Tests for the BaseNumber class and its methods."""

    def test_init_raw_parts(self):
        # Test parsing of integer and fraction parts for base 16
        num = BaseNumber("4e7.8fabc", base=16)
        self.assertEqual(num.get_integer_raw(), "4e7")
        self.assertEqual(num.get_fraction_raw(), "8fabc")
        self.assertEqual(num.get_number_raw(), "4e7.8fabc")
        self.assertEqual(str(num), "4e7.8fabc")

    def test_signed_numbers(self):
        # Test positive sign handling
        num_pos = BaseNumber("+10.5", base=10)
        self.assertEqual(num_pos.sign, "+")
        self.assertEqual(num_pos.get_number_raw(), "10.5")

        # Test negative sign handling
        num_neg = BaseNumber("-10.5", base=10)
        self.assertEqual(num_neg.sign, "-")
        self.assertEqual(num_neg.get_number_raw(), "10.5")

    def test_integer_only_number(self):
        # Test numbers without a fraction or delimiter
        num = BaseNumber("1010", base=2)
        self.assertEqual(num.get_integer_raw(), "1010")
        self.assertIsNone(num.get_fraction_raw())
        self.assertEqual(num.get_integer(), 10)

    def test_digit_maps(self):
        # Validate lookup dictionaries exist and map correctly
        self.assertEqual(CHAR_TO_DIGIT_MAP["a"], 10)
        self.assertEqual(CHAR_TO_DIGIT_MAP["F"], 15)
        self.assertEqual(DIGIT_TO_CHAR_MAP[10], "A")
        self.assertEqual(DIGIT_TO_CHAR_MAP[15], "F")

    def test_conversion_method_base2(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE2:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base3(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE3:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base4(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE4:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base5(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE5:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base6(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE6:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base7(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE7:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base8(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE8:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base9(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE9:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base10(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE10:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base11(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE11:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base12(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE12:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base13(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE13:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base14(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE14:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base15(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE15:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base16(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE16:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base17(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE17:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base18(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE18:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base19(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE19:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base20(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE20:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base21(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE21:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base22(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE22:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base23(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE23:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base24(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE24:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base25(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE25:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base26(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE26:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base27(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE27:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base28(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE28:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base29(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE29:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base30(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE30:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base31(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE31:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base32(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE32:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base33(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE33:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base34(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE34:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base35(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE35:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])

    def test_conversion_method_base36(self):
        # Test basic invocation of convert_to method
        for number in NUMBERS_BASE36:
            num = BaseNumber(number["number"], base=number["base"])
            result = num.convert_to(10, precision=number['precision'])
            self.assertIsInstance(result, str)
            self.assertEqual(result, number["result"])


if __name__ == "__main__":
    unittest.main()