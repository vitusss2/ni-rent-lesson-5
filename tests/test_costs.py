import pytest
from src.manager import Manager
from src.models import Bill, Parameters


def test_apartment_costs_filter_period_and_apartment():
    manager = Manager(Parameters())
    assert manager.get_apartment_costs('missing', 2025, 1) is None
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
    manager.bills.append(Bill(apartment='apart-polanka', date_due='2025-02-01', settlement_year=2025, settlement_month=2, amount_pln=250, type='water'))
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 250.0
    assert manager.get_apartment_costs('apart-polanka', 2025) == 1160.0
    assert manager.get_apartment_costs('apart-polanka') == 1160.0


@pytest.mark.parametrize('month', [-1, 0, 13, 100, 1.5, '3', None])
def test_invalid_month(month):
    manager = Manager(Parameters())
    if month is None:
        assert manager.get_apartment_costs('apart-polanka', 2025, month) == 910.0
    else:
        with pytest.raises(ValueError):
            manager.get_apartment_costs('apart-polanka', 2025, month)


def test_month_requires_year():
    with pytest.raises(ValueError):
        Manager(Parameters()).get_apartment_costs('apart-polanka', month=1)
