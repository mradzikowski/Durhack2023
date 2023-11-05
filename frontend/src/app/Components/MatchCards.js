"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Loading from "./Loading";
import imagemapping from "../Mappings/imagemapping.json";
import styles from "../page.module.css";

export default function MatchCards({ setSelected }) {
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
      "https://footballapi.pulselive.com/football/compseasons/578/teams",
    );
    setTeams(teams.data);
  };

  const getFixtures = async () => {
    const tString = teams.map((t) => t.id).join(",");
    const fixtures = await axios.get(
      `https://footballapi.pulselive.com/football/fixtures?comps=1&teams=${tString}&compSeasons=578&page=0&pageSize=20&sort=asc&statuses=U,L&altIds=true`,
    );
    setFixtures(fixtures.data.content);
  };

  const getFixtureDetails = async () => {
    const getFixtureDetails = await Promise.all(
      fixtures &&
        Array.isArray(fixtures) &&
        fixtures.map(async (fix) => {
          const data = await axios.get(
            `https://footballapi.pulselive.com/football/fixtures/${fix.id}`,
          );
          return data.data;
        }),
    );
    setFixtureInfo(getFixtureDetails);
  };

  return (
    <>
      {fixtureInfo && Array.isArray(fixtureInfo) ? (
        fixtureInfo.map((fixture) => {
          const team1ImageMap = imagemapping.find(
            (d) => d.id == fixture.teams[0].team.id,
          ).imageId;
          const team2ImageMap = imagemapping.find(
            (d) => d.id == fixture.teams[1].team.id,
          ).imageId;
          fixture.team1ImageId = team1ImageMap;
          fixture.team2ImageId = team2ImageMap;
          return (
            <div
              id={fixture.id}
              key={fixture.id}
              className={`${styles.card} click`}
              onClick={() => setSelected(fixture)}
            >
              <div style={{ textAlign: "center" }}>
                {fixture && fixture.kickoff && fixture.kickoff.label
                  ? new Date(fixture.kickoff.millis).toDateString()
                  : "To be Decided"}
              </div>
              <div style={{ display: "flex" }}>
                <div className="team">
                  <img
                    width={90}
                    height={90}
                    src={`https://resources.premierleague.com/premierleague/badges/50/t${team1ImageMap}@x2.png`}
                  />
                  <span>{fixture.teams[0].team.name}</span>
                </div>
                <div className="vs">{" VS "}</div>
                <div className="team">
                  <span>{fixture.teams[1].team.name}</span>
                  <img
                    width={90}
                    height={90}
                    src={`https://resources.premierleague.com/premierleague/badges/50/t${team2ImageMap}@x2.png`}
                  />
                </div>
              </div>
            </div>
          );
        })
      ) : (
        <Loading />
      )}
    </>
  );
}
