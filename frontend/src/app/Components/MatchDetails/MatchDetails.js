import React from "react";
import "./matchDetails.css";
import styles from "../../page.module.css";

const MatchDetails = ({ selected, setSelected }) => {
  const fixture = selected;
  const team1ImageMap = selected.team1ImageId;
  const team2ImageMap = selected.team2ImageId;
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

          <div style={{ display: "flex" }}>
            <div className="vs">{" Predictions "}</div>
          </div>

          <div style={{ display: "flex", margin:"0rem 15rem"}}>
            <div className="team">
                <h2>1</h2>
            </div>
            <div className="vs"></div>
            <div className="team">
              <h2>0</h2>
            </div>
          </div>

        </div>
      </div>
    </>
  );
};

export default MatchDetails;
