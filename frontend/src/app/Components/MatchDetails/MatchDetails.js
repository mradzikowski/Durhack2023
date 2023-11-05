import React, { useEffect, useState } from "react";
import "./matchDetails.css";
import styles from "../../page.module.css";
import teamNameMapping from "../../Mappings/teamNameMapping.json";
import axios from "axios";

const MatchDetails = ({ selected, setSelected }) => {
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
    const team1 = teamNameMapping.find(
      (d) => d.name == fixture.teams[0].team.name
    ).map;
    const team2 = teamNameMapping.find(
      (d) => d.name == fixture.teams[1].team.name
    ).map;
    const match = await axios.get(
      `http://localhost:8080/fixtures/prediction/${team1}/${team2}/5`
    );
    setMatchDetails(match.data);
  };

  return (
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
              : "To be Decided"}
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

          <h2 style={{ textAlign: "center" }}>
            Previously Won Fixtures Between
          </h2>
          <div style={{ display: "flex" }}>
            <div className="vs">
              {matchDetails &&
                matchDetails.last_fixtures_between.map((fix) => {
                  return (
                    <span
                      style={{
                        margin: "20px",
                        textAlign: "center",
                        fontSize: "0.8rem",
                      }}
                    >
                      <img
                        key={fix.id}
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
          <div style={{ display: "flex" }}>
            <div className="team">
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
                        key={fix.id}
                        src={
                          fix.result == 0
                            ? winImage
                            : fix.result == 1
                            ? drawImage
                            : looseImage
                        }
                        height={40}
                        width={40}
                      />
                      <div>{fix.date}</div>
                    </span>
                  );
                })}
            </div>
            <div className="vs"></div>
            <div className="team">
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
                        key={fix.id}
                        src={
                          fix.result == 0
                            ? winImage
                            : fix.result == 1
                            ? drawImage
                            : looseImage
                        }
                        height={40}
                        width={40}
                      />
                      <div>{fix.date}</div>
                    </span>
                  );
                })}
            </div>
          </div>


          <h2 style={{ textAlign: "center" }}>Previous Fixtures At Home</h2>
          <div style={{ display: "flex" }}>
            <div className="team">
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
                        key={fix.id}
                        src={
                          fix.result == 0
                            ? winImage
                            : fix.result == 1
                            ? drawImage
                            : looseImage
                        }
                        height={40}
                        width={40}
                      />
                      <div>{fix.date}</div>
                    </span>
                  );
                })}
            </div>
            <div className="vs"></div>
            <div className="team">
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
                        key={fix.id}
                        src={
                          fix.result == 0
                            ? winImage
                            : fix.result == 1
                            ? drawImage
                            : looseImage
                        }
                        height={40}
                        width={40}
                      />
                      <div>{fix.date}</div>
                    </span>
                  );
                })}
            </div>
          </div>

        </div>
      </div>
    </>
  );
};

export default MatchDetails;
