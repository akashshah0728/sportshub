from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, Date, Boolean, UniqueConstraint, DateTime
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

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=False)
    kickoff_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(
        Enum("scheduled", "in_progress", "concluded", name="game_status_enum"),
        nullable=False,
        default="scheduled",
    )
    outcome = Column(
        Enum("home_win", "away_win", "tied", name="game_outcome_enum"),
        nullable=True,
    )
    home_team_odds = Column(Integer, nullable=False)
    away_team_odds = Column(Integer, nullable=False)

class CustomPrediction(Base):
    __tablename__ = "custom_predictions"

    id = Column(Integer, primary_key=True, index=True)
    league_member_id = Column(Integer, ForeignKey("league_members.id"), nullable=False)
    prediction = Column(String, nullable=False)
    bold_level = Column(
        Enum("mild", "hot", "red_hot", "moronic", name = "bold_level_enum"),
        nullable=False,
        )

class SetPrediction(Base):
    __tablename__ = "set_predictions"

    id = Column(Integer, primary_key=True, index=True)
    league_member_id = Column(Integer, ForeignKey("league_members.id"), nullable=False)
    category = Column(
        Enum(
            "last_undefeated_team",
            "first_coach_fired",
            "super_bowl_champion",
            "longest_losing_streak",
            "longest_win_streak",
            "longest_field_goal",
            "best_record",
            "worst_record",
            "first_qb_benched",
            "mvp",
            "dpoy",
            "nfc_champion",
            "afc_champion",
            name="set_prediction_category_enum",
        ),
        nullable=False,
    )
    predicted_team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=True)
    predicted_player_id = Column(Integer, ForeignKey("nfl_players.id"), nullable=True)
    predicted_text = Column(String, nullable=True)

class PrizeMoney(Base):
    __tablename__ = "prize_money"

    id = Column(Integer, primary_key=True, index=True)
    league_member_id = Column(Integer, ForeignKey("league_members.id"), nullable=False)
    usd_winnings = Column(Numeric(10,2), nullable=False)

class Wager(Base):
    __tablename__ = "wagers"
    __table_args__ = (
        UniqueConstraint("league_member_id", "game_id", name="uq_wager_per_game"),
    )

    id = Column(Integer, primary_key=True, index=True)
    league_member_id = Column(Integer, ForeignKey("league_members.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    selected_team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=False)
    amount_wagered = Column(Numeric(10, 2), nullable=False)
    moneyline_odds = Column(Integer, nullable=False)
    status = Column(
        Enum("pending", "won", "lost", "push", name="wager_status_enum"),
        nullable=False,
        default="pending",
    )
    payout = Column(Numeric(10, 2), nullable=False)
    is_insured = Column(Boolean, nullable=False, default=False)
    insurance_refund_amount = Column(Numeric(10, 2), nullable=True)


class PostseasonPrediction(Base):
    __tablename__ = "postseason_predictions"
    __table_args__ = (
        UniqueConstraint("league_member_id", "game_id", name="uq_postseason_prediction_per_game"),
    )

    id = Column(Integer, primary_key=True, index=True)
    league_member_id = Column(Integer, ForeignKey("league_members.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    selected_team_id = Column(Integer, ForeignKey("nfl_teams.id"), nullable=False)
    status = Column(
        Enum("pending", "correct", "incorrect", name="postseason_prediction_status_enum"),
        nullable=False,
        default="pending",
    )