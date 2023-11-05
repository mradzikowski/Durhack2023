#!/bin/sh

alembic upgrade head

if [ ${PUBLIC_ROUTE_PATH} ]
then
  uvicorn app.main:app --proxy-headers --root-path ${PUBLIC_ROUTE_PATH} --host 0.0.0.0 --port 5500
else
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8080 --reload
fi
