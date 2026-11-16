from src.manager import Manager
from src.models import Parameters, TenantSettlement
import pytest


def test_multiple_tenants_split_bills_equally():
    manager = Manager(Parameters())
    apartment = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    settlements = manager.create_tenant_settlements(apartment)
    assert len(settlements) == 3
    assert all(isinstance(item, TenantSettlement) for item in settlements)
    assert {item.tenant for item in settlements} == {'tenant-1', 'tenant-2', 'tenant-3'}
    assert all(item.apartment_settlement == 'apart-polanka' for item in settlements)
    assert all(item.month == 1 for item in settlements)
    assert all(item.year == 2025 for item in settlements)
    assert all(item.bills_pln == pytest.approx(910 / 3) for item in settlements)
    assert sum(item.bills_pln for item in settlements) == pytest.approx(910)
    assert {item.rent_pln for item in settlements} == {1500, 1400, 1300}
    assert all(item.total_due_pln == pytest.approx(item.rent_pln + item.bills_pln) for item in settlements)
    assert all(item.balance_pln == pytest.approx(-item.total_due_pln) for item in settlements)


def test_one_tenant_pays_all_bills():
    manager = Manager(Parameters())
    manager.tenants = {'tenant-1': manager.tenants['tenant-1']}
    apartment = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    settlements = manager.create_tenant_settlements(apartment)
    assert len(settlements) == 1
    assert settlements[0].tenant == 'tenant-1'
    assert settlements[0].bills_pln == 910.0
    assert settlements[0].rent_pln == 1500.0
    assert settlements[0].total_due_pln == 2410.0
    assert settlements[0].balance_pln == -2410.0


def test_no_tenants_creates_no_settlements():
    manager = Manager(Parameters())
    manager.tenants = {}
    apartment = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    assert manager.create_tenant_settlements(apartment) == []
    assert apartment.total_bills_pln == 910.0


def test_no_bills_creates_zero_bill_shares():
    manager = Manager(Parameters())
    apartment = manager.create_apartment_settlement('apart-polanka', 2025, 2)
    settlements = manager.create_tenant_settlements(apartment)
    assert len(settlements) == 3
    assert all(item.bills_pln == 0.0 for item in settlements)
