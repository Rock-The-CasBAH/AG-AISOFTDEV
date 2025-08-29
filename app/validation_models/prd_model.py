from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExecutiveSummaryAndVision(BaseModel):
    """A high-level overview for stakeholders about the product's purpose, core problem it solves, and target user base."""
    summary: str

class ProblemStatement(BaseModel):
    """Detailed description of the primary problem the product aims to solve."""
    statement: str
    user_personas: List[str]
    scenarios: List[str]

class SuccessMetric(BaseModel):
    """Defines the goals and their respective key performance indicators and targets."""
    goal: str
    kpi: str
    target: str

class UserStory(BaseModel):
    """Representation of an Agile user story with acceptance criteria."""
    story: str
    acceptance_criteria: List[str]

class FunctionalRequirements(BaseModel):
    """Details what the product must do, broken down into actionable user stories."""
    user_stories: List[UserStory]

class NonFunctionalRequirements(BaseModel):
    """The qualities and constraints of the system, such as performance, security, and scalability."""
    performance: str
    security: str
    accessibility: str
    scalability: str

class ReleaseMilestone(BaseModel):
    """High-level timeline for delivery of different versions."""
    version: str
    target_date: Optional[str]
    features: List[str]

class OutOfScope(BaseModel):
    """Defines what is not included in the current version to prevent scope creep."""
    out_of_scope: List[str]
    future_work: List[str]

class Appendix(BaseModel):
    """Tracks dependencies, assumptions, and open questions related to the PRD."""
    open_questions: List[str]
    dependencies: List[str]

class ProductRequirementsDocument(BaseModel):
    """Pydantic model for a Product Requirements Document (PRD)."""
    product_name: str = Field(..., description="Name of the product")
    status: str = Field(..., description="Current status of the document, e.g., Draft")
    author: str = Field(..., description="Author or team responsible for the document")
    version: float = Field(..., description="Version number of the document")
    last_updated: Optional[str] = Field(None, description="Last updated date")

    executive_summary_and_vision: ExecutiveSummaryAndVision
    problem_statement: ProblemStatement
    success_metrics: List[SuccessMetric]
    functional_requirements: FunctionalRequirements
    non_functional_requirements: NonFunctionalRequirements
    release_plan_and_milestones: List[ReleaseMilestone]
    out_of_scope_and_future_considerations: OutOfScope
    appendix_and_open_questions: Appendix