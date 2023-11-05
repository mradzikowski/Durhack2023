"use client";
import { useState } from "react";
import MainPage from "./Components/MainPage";
import "./page.css";
import styles from "./page.module.css";
import MatchDetails from "./Components/MatchDetails/MatchDetails";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPagePrev from "./Components/MainPagePrev";
import MatchDetailsPrev from "./Components/MatchDetailsPrev/MatchDetailsPrev";

export default function Home() {
  const [selected, setSelected] = useState(null);
  const [selectedPrev, setSelectedPrev] = useState(null);
  return (
    <BrowserRouter>
      <Routes>
        <Route
          index
          path="/"
          element={
            <main className={styles.main}>
              {selected ? (
                <MatchDetails selected={selected} setSelected={setSelected} />
              ) : (
                <MainPage setSelected={setSelected} />
              )}
            </main>
          }
        />

        <Route
          path="/prevseason"
          element={
            <main className={styles.main}>
              {selectedPrev ? (
                <MatchDetailsPrev selected={selectedPrev} setSelected={setSelectedPrev} />
              ) : (
                <MainPagePrev setSelected={setSelectedPrev} />
              )}
            </main>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
