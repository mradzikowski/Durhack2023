"use client";
import { useState } from "react";
import MainPage from "./Components/MainPage";
import "./page.css";
import styles from "./page.module.css";
import MatchDetails from "./Components/MatchDetails/MatchDetails";

export default function Home() {
  const [selected, setSelected] = useState(null);
  return (
    <main className={styles.main}>
      {selected ? (
        <MatchDetails selected={selected} setSelected={setSelected} />
      ) : (
        <MainPage setSelected={setSelected} />
      )}
    </main>
  );
}
