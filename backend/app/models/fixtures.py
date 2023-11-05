import uuid as uuid
from enum import Enum

from dateutil import parser
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.utils import get_logger
from sqlalchemy import Column, Integer, String, select, and_, or_
from sqlalchemy.dialects.postgresql import ENUM, UUID

logger = get_logger("Fixture Model")


class FixtureResult(Enum):
    HOME = 0
    DRAW = 1
    AWAY = 2


def format_date_string(date_string):
    try:
        # Parse the date_string to datetime
        dt = parser.parse(date_string)
        # Format the date consistently
        return dt.strftime('%d/%m/%Y')
    except ValueError:
        # Handle the error if the date_string is not a valid date
        print("The provided string is not a recognizable date.")
        return None


class Fixture(Base):
    __tablename__ = "fixtures"  # type: ignore
    __table_args__ = {"extend_existing": True}

    id: Column[UUID] | uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    home_team: Column[String] | str = Column(String, nullable=False)
    away_team: Column[String] | str = Column(String, nullable=False)
    full_time_home_goals: Column[Integer] | int = Column(Integer, nullable=False)
    full_time_away_goals: Column[Integer] | int = Column(Integer, nullable=False)
    date: Column[String] | str = Column(String, nullable=False)
    result: Column[Enum] | str = Column(ENUM(FixtureResult), nullable=False)

    def __init__(
        self,
        home_team: str,
        away_team: str,
        full_time_home_goals: int,
        full_time_away_goals: int,
        date: str,
    ):
        self.id = uuid.uuid4()
        self.home_team = home_team
        self.away_team = away_team
        self.full_time_home_goals = full_time_home_goals
        self.full_time_away_goals = full_time_away_goals
        self.date = format_date_string(date)
        self.result = self.get_result(
            home_goals=full_time_home_goals,
            away_goals=full_time_away_goals,
        )

    @classmethod
    async def find_fixtures_by_teams(cls, db_session: AsyncSession, first_team: str, second_team: str, number_of_fixtures: int):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            or_(
                and_(
                    cls.home_team == first_team,
                    cls.away_team == second_team,
                ),
                and_(
                    cls.home_team == second_team,
                    cls.away_team == first_team,
                ),
            )
            # and_(
            #     cls.home_team.in_([first_team, second_team]),
            # )
        ).order_by(cls.date.desc()).limit(number_of_fixtures)
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def check_if_the_fixture_exists(cls, db_session: AsyncSession, first_team: str, second_team: str, date: str):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            first_team == cls.home_team,
            second_team == cls.away_team,
            format_date_string(date) == cls.date,
        ).first()
        result = await db_session.execute(query)
        value = result.scalars().first()
        return True if value else False

    @classmethod
    async def find_fixtures_by_team(cls, db_session: AsyncSession, team: str,
                               number_of_fixtures: int):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            or_(
                cls.home_team == team,
                cls.away_team == team,
            )
        ).order_by(cls.date.desc()).limit(number_of_fixtures)
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_by_team_home(cls, db_session: AsyncSession, team: str,
                                    number_of_fixtures: int):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
                cls.home_team == team,
        ).order_by(cls.date.desc()).limit(number_of_fixtures)
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_by_team_away(cls, db_session: AsyncSession, team: str,
                                         number_of_fixtures: int):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            cls.away_team == team,
        ).order_by(cls.date.desc()).limit(number_of_fixtures)
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_for_team_home(cls, db_session: AsyncSession, team: str,):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            cls.home_team == team,
        ).order_by(cls.date.desc())
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_for_team_away(cls, db_session: AsyncSession, team: str, ):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = select(cls).where(
            cls.away_team == team,
        ).order_by(cls.date.desc())
        result = await db_session.execute(query)
        return list(result.scalars().all())


    def get_result(self, home_goals: int, away_goals: int) -> FixtureResult:
        if home_goals > away_goals:
            return FixtureResult.HOME
        elif home_goals < away_goals:
            return FixtureResult.AWAY
        else:
            return FixtureResult.DRAW
