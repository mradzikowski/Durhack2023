import React from "react";
import MatchCards from "./MatchCards";
import Image from "next/image";
import styles from "../page.module.css";
const MainPage = ({ setSelected }) => {
  return (
    <>
      <div className={styles.description}>
        <p>
          Premier League&nbsp;
          <code className={styles.code}>Predictions</code>
        </p>
        <div>
          <a
            href="https://vercel.com?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            By{" "}
            <Image
              src="/vercel.svg"
              alt="Vercel Logo"
              className={styles.vercelLogo}
              width={100}
              height={24}
              priority
            />
          </a>
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
        <MatchCards setSelected={setSelected} />
      </div>
    </>
  );
};
export default MainPage;
