from src.models import (
    Apartment, ApartmentSettlement, Bill, Parameters, Tenant,
    TenantSettlement, Transfer,
)


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(self, apartment_key: str, year: int | None = None,
                            month: int | None = None) -> float | None:
        """Sum apartment bills; optional year/month restrict the period."""
        if month is not None and (type(month) is not int or not 1 <= month <= 12):
            raise ValueError('month must be an integer between 1 and 12')
        if year is not None and (type(year) is not int or year < 1):
            raise ValueError('year must be a positive integer')
        if month is not None and year is None:
            raise ValueError('year is required when month is provided')
        if apartment_key not in self.apartments:
            return None

        return float(sum(
            bill.amount_pln for bill in self.bills
            if bill.apartment == apartment_key
            and (year is None or bill.settlement_year == year)
            and (month is None or bill.settlement_month == month)
        ))

    def create_apartment_settlement(self, apartment_key: str, year: int,
                                    month: int) -> ApartmentSettlement | None:
        """Create a monthly bill settlement; payment processing comes later."""
        costs = self.get_apartment_costs(apartment_key, year, month)
        if costs is None:
            return None
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=0.0,
            total_bills_pln=costs,
            total_due_pln=costs,
        )

    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement
                                  ) -> list[TenantSettlement]:
        """Split bills equally among tenants assigned to this apartment."""
        tenants = [
            (key, tenant) for key, tenant in self.tenants.items()
            if tenant.apartment == apartment_settlement.apartment
        ]
        if not tenants:
            return []
        share = apartment_settlement.total_bills_pln / len(tenants)
        return [
            TenantSettlement(
                tenant=key,
                apartment_settlement=apartment_settlement.apartment,
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=tenant.rent_pln,
                bills_pln=share,
                total_due_pln=tenant.rent_pln + share,
                balance_pln=-(tenant.rent_pln + share),
            )
            for key, tenant in tenants
        ]
