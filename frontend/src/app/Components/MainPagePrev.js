import React from "react";
import MatchCards from "./MatchCards";
import Image from "next/image";
import styles from "../page.module.css";
import { Link } from "react-router-dom";
import MatchDetailsPrev from "./MatchDetailsPrev/MatchDetailsPrev";
import MatchCardsPrev from "./MatchCardsPrev";
const MainPagePrev = ({ setSelected }) => {
  return (
    <>
      <div className={styles.description}>
        <p>
          Premier League&nbsp;
          <code className={styles.code}>Predictions</code>
        </p>
        <div>
          <Link to="/">
            Main Page
          </Link>
        </div>
      </div>

      <div className={styles.center}>
        <Image
          className={styles.logo}
          src="/pl.svg"
          alt="Next.js Logo"
          width={180}
          height={180}
          priority
        />
      </div>

      <div className={`${styles.grid} gridone`}>
        <MatchCardsPrev setSelected={setSelected} />
      </div>
    </>
  );
};
export default MainPagePrev;
