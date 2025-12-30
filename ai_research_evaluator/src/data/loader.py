"""
Data loader for conference paper CSV files.
顶会论文 CSV 数据加载器
"""

import os
from pathlib import Path
from typing import Optional

import pandas as pd

from src.data.cleaner import clean_abstract, clean_keywords, clean_title, safe_int, safe_str
from src.data.schema import ConferenceData, Paper
from src.utils.exceptions import DataLoadError


# Supported conferences and their CSV file patterns
SUPPORTED_CONFERENCES = {
    "neurips": "neurips_papers.csv",
    "iclr": "iclr_papers.csv",
    "icml": "icml_papers.csv",
    "aaai": "aaai_papers.csv",
    "acl": "acl_papers.csv",
    "emnlp": "emnlp_papers.csv",
    "naacl": "naacl_papers.csv",
    "ijcai": "ijcai_papers.csv",
    "aistats": "aistats_papers.csv",
}


class PapersLoader:
    """
    Loader for conference paper CSV files.
    顶会论文 CSV 加载器
    """

    def __init__(self, data_root: Optional[str] = None):
        """
        Initialize the loader.
        
        Args:
            data_root: Root directory containing conference data.
                       Defaults to PAPERS_DATA_ROOT environment variable.
        """
        self.data_root = data_root or os.environ.get("PAPERS_DATA_ROOT", "")

    def load_csv(self, csv_path: Path) -> list[Paper]:
        """
        Load papers from a single CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            List of Paper objects
            
        Raises:
            DataLoadError: If file not found or parsing fails
        """
        csv_path = Path(csv_path)
        
        if not csv_path.exists():
            raise DataLoadError(f"CSV file not found: {csv_path}", str(csv_path))
        
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise DataLoadError(f"Failed to parse CSV: {e}", str(csv_path))
        
        papers = []
        for _, row in df.iterrows():
            try:
                paper = self._row_to_paper(row)
                papers.append(paper)
            except Exception as e:
                # Log warning but continue processing other rows
                continue
        
        return papers

    def _row_to_paper(self, row: pd.Series) -> Paper:
        """
        Convert a DataFrame row to a Paper object.
        
        Args:
            row: Pandas Series representing a row
            
        Returns:
            Paper object
        """
        return Paper(
            id=safe_str(row.get("id"), "unknown"),
            title=clean_title(row.get("title")),
            keywords=clean_keywords(row.get("keywords")),
            abstract=clean_abstract(row.get("abstract")),
            pdf=safe_str(row.get("pdf")) or None,
            forum=safe_str(row.get("forum")) or None,
            year=safe_int(row.get("year"), 2024),
            presentation_type=safe_str(row.get("presentation_type")) or None,
        )

    def load_multiple_csvs(self, csv_paths: list[Path]) -> list[Paper]:
        """
        Load papers from multiple CSV files.
        
        Args:
            csv_paths: List of paths to CSV files
            
        Returns:
            Combined list of Paper objects from all files
        """
        all_papers = []
        for path in csv_paths:
            papers = self.load_csv(path)
            all_papers.extend(papers)
        return all_papers

    def load_conference(self, conference_name: str) -> ConferenceData:
        """
        Load data for a specific conference.
        
        Args:
            conference_name: Conference name (e.g., 'neurips', 'iclr')
            
        Returns:
            ConferenceData object
            
        Raises:
            DataLoadError: If conference not supported or data not found
        """
        conf_lower = conference_name.lower()
        
        if conf_lower not in SUPPORTED_CONFERENCES:
            raise DataLoadError(
                f"Unsupported conference: {conference_name}. "
                f"Supported: {list(SUPPORTED_CONFERENCES.keys())}"
            )
        
        if not self.data_root:
            raise DataLoadError(
                "PAPERS_DATA_ROOT environment variable not set. "
                "Please set it to the path containing conference data directories."
            )
        
        csv_filename = SUPPORTED_CONFERENCES[conf_lower]
        csv_path = Path(self.data_root) / conference_name.upper() / csv_filename
        
        papers = self.load_csv(csv_path)
        
        # Extract year from papers (use most common year)
        years = [p.year for p in papers if p.year]
        year = max(set(years), key=years.count) if years else 2024
        
        return ConferenceData(
            name=conference_name.upper(),
            year=year,
            papers=papers,
        )

    def load_all_conferences(self) -> dict[str, ConferenceData]:
        """
        Load data from all supported conferences.
        
        Returns:
            Dictionary mapping conference name to ConferenceData
        """
        result = {}
        for conf_name in SUPPORTED_CONFERENCES:
            try:
                result[conf_name.upper()] = self.load_conference(conf_name)
            except DataLoadError:
                # Skip conferences that don't have data
                continue
        return result

    def get_all_papers(self) -> list[Paper]:
        """
        Get all papers from all loaded conferences.
        
        Returns:
            List of all Paper objects
        """
        conferences = self.load_all_conferences()
        all_papers = []
        for conf_data in conferences.values():
            all_papers.extend(conf_data.papers)
        return all_papers
