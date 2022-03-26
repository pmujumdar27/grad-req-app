from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(String, nullable=False, unique=True)
    course_name = Column(String, nullable=False)
    course_credits = Column(Integer, nullable=False)
    sem_offered = Column(String, nullable=False)
    is_bs = Column(Boolean, server_default="False", nullable=False)
    is_hs = Column(Boolean, server_default="False", nullable=False)

class ProgramMajor(Base):
    __tablename__ = "programmajor"

    id = Column(Integer, primary_key=True, nullable=False)
    major_code = Column(String, nullable=False, unique=True)
    core_creds = Column(Integer, nullable=False)
    ext_core_creds = Column(Integer, nullable=False)
    bs_creds = Column(Integer, nullable=False)
    hs_creds = Column(Integer, nullable=False)
    open_creds = Column(Integer, nullable=False)

class ProgramMinor(Base):
    __tablename__ = "programminor"

    id = Column(Integer, primary_key=True, nullable=False)
    minor_code = Column(String, nullable=False, unique=True)

class CoreRel(Base):
    __tablename__ = "corerel"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    major_id = Column(Integer, ForeignKey("programmajor.id", ondelete="CASCADE"), nullable=False)

class ExtCoreRel(Base):
    __tablename__ = "extcorerel"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    major_id = Column(Integer, ForeignKey("programmajor.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    program_major = Column(String, ForeignKey("programmajor.major_code", ondelete="CASCADE"), nullable=False)
    program_minor = Column(String, ForeignKey("programminor.minor_code", ondelete="CASCADE"), nullable=False)

class CourseTypes(Base):
    __tablename__ = "coursetypes"

    id = Column(Integer, primary_key=True, nullable=False)
    count_towards = Column(String, nullable = False, unique=True)

class SelectedCourse(Base):
    __tablename__ = "selectedcourses"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"))
    semester = Column(Integer, nullable=False)
    count_towards = Column(String, ForeignKey("coursetypes.count_towards", ondelete="CASCADE"), nullable=False)
