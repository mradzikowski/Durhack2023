import uuid

from pydantic import BaseModel, Field

from app.models.fixtures import FixtureResult


class FixtureCreate(BaseModel):
    home_team: str | None = None
    away_team: str | None = None
    full_time_home_goals: int | None = None
    full_time_away_goals: int | None = None
    date: str | None = None
    result: FixtureResult | int | None = None


class FixtureResponse(FixtureCreate):
    id: uuid.UUID = Field(..., title="ID of the receipt")


class PredictedScore(BaseModel):
    home: int | None = None
    away: int | None = None


class FrontendFixtureResponse(BaseModel):
    last_fixtures_home: list[FixtureResponse] | None = None
    last_fixtures_away: list[FixtureResponse] | None = None
    last_fixtures_between: list[FixtureResponse] | None = None
    last_fixtures_home_home: list[FixtureResponse] | None = None
    last_fixtures_away_away: list[FixtureResponse] | None = None
    predicted_score: PredictedScore | None = None


