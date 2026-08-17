from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from build_powerbi_model import EXPORTS, _quality_checks


def test_powerbi_export_defines_two_facts_and_four_dimensions() -> None:
    assert set(EXPORTS) == {
        "fact_orders",
        "fact_order_items",
        "dim_customers",
        "dim_sellers",
        "dim_products",
        "dim_dates",
    }


def test_powerbi_measure_pack_covers_service_and_commercial_kpis() -> None:
    dax = (ROOT / "bi" / "power_bi" / "measures.dax").read_text(encoding="utf-8")
    for measure in ["OTDR %", "SLA Breach Rate %", "P90 Lead Time Days", "GMV", "Freight as % of GMV"]:
        assert f"{measure} :=" in dax


def test_powerbi_model_documentation_declares_relationships() -> None:
    documentation = (ROOT / "bi" / "power_bi" / "README.md").read_text(encoding="utf-8")
    assert "Model relationships" in documentation
    assert "one-to-many" in documentation
