import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error

from app.db.session import async_session
from app.models.fixtures import Fixture, format_date_string
from app.utils import get_logger

logger = get_logger("Predictor")


async def get_data_from_database() -> list[Fixture]:
    async with async_session() as session:
        fixtures: list[Fixture] = await Fixture.find_all(db_session=session)
        return fixtures


async def convert_data_to_pandas_dataframe() -> pd.DataFrame:
    fixtures = await get_data_from_database()
    data = []
    for fixture in fixtures:
        data.append(
            {
                "date": fixture.date,
                "home_team": fixture.home_team,
                "away_team": fixture.away_team,
                "full_time_home_goals": fixture.full_time_home_goals,
                "full_time_away_goals": fixture.full_time_away_goals,
            },
        )
    return pd.DataFrame(data)


async def training_the_model():
    data = await convert_data_to_pandas_dataframe()
    data['date'] = pd.to_datetime(data['date']).map(pd.Timestamp.toordinal)
    X = data[['home_team', 'away_team', 'date']]

    y_FTHG = data['full_time_home_goals']
    y_FTAG = data['full_time_away_goals']

    categorical_features = ['home_team', 'away_team']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ],
        remainder='passthrough'
    )

    X_train, X_test, y_home_train, y_home_test, y_away_train, y_away_test = train_test_split(
        X, y_FTHG, y_FTAG, test_size=0.2, random_state=42)

    model_home = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('regressor', RandomForestRegressor(random_state=42))])
    model_away = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('regressor', RandomForestRegressor(random_state=42))])


    model_home.fit(X_train, y_home_train)
    model_away.fit(X_train, y_away_train)

    y_home_pred = model_home.predict(X_test)
    y_away_pred = model_away.predict(X_test)

    home_mse = mean_squared_error(y_home_test, y_home_pred)
    away_mse = mean_squared_error(y_away_test, y_away_pred)

    logger.info(f"Home Goals Prediction MSE: {home_mse}")
    logger.info(f"Away Goals Prediction MSE: {away_mse}")

    joblib.dump(model_home, 'predicting_fthg.pkl')
    joblib.dump(model_away, 'predicting_ftag.pkl')
    joblib.dump(preprocessor, 'preprocessor.pkl')

    return model_home, model_away


async def predict_the_model(fixture: Fixture | None, model_FTHG, model_FTAG, home_team, away_team, date):
    date = format_date_string(date)
    if fixture:
        data = [{
            "date": fixture.date,
            "home_team": fixture.home_team,
            "away_team": fixture.away_team,
        }]
    else:
        data = [{
            "date": date,
            "home_team": home_team,
            "away_team": away_team,
        }]

    data[0]['date'] = pd.to_datetime(data[0]['date']).toordinal()

    data = pd.DataFrame(data)

    predictions_fthg = model_FTHG.predict(data)
    predictions_ftag = model_FTAG.predict(data)

    logger.info(f"Data predicted fthg {predictions_fthg}")
    logger.info(f"Data predicted ftag {predictions_ftag}")

    logger.info(f"Predicted FTHG: {predictions_fthg[0]}")
    logger.info(f"Predicted FTAG: {predictions_ftag[0]}")

    return (predictions_fthg[0], predictions_ftag[0])

