import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

projects_users = Table('projects_users', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id', ondelete = 'CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete = 'CASCADE'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    sub = Column(String, nullable = False)
    email = Column(String)
    name = Column(String)
    avatar = Column(String)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    desc = Column(String)

    users = relationship("User", secondary = projects_users)

class SourceType(enum.Enum):

    GITLAB = 'gitlab'

class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    type = Column(Enum(SourceType), nullable = False)
    config = Column(JSON, nullable = False)

class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    desc = Column(String, default = '')
    project_id = Column(Integer, ForeignKey('projects.id', ondelete = 'CASCADE'), nullable = False)
    reporter_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    assignee_id = Column(Integer, ForeignKey('users.id', ondelete = 'SET NULL'))
    status = Column(String, default = 'todo', nullable = False)
    rank = Column(Integer, default = 0)
    status_date = Column(DateTime, default = datetime.now, nullable = False)

    project = relationship("Project", backref = "issues")

class TimeEntry(Base):
    __tablename__ = 'time_entries'

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id', ondelete = 'SET NULL'))
    project_id = Column(Integer, ForeignKey('projects.id', ondelete = 'CASCADE'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    start = Column(DateTime, default = datetime.now)
    end = Column(DateTime)

    issue = relationship("Issue", backref = "time_entries")
    project = relationship("Project", backref = "time_entries")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete = 'CASCADE'), nullable = False)
    created_user_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    paid_user_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    amount = Column(Integer, nullable = False)
    time = Column(DateTime, default = datetime.now)
    note = Column(String, default = '')

    project = relationship("Project", backref = "payments")

class ProjectInvitationToken(Base):

    __tablename__ = 'project_invitation_tokens'

    id = Column(Integer, primary_key = True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete = 'CASCADE'), nullable = False)
    token = Column(String, nullable = False)

    project = relationship("Project", backref = "tokens")
