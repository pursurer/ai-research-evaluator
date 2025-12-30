"""
Tests for data loading module.
数据加载模块测试 (TDD - 先写测试)
"""

import json
from pathlib import Path

import pytest

from src.data.schema import Paper, ConferenceData
from src.data.loader import PapersLoader
from src.data.cleaner import clean_keywords, clean_abstract
from src.utils.exceptions import DataLoadError


class TestPaperSchema:
    """Test Paper data model."""

    def test_paper_creation_with_valid_data(self) -> None:
        """Test creating a Paper with valid data."""
        paper = Paper(
            id="test_1",
            title="Sample Paper Title",
            keywords=["Deep Learning", "NLP"],
            abstract="This is a sample abstract.",
            pdf="https://example.com/paper.pdf",
            forum="https://example.com/forum",
            year=2024,
            presentation_type="Oral",
        )
        assert paper.id == "test_1"
        assert paper.title == "Sample Paper Title"
        assert paper.keywords == ["Deep Learning", "NLP"]
        assert paper.year == 2024

    def test_paper_with_optional_fields(self) -> None:
        """Test Paper with optional fields as None."""
        paper = Paper(
            id="test_2",
            title="Minimal Paper",
            keywords=[],
            abstract="",
            pdf=None,
            forum=None,
            year=2024,
            presentation_type=None,
        )
        assert paper.pdf is None
        assert paper.presentation_type is None

    def test_paper_keywords_must_be_list(self) -> None:
        """Test that keywords must be a list."""
        paper = Paper(
            id="test_3",
            title="Test",
            keywords=["single"],
            abstract="",
            pdf=None,
            forum=None,
            year=2024,
            presentation_type=None,
        )
        assert isinstance(paper.keywords, list)


class TestCleanFunctions:
    """Test data cleaning functions."""

    def test_clean_keywords_from_json_string(self) -> None:
        """Test parsing keywords from JSON string format."""
        raw = '["Deep Learning", "NLP", "Transformers"]'
        result = clean_keywords(raw)
        assert result == ["Deep Learning", "NLP", "Transformers"]

    def test_clean_keywords_already_list(self) -> None:
        """Test keywords that are already a list."""
        raw = ["Deep Learning", "NLP"]
        result = clean_keywords(raw)
        assert result == ["Deep Learning", "NLP"]

    def test_clean_keywords_empty_string(self) -> None:
        """Test empty string returns empty list."""
        result = clean_keywords("")
        assert result == []

    def test_clean_keywords_none(self) -> None:
        """Test None returns empty list."""
        result = clean_keywords(None)
        assert result == []

    def test_clean_keywords_malformed_json(self) -> None:
        """Test malformed JSON returns empty list."""
        raw = '["broken'
        result = clean_keywords(raw)
        assert result == []

    def test_clean_abstract_removes_extra_whitespace(self) -> None:
        """Test abstract cleaning removes extra whitespace."""
        raw = "  This   has   extra   spaces.  \n\n"
        result = clean_abstract(raw)
        assert result == "This has extra spaces."

    def test_clean_abstract_none(self) -> None:
        """Test None abstract returns empty string."""
        result = clean_abstract(None)
        assert result == ""


class TestPapersLoader:
    """Test PapersLoader class."""

    def test_load_single_csv(self, test_data_dir: Path) -> None:
        """Test loading a single CSV file."""
        loader = PapersLoader()
        csv_path = test_data_dir / "sample_papers.csv"
        papers = loader.load_csv(csv_path)
        
        assert len(papers) == 3
        assert all(isinstance(p, Paper) for p in papers)

    def test_load_csv_parses_keywords(self, test_data_dir: Path) -> None:
        """Test that keywords are correctly parsed from JSON string."""
        loader = PapersLoader()
        csv_path = test_data_dir / "sample_papers.csv"
        papers = loader.load_csv(csv_path)
        
        # First paper should have parsed keywords
        assert isinstance(papers[0].keywords, list)
        assert "Video Generation" in papers[0].keywords

    def test_load_csv_file_not_found(self) -> None:
        """Test DataLoadError raised for missing file."""
        loader = PapersLoader()
        with pytest.raises(DataLoadError) as exc_info:
            loader.load_csv(Path("/nonexistent/path.csv"))
        assert "not found" in str(exc_info.value).lower()

    def test_load_conference_by_name(self, test_data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading conference data by name."""
        # Mock the data root to use test data
        monkeypatch.setenv("PAPERS_DATA_ROOT", str(test_data_dir.parent))
        
        loader = PapersLoader()
        # This test will be skipped if real data is not available
        # In production, it would load from PAPERS_DATA_ROOT/NeurIPS/neurips_papers.csv

    def test_load_all_conferences(self, test_data_dir: Path) -> None:
        """Test loading multiple conference CSVs."""
        loader = PapersLoader()
        # Load multiple CSVs
        csv_files = [test_data_dir / "sample_papers.csv"]
        all_papers = loader.load_multiple_csvs(csv_files)
        
        assert len(all_papers) == 3

    def test_get_papers_by_year(self, test_data_dir: Path) -> None:
        """Test filtering papers by year."""
        loader = PapersLoader()
        csv_path = test_data_dir / "sample_papers.csv"
        papers = loader.load_csv(csv_path)
        
        papers_2024 = [p for p in papers if p.year == 2024]
        assert len(papers_2024) == 3

    def test_get_papers_by_keyword(self, test_data_dir: Path) -> None:
        """Test filtering papers by keyword."""
        loader = PapersLoader()
        csv_path = test_data_dir / "sample_papers.csv"
        papers = loader.load_csv(csv_path)
        
        # Filter papers containing "Video Generation" keyword
        video_papers = [p for p in papers if "Video Generation" in p.keywords]
        assert len(video_papers) >= 1


class TestConferenceData:
    """Test ConferenceData model."""

    def test_conference_data_creation(self) -> None:
        """Test creating ConferenceData."""
        papers = [
            Paper(
                id="1", title="Test", keywords=[], abstract="",
                pdf=None, forum=None, year=2024, presentation_type=None
            )
        ]
        conf = ConferenceData(
            name="NeurIPS",
            year=2024,
            papers=papers,
        )
        assert conf.name == "NeurIPS"
        assert len(conf.papers) == 1

    def test_conference_data_paper_count(self) -> None:
        """Test paper_count property."""
        papers = [
            Paper(id="1", title="T1", keywords=[], abstract="", pdf=None, forum=None, year=2024, presentation_type=None),
            Paper(id="2", title="T2", keywords=[], abstract="", pdf=None, forum=None, year=2024, presentation_type=None),
        ]
        conf = ConferenceData(name="ICLR", year=2024, papers=papers)
        assert conf.paper_count == 2
