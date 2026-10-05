from hcis.domain.models import HistoricalDate,HistoricalQuantity,ResearchQuestion,Hypothesis,CoverageCell,GoldenCase,ResearchRun
def test_final_p0_tables_exist():
    names={c.__tablename__ for c in [HistoricalDate,HistoricalQuantity,ResearchQuestion,Hypothesis,CoverageCell,GoldenCase,ResearchRun]}
    assert names=={"historical_dates","historical_quantities","research_questions","hypotheses","coverage_cells","golden_cases","research_runs"}
