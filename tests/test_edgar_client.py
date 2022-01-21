from typing import Dict

from sec_edgar_api import EdgarClient


def test_get_submissions(edgar_client: EdgarClient, apple_stock: Dict[str, str]):
    cik = apple_stock["cik"]
    submissions_original = edgar_client.get_submissions(
        cik=cik, handle_pagination=False
    )

    num_recent_filings = len(
        submissions_original["filings"]["recent"]["accessionNumber"]
    )
    num_older_filings = sum(
        f["filingCount"] for f in submissions_original["filings"]["files"]
    )
    expected = num_recent_filings + num_older_filings

    submissions_merged = edgar_client.get_submissions(cik=cik, handle_pagination=True)
    assert expected == len(submissions_merged["filings"]["recent"]["accessionNumber"])

    for merged_list in submissions_merged["filings"]["recent"].values():
        assert expected == len(merged_list)


def test_get_company_concept(
    edgar_client: EdgarClient,
    apple_stock: Dict[str, str],
    concept_data_accounts_payable_current: Dict[str, str],
):
    cik = apple_stock["cik"]
    name = apple_stock["name"]
    taxonomy = concept_data_accounts_payable_current["taxonomy"]
    tag = concept_data_accounts_payable_current["tag"]
    company_concepts = edgar_client.get_company_concept(
        cik=cik, taxonomy=taxonomy, tag=tag
    )

    assert company_concepts["cik"] == int(cik.strip("0"))
    assert company_concepts["entityName"] == name
    assert company_concepts["taxonomy"] == taxonomy
    assert company_concepts["tag"] == tag

    assert "label" in company_concepts
    assert "description" in company_concepts
    assert "units" in company_concepts
    assert "USD" in company_concepts["units"]
    assert len(company_concepts["units"]["USD"]) > 0


def test_get_company_facts(edgar_client: EdgarClient, apple_stock: Dict[str, str]):
    cik = apple_stock["cik"]
    name = apple_stock["name"]
    company_facts = edgar_client.get_company_facts(cik=cik)

    assert company_facts["cik"] == int(cik.strip("0"))
    assert company_facts["entityName"] == name
    assert "facts" in company_facts

    facts = company_facts["facts"]
    assert "dei" in facts
    assert "us-gaap" in facts


def test_get_frames_instantaneous(
    edgar_client: EdgarClient, concept_data_accounts_payable_current: Dict[str, str]
):
    taxonomy = concept_data_accounts_payable_current["taxonomy"]
    tag = concept_data_accounts_payable_current["tag"]
    unit = concept_data_accounts_payable_current["unit"]
    year = concept_data_accounts_payable_current["year"]
    quarter = concept_data_accounts_payable_current["quarter"]
    frames = edgar_client.get_frames(
        taxonomy=taxonomy,
        tag=tag,
        unit=unit,
        year=year,
        quarter=quarter,
        instantaneous=True,
    )

    assert "label" in frames
    assert "description" in frames
    assert "pts" in frames
    assert "data" in frames

    assert frames["taxonomy"] == taxonomy
    assert frames["tag"] == tag
    assert frames["uom"] == unit
    assert frames["ccp"] == "CY2019Q1I"
    assert len(frames["data"]) > 0


def test_get_frames_not_instantaneous(
    edgar_client: EdgarClient, concept_data_gross_profit: Dict[str, str]
):
    taxonomy = concept_data_gross_profit["taxonomy"]
    tag = concept_data_gross_profit["tag"]
    unit = concept_data_gross_profit["unit"]
    year = concept_data_gross_profit["year"]
    quarter = concept_data_gross_profit["quarter"]
    frames = edgar_client.get_frames(
        taxonomy=taxonomy,
        tag=tag,
        unit=unit,
        year=year,
        quarter=quarter,
        instantaneous=False,
    )

    assert frames["ccp"] == "CY2019Q1"
    assert len(frames["data"]) > 0


def test_get_frames_entire_year(
    edgar_client: EdgarClient, concept_data_gross_profit: Dict[str, str]
):
    taxonomy = concept_data_gross_profit["taxonomy"]
    tag = concept_data_gross_profit["tag"]
    unit = concept_data_gross_profit["unit"]
    year = concept_data_gross_profit["year"]
    frames = edgar_client.get_frames(
        taxonomy=taxonomy,
        tag=tag,
        unit=unit,
        year=year,
        quarter=None,
        instantaneous=False,
    )

    assert frames["ccp"] == "CY2019"
    assert len(frames["data"]) > 0
