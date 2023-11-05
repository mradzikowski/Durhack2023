import uuid as uuid
from enum import Enum

from models.base import Base
from sqlalchemy import Column, Integer, String, and_, or_, select
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_logger

logger = get_logger("Fixture Model")


class FixtureResult(Enum):
    HOME = 0
    DRAW = 1
    AWAY = 2


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
        self.date = date
        self.result = self.get_result(
            home_goals=full_time_home_goals,
            away_goals=full_time_away_goals,
        )

    @classmethod
    async def find_fixtures_by_teams(
        cls,
        db_session: AsyncSession,
        first_team: str,
        second_team: str,
        number_of_fixtures: int,
    ):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = (
            select(cls)
            .where(
                or_(
                    and_(
                        cls.home_team == first_team,
                        cls.away_team == second_team,
                    ),
                    and_(
                        cls.home_team == second_team,
                        cls.away_team == first_team,
                    ),
                ),
                # and_(
                #     cls.home_team.in_([first_team, second_team]),
                # )
            )
            .order_by(cls.date.desc())
            .limit(number_of_fixtures)
        )
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_by_team(
        cls,
        db_session: AsyncSession,
        team: str,
        number_of_fixtures: int,
    ):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = (
            select(cls)
            .where(
                or_(
                    cls.home_team == team,
                    cls.away_team == team,
                ),
            )
            .order_by(cls.date.desc())
            .limit(number_of_fixtures)
        )
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_by_team_home(
        cls,
        db_session: AsyncSession,
        team: str,
        number_of_fixtures: int,
    ):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = (
            select(cls)
            .where(
                cls.home_team == team,
            )
            .order_by(cls.date.desc())
            .limit(number_of_fixtures)
        )
        result = await db_session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def find_fixtures_by_team_away(
        cls,
        db_session: AsyncSession,
        team: str,
        number_of_fixtures: int,
    ):
        """
        Find the last number_of_fixtures fixtures between the two teams
        :param db_session: asynchronous db session
        :param first_team: first team
        :param second_team: second team
        :param number_of_fixtures: number of fixtures
        :return: list of fixtures
        """
        query = (
            select(cls)
            .where(
                cls.away_team == team,
            )
            .order_by(cls.date.desc())
            .limit(number_of_fixtures)
        )
        result = await db_session.execute(query)
        return list(result.scalars().all())

    def get_result(self, home_goals: int, away_goals: int) -> FixtureResult:
        if home_goals > away_goals:
            return FixtureResult.HOME
        elif home_goals < away_goals:
            return FixtureResult.AWAY
        else:
            return FixtureResult.DRAW
