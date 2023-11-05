import joblib

from app.deps import get_db
from app.machine_learning_models.predictorr import predict_the_model, training_the_model
from app.models.fixtures import Fixture, FixtureResult, format_date_string
from app.schemas.fixtures import FixtureResponse, FrontendFixtureResponse
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_logger

logger = get_logger("Fixtures Router")

router = APIRouter()


@router.get(
    "/retrain",
)
async def retraining_the_model(
    background_tasks: BackgroundTasks,
):
    logger.info("Retraining the model in the background...")
    background_tasks.add_task(training_the_model)


@router.get(
    "/prediction/{first_team}/{second_team}/{number_of_fixtures}/{date}",
    response_model=FrontendFixtureResponse,
)
async def retrieving_last_fixtures_between_teams(
    first_team: str,
    second_team: str,
    date: str,
    number_of_fixtures: int = 5,
    db_session: AsyncSession = Depends(get_db),
):
    home_fixtures: list[Fixture] = await Fixture.find_fixtures_for_team_home(
        db_session=db_session,
        team=first_team,
    )
    away_fixtures: list[Fixture] = await Fixture.find_fixtures_for_team_away(
        db_session=db_session,
        team=second_team,
    )

    predicted_ftag, predicted_fthg = await predict_the_model(
        home_team=first_team,
        away_team=second_team,
        date=format_date_string(date),
        model_FTAG=joblib.load('predicting_fthg.pkl'),
        model_FTHG=joblib.load('predicting_ftag.pkl'),
        fixture=None,
    )


    return {
        "last_fixtures_home": await Fixture.find_fixtures_by_team(
            db_session=db_session,
            team=first_team,
            number_of_fixtures=number_of_fixtures,
        ),
        "last_fixtures_away": await Fixture.find_fixtures_by_team(
            db_session=db_session,
            team=second_team,
            number_of_fixtures=number_of_fixtures,
        ),
        "last_fixtures_between": await Fixture.find_fixtures_by_teams(
            db_session=db_session,
            first_team=first_team,
            second_team=second_team,
            number_of_fixtures=number_of_fixtures,
        ),
        "last_fixtures_home_home": await Fixture.find_fixtures_by_team_home(
            db_session=db_session,
            number_of_fixtures=number_of_fixtures,
            team=first_team,
        ),
        "last_fixtures_away_away": await Fixture.find_fixtures_by_team_away(
            db_session=db_session,
            number_of_fixtures=number_of_fixtures,
            team=second_team,
        ),
        "predicted_score": {
            "home": round(predicted_fthg),
            "away": round(predicted_ftag),
        },
        "home_ratio": {
            "win": len(
                [fix for fix in home_fixtures if fix.result == FixtureResult.HOME],
            ),
            "draw": len(
                [fix for fix in home_fixtures if fix.result == FixtureResult.DRAW],
            ),
            "lose": len(
                [fix for fix in home_fixtures if fix.result == FixtureResult.AWAY],
            ),
        },
        "away_ratio": {
            "win": len(
                [fix for fix in away_fixtures if fix.result == FixtureResult.AWAY],
            ),
            "draw": len(
                [fix for fix in away_fixtures if fix.result == FixtureResult.DRAW],
            ),
            "lose": len(
                [fix for fix in away_fixtures if fix.result == FixtureResult.HOME],
            ),
        },
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
    return await Fixture.find_fixtures_by_teams(
        db_session=db_session,
        first_team=first_team,
        second_team=second_team,
        number_of_fixtures=number_of_fixtures,
    )


@router.get(
    "/{team}/{number_of_fixtures}",
    response_model=list[FixtureResponse],
)
async def retrieving_last_fixtures_for_team(
    team: str,
    number_of_fixtures: int = 5,
    db_session: AsyncSession = Depends(get_db),
):
    return await Fixture.find_fixtures_by_team(
        db_session=db_session,
        team=team,
        number_of_fixtures=number_of_fixtures,
    )
