"""
Data models for paper and conference data.
论文和会议数据模型定义
"""

from typing import Optional

from pydantic import BaseModel, Field


class Paper(BaseModel):
    """
    Paper data model representing a single conference paper.
    单篇论文数据模型
    """

    id: str = Field(..., description="Unique identifier for the paper")
    title: str = Field(..., description="Paper title")
    keywords: list[str] = Field(default_factory=list, description="List of keywords")
    abstract: str = Field(default="", description="Paper abstract")
    pdf: Optional[str] = Field(default=None, description="PDF URL")
    forum: Optional[str] = Field(default=None, description="Forum/discussion URL")
    year: int = Field(..., description="Publication year")
    presentation_type: Optional[str] = Field(
        default=None, description="Presentation type (Oral/Poster/Spotlight)"
    )

    class Config:
        """Pydantic model configuration."""

        str_strip_whitespace = True


class ConferenceData(BaseModel):
    """
    Conference data model containing multiple papers.
    会议数据模型，包含多篇论文
    """

    name: str = Field(..., description="Conference name (e.g., NeurIPS, ICLR)")
    year: int = Field(..., description="Conference year")
    papers: list[Paper] = Field(default_factory=list, description="List of papers")

    @property
    def paper_count(self) -> int:
        """Return the number of papers in this conference."""
        return len(self.papers)

    def get_papers_by_keyword(self, keyword: str) -> list[Paper]:
        """
        Filter papers containing the specified keyword.
        
        Args:
            keyword: Keyword to search for (case-insensitive)
            
        Returns:
            List of papers containing the keyword
        """
        keyword_lower = keyword.lower()
        return [
            paper
            for paper in self.papers
            if any(keyword_lower in kw.lower() for kw in paper.keywords)
        ]

    def get_papers_by_presentation_type(self, ptype: str) -> list[Paper]:
        """
        Filter papers by presentation type.
        
        Args:
            ptype: Presentation type (Oral/Poster/Spotlight)
            
        Returns:
            List of papers with matching presentation type
        """
        return [
            paper
            for paper in self.papers
            if paper.presentation_type and paper.presentation_type.lower() == ptype.lower()
        ]
