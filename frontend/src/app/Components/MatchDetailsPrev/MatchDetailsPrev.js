import React, { useEffect, useState } from "react";
import "./matchDetailsPrev.css";
import styles from "../../page.module.css";
import teamNameMapping from "../../Mappings/teamNameMapping.json";
import axios from "axios";
import PieChart from "../PieChart";
import Loading from "../Loading";

const MatchDetailsPrev = ({ selected, setSelected }) => {
  const fixture = selected;
  const team1ImageMap = selected.team1ImageId;
  const team2ImageMap = selected.team2ImageId;
  const teamOneImage = `https://resources.premierleague.com/premierleague/badges/50/t${team1ImageMap}@x2.png`;
  const teamTwoImage = `https://resources.premierleague.com/premierleague/badges/50/t${team2ImageMap}@x2.png`;
  const drawImage = "/draw.svg";

  const winImage = "/win.svg";
  const looseImage = "lose.svg";

  const [matchDetails, setMatchDetails] = useState(null);

  useEffect(() => {
    getMatchDetails();
  }, []);

  const getMatchDetails = async () => {
    let team1 = teamNameMapping.find(
      (d) => d.name == fixture.teams[0].team.name
    )
    team1 = team1 ? team1.map : fixture.teams[0].team.name
    let team2 = teamNameMapping.find(
      (d) => d.name == fixture.teams[1].team.name
    )
    team2 = team2 ? team2.map : fixture.teams[1].team.name
    const date = selected && selected.kickoff && selected.kickoff.millis ? new Date(selected.kickoff.millis).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
    const match = await axios.get(
      `http://localhost:8080/fixtures/prediction/${team1}/${team2}/5/${date}`
    );
    setMatchDetails(match.data);
  };

  return (
    <>
      {matchDetails ? (
        <>
          <div className={styles.description}>
            <p>
              Premier League&nbsp;
              <code className={styles.code}>Predictions</code>
            </p>
            <div>
              <span
                style={{ fontSize: "2rem" }}
                onClick={() => setSelected(null)}
                className="click"
              >
                &#x2715;
              </span>
            </div>
          </div>

          <div className={`gridone ${styles.grid}`}>
            <div className={styles.card}>
              <h2 style={{ textAlign: "center" }}>
                {selected.kickoff.millis
                  ? new Date(selected.kickoff.millis).toDateString()
                  : "TBD"}
              </h2>

              {/* Display Teams */}
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

              <h2 style={{ textAlign: "center" }}>Predictions</h2>
              <h2 style={{ textAlign: "center" }}>
                {matchDetails && matchDetails.predicted_score.home}-
                {matchDetails && matchDetails.predicted_score.away}
              </h2>

              <h2 style={{ textAlign: "center" }}>Actual Score</h2>
              <h2 style={{ textAlign: "center" }}>
                {selected && selected.teams[0].score}-
                {selected && selected.teams[1].score}
              </h2>

              <h2 style={{ textAlign: "center" }}>
                Previously Won Fixtures Between
              </h2>
              <div style={{ display: "flex" }}>
                <div className="vs">
                  {matchDetails &&
                    matchDetails.last_fixtures_between.map((fix) => {
                      return (
                        <span
                          key={fix.id}
                          style={{
                            margin: "20px",
                            textAlign: "center",
                            fontSize: "0.8rem",
                          }}
                        >
                          <img
                            src={
                              fix.result == 0
                                ? teamOneImage
                                : fix.result == 1
                                ? drawImage
                                : teamTwoImage
                            }
                            height={50}
                            width={50}
                          />
                          <div>{fix.date}</div>
                        </span>
                      );
                    })}
                </div>
              </div>

              <h2 style={{ textAlign: "center" }}>Previous Fixtures</h2>
              <div className="gridtwo">
                <div className={styles.card}>
                  {matchDetails &&
                    matchDetails.last_fixtures_home.map((fix) => {
                      return (
                        <span
                          key={fix.id}
                          style={{
                            margin: "10px",
                            textAlign: "center",
                            fontSize: "0.8rem",
                          }}
                        >
                          <img
                            src={
                              fix.result == 0
                                ? winImage
                                : fix.result == 1
                                ? drawImage
                                : looseImage
                            }
                            height={25}
                            width={25}
                          />
                          <div>{fix.date}</div>
                        </span>
                      );
                    })}
                </div>
                <div className={styles.card}>
                  {matchDetails &&
                    matchDetails.last_fixtures_away.map((fix) => {
                      return (
                        <span
                          key={fix.id}
                          style={{
                            margin: "10px",
                            textAlign: "center",
                            fontSize: "0.8rem",
                          }}
                        >
                          <img
                            src={
                              fix.result == 0
                                ? winImage
                                : fix.result == 1
                                ? drawImage
                                : looseImage
                            }
                            height={25}
                            width={25}
                          />
                          <div>{fix.date}</div>
                        </span>
                      );
                    })}
                </div>
              </div>

              <div className="gridtwo">
                <div className={styles.card}>
                  <h2 style={{ textAlign: "center" }}>
                    Previous Fixtures At Home
                  </h2>
                  {matchDetails &&
                    matchDetails.last_fixtures_home_home.map((fix) => {
                      return (
                        <span
                          key={fix.id}
                          style={{
                            margin: "10px",
                            textAlign: "center",
                            fontSize: "0.8rem",
                          }}
                        >
                          <img
                            src={
                              fix.result == 0
                                ? winImage
                                : fix.result == 1
                                ? drawImage
                                : looseImage
                            }
                            height={25}
                            width={25}
                          />
                          <div>{fix.date}</div>
                        </span>
                      );
                    })}
                </div>
                <div className={styles.card}>
                  <h2 style={{ textAlign: "center" }}>
                    Previous Fixtures Away
                  </h2>
                  {matchDetails &&
                    matchDetails.last_fixtures_away_away.map((fix) => {
                      return (
                        <span
                          key={fix.id}
                          style={{
                            margin: "10px",
                            textAlign: "center",
                            fontSize: "0.8rem",
                          }}
                        >
                          <img
                            src={
                              fix.result == 0
                                ? winImage
                                : fix.result == 1
                                ? drawImage
                                : looseImage
                            }
                            height={25}
                            width={25}
                          />
                          <div>{fix.date}</div>
                        </span>
                      );
                    })}
                </div>
              </div>

              <div className="gridtwo">
                <div className={styles.card}>
                  <h2 style={{ textAlign: "center" }}>
                    Previous Fixtures Home
                  </h2>
                  <PieChart
                    data={[
                      matchDetails.home_ratio.win,
                      matchDetails.home_ratio.draw,
                      matchDetails.home_ratio.lose,
                    ]}
                  />
                </div>
                <div className={styles.card}>
                  <h2 style={{ textAlign: "center" }}>
                    Previous Fixtures Away
                  </h2>
                  <PieChart
                    data={[
                      matchDetails.away_ratio.win,
                      matchDetails.away_ratio.draw,
                      matchDetails.away_ratio.lose,
                    ]}
                  />
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default MatchDetailsPrev;
