"""SQLAlchemy models for the application."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    JSON,
    Date,
    Float,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .database import Base

class Project(Base):
    """SQLAlchemy model for the 'projects' table."""
    __tablename__ = 'projects'

    id = Column(BigInteger, primary_key=True)
    workspace_id = Column(BigInteger)
    client_id = Column(BigInteger, nullable=True)
    name = Column(String)
    is_private = Column(Boolean)
    active = Column(Boolean)
    at = Column(DateTime)
    created_at = Column(DateTime)
    server_deleted_at = Column(DateTime, nullable=True)
    color = Column(String)
    billable = Column(Boolean)
    template = Column(String, nullable=True)
    auto_estimates = Column(Boolean, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    estimated_seconds = Column(Integer, nullable=True)
    rate = Column(Float, nullable=True)
    rate_last_updated = Column(DateTime, nullable=True)
    currency = Column(String, nullable=True)
    recurring = Column(Boolean)
    template_id = Column(BigInteger, nullable=True)
    recurring_parameters = Column(String, nullable=True)
    fixed_fee = Column(Float, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    actual_seconds = Column(Integer, nullable=True)
    total_count = Column(Integer)
    client_name = Column(String, nullable=True)
    can_track_time = Column(Boolean)
    start_date = Column(Date)
    status = Column(String)
    wid = Column(BigInteger)
    cid = Column(BigInteger, nullable=True)
    integration_provider = Column(String)
    pinned = Column(Boolean)

    time_entries = relationship("TimeEntry", back_populates="project")

    def __repr__(self):
        return f'<Project {self.name!r}>'

class TimeEntry(Base):
    """SQLAlchemy model for the 'time_entries' table."""
    __tablename__ = 'time_entries'

    id = Column(BigInteger, primary_key=True)
    workspace_id = Column(BigInteger)
    project_id = Column(BigInteger, ForeignKey('projects.id'))
    task_id = Column(BigInteger, nullable=True)
    billable = Column(Boolean)
    start = Column(DateTime)
    stop = Column(DateTime)
    duration = Column(Integer) # seconds
    description = Column(String)
    tags = Column(JSON)
    tag_ids = Column(JSON)
    duronly = Column(Boolean)
    at = Column(DateTime)
    server_deleted_at = Column(DateTime, nullable=True)
    user_id = Column(BigInteger)
    uid = Column(BigInteger)
    wid = Column(BigInteger)
    pid = Column(BigInteger)

    project = relationship("Project", back_populates="time_entries")

    def __repr__(self):
        return f'<Time Entry {self.description!r}>'
