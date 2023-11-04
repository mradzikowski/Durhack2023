"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Loading from "./Loading";

export default function Lander() {
  const [teams, setTeams] = useState(null);
  const [fixtures, setFixtures] = useState(null);
  const [fixtureInfo, setFixtureInfo] = useState(null);

  useEffect(() => {
    getTeams();
  }, []);

  useEffect(() => {
    if (teams) {
      getFixtures();
    }
  }, [teams]);

  useEffect(() => {
    if (fixtures) {
      getFixtureDetails();
    }
  }, [fixtures]);

  const getTeams = async () => {
    const teams = await axios.get(
      "https://footballapi.pulselive.com/football/compseasons/578/teams"
    );
    setTeams(teams.data);
  };

  const getFixtures = async () => {
    const tString = teams.map((t) => t.id).join(",");
    const fixtures = await axios.get(
      `https://footballapi.pulselive.com/football/fixtures?comps=1&teams=${tString}&compSeasons=578&page=0&pageSize=20&sort=asc&statuses=U,L&altIds=true`
    );
    setFixtures(fixtures.data.content);
  };

  const getFixtureDetails = async () => {
    const getFixtureDetails = await Promise.all(
      fixtures &&
        Array.isArray(fixtures) &&
        fixtures.map(async (fix) => {
          const data = await axios.get(
            `https://footballapi.pulselive.com/football/fixtures/${fix.id}`
          );
          return data.data;
        })
    );
    setFixtureInfo(getFixtureDetails);
  };
  return (
    <div>
      {fixtureInfo && Array.isArray(fixtureInfo) ? (
        fixtureInfo.map((fixture) => {
          return (
            <div id={fixture.id}>
              <span>{fixture.teams[0].team.name}</span>
              {" VS "}
              <span>{fixture.teams[1].team.name}</span>
              <span>{new Date(fixture.kickoff.millis).toUTCString()}</span>
            </div>
          );
        })
      ) : (
        <Loading/>
      )}
    </div>
  );
}
