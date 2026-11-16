import pytest
from src.manager import Manager
from src.models import ApartmentSettlement, Parameters


def test_apartment_settlement_with_bills():
    manager = Manager(Parameters())
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_due_pln == 910.0


def test_apartment_settlement_without_bills():
    manager = Manager(Parameters())
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 2)
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 2
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_due_pln == 0.0
    assert manager.create_apartment_settlement('missing', 2025, 1) is None


def test_apartment_settlement_rejects_bad_month():
    with pytest.raises(ValueError):
        Manager(Parameters()).create_apartment_settlement('apart-polanka', 2025, 13)
