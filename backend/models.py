from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    season_year = Column(Integer, unique=True, nullable=False)

class NFLTeam(Base):
    __tablename__ = "nfl_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, nullable=False)
    conference = Column(String, nullable=False)
    division = Column(String, nullable=False)


class NFLPlayer(Base):
    __tablename__ = "nfl_players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=False)


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    join_code = Column(String, unique=True, nullable=False, index=True)