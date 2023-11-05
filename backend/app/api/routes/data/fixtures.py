from app.deps import get_db
from app.models.fixtures import Fixture
from app.schemas.fixtures import FixtureResponse, FrontendFixtureResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "/prediction/{first_team}/{second_team}/{number_of_fixtures}",
    response_model=FrontendFixtureResponse,
)
async def retrieving_last_fixtures_between_teams(
    first_team: str,
    second_team: str,
    number_of_fixtures: int = 5,
    db_session: AsyncSession = Depends(get_db),
):

    return {
        "last_fixtures_home": await Fixture.find_fixtures_by_team(db_session=db_session, team=first_team, number_of_fixtures=number_of_fixtures),
        "last_fixtures_away": await Fixture.find_fixtures_by_team(db_session=db_session, team=second_team, number_of_fixtures=number_of_fixtures),
        "last_fixtures_between": await Fixture.find_fixtures_by_teams(db_session=db_session, first_team=first_team, second_team=second_team, number_of_fixtures=number_of_fixtures),
        "last_fixtures_home_home": await Fixture.find_fixtures_by_team_home(db_session=db_session, number_of_fixtures=number_of_fixtures, team=first_team),
        "last_fixtures_away_away": await Fixture.find_fixtures_by_team_away(db_session=db_session, number_of_fixtures=number_of_fixtures, team=second_team),
        "predicted_score": {
            "home": 1,
            "away": 0,
        }
    }



@router.get(
    "/",
    response_model=list[FixtureResponse],
)
async def retrieving_all_fixtures(
    db_session: AsyncSession = Depends(get_db),
):
    return await Fixture.find_all(db_session=db_session)


@router.get(
    "/{first_team}/{second_team}/{number_of_fixtures}",
    response_model=list[FixtureResponse],
)
async def retrieving_last_fixtures_between_teams(
    first_team: str,
    second_team: str,
    number_of_fixtures: int = 5,
    db_session: AsyncSession = Depends(get_db),
):
    return await Fixture.find_fixtures_by_teams(db_session=db_session, first_team=first_team, second_team=second_team, number_of_fixtures=number_of_fixtures)


@router.get(
    "/{team}/{number_of_fixtures}",
    response_model=list[FixtureResponse],
)
async def retrieving_last_fixtures_for_team(
    team: str,
    number_of_fixtures: int = 5,
    db_session: AsyncSession = Depends(get_db),
):
    return await Fixture.find_fixtures_by_team(db_session=db_session, team=team, number_of_fixtures=number_of_fixtures)
