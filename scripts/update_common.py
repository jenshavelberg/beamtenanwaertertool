"""Shared helpers/constants for update scripts."""

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

# Common payroll/config constants
VL = 6.65
KIRCHENSTEUER_RATE_HESSEN = 0.09
GKV_ARBEITNEHMER_RATE_2026 = 0.102  # 7.3% + 2.9%


def est_2025(zve: float) -> int:
    """Calculate annual Einkommensteuer for 2025 (§32a EStG)."""
    if zve <= 12096:
        return 0
    if zve <= 17443:
        y = (zve - 12096) / 10000
        return math.floor((922.98 * y + 1400) * y)
    if zve <= 66760:
        z = (zve - 17443) / 10000
        return math.floor((176.75 * z + 2397) * z + 1025.38)
    if zve <= 277825:
        return math.floor(0.42 * zve - 10637.26)
    return math.floor(0.45 * zve - 18972.21)


def calc_monthly_lst(monthly_brutto: float) -> float:
    """Calculate monthly Lohnsteuer for Beamte (StKl I/IV)."""
    annual_gross = monthly_brutto * 12
    vp = annual_gross * 0.20
    zve = max(0, annual_gross - 1230 - 36 - vp)
    zve = math.floor(zve)
    annual_est = est_2025(zve)
    return round(annual_est / 12, 2)
