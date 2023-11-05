import csv
import os

from app.db.session import async_session
from app.models.fixtures import Fixture
from app.utils import get_logger

logger = get_logger("Init DB")

csv_file = "app/dataset/combined_data.csv"


async def init_database_on_startup():
    logger.info("Initializing database on startup...")
    async with async_session() as session:
        with open(csv_file, newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            _ = next(csv_reader)  # Skip the header row

            # Iterate over the CSV rows
            for row in csv_reader:
                # Assuming the CSV columns match the columns of the table
                date = row[1].split("/")
                date = date[2] + "-" + date[1] + "-" + date[0]

                does_data_exist = await Fixture.check_if_the_fixture_exists(
                    db_session=session,
                    first_team=row[2],
                    second_team=row[3],
                    date=date,
                )
                if not does_data_exist:
                    data = Fixture(
                        home_team=row[2],
                        away_team=row[3],
                        date=date,
                        full_time_home_goals=int(row[4]),
                        full_time_away_goals=int(row[5]),
                    )
                    session.add(data)
                else:
                    logger.info(
                        f"Data already exists for {row[2]} vs {row[3]} on {date}. Duplicate data not added.",
                    )
        await session.commit()
