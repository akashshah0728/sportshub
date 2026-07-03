from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, Date, Boolean, UniqueConstraint
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

class LeagueMember(Base):
    __tablename__ = "league_members"
    __table_args__ = (
        UniqueConstraint('league_id', "user_id", "season_id", name="uq_league_member_per_season"),
    )

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    member_role = Column(
        Enum("commissioner", "player", name="member_role_enum"),
        nullable=False,
    )
    buy_in_amount = Column(Numeric(10, 2), nullable=False)
    initial_seed_money = Column(Numeric(12, 2), nullable=False)

class LeagueRule(Base):
    __tablename__ = "league_rules"
    __table_args__ = (
        UniqueConstraint("league_id", "season_id", name="uq_league_rule_per_season"),
    )

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    global_minimum_wager = Column(Numeric(10, 2), nullable=False)
    favorite_odds_threshold = Column(Integer, nullable=False)
    favorite_odds_ceiling = Column(Integer, nullable=False)
    predictions_lock_date = Column(Date, nullable=False)
    usd_to_seed_money_conversion = Column(Numeric(10, 4), nullable=False)
    minimum_usd_buy_in = Column(Numeric(10, 2), nullable=False)
    maximum_insurance_refund = Column(Numeric(10, 2), nullable=False)
    postseason_wagering_enabled = Column(Boolean, nullable=False, default=False)

class InsuranceRule(Base):
    __tablename__ = "insurance_rules"
    __table_args__ = (
        UniqueConstraint("league_id", "season_id", "week_number", name="uq_insurance_rule_per_week"),
    )

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    insurance_allowance = Column(Integer, nullable=False)

class Week(Base):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    week_status = Column(
        Enum("active", "concluded", name="week_status_enum"),
        nullable=False,
    )
    is_postseason = Column(Boolean, nullable=False, default=False)