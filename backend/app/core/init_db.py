import csv
import os

from app.db.session import async_session
from app.models.fixtures import Fixture

csv_file = "app/dataset/combined_data.csv"

async def init_database_on_startup():
    async with async_session() as session:
        # Display the files in the directory

        # print(os.listdir(f"app/core/"))
        if os.path.isfile(csv_file):
            print("File exists")
        else:
            print("File does not exist")

        with open(csv_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            _ = next(csv_reader)  # Skip the header row

            # Iterate over the CSV rows
            for row in csv_reader:
                # Assuming the CSV columns match the columns of the table
                date = row[1].split("/")
                date = date[2] + "-" + date[1] + "-" + date[0]
                data = Fixture(
                    home_team=row[2],
                    away_team=row[3],
                    date=date,
                    full_time_home_goals=int(row[4]),
                    full_time_away_goals=int(row[5]),
                )
                session.add(data)
        await session.commit()