"use client";

//CSS
import styles from "./Footer.module.css";

export default function Footer({src, txt}) {
  return (
    <div className={styles.Footer}>
        <div className={styles.Footer_Header}>
          <h3>Resolved</h3>
        </div>
        <div className={styles.Footer_Creators}>
          <h5>Creators</h5>
          <a href="https://github.com/54JIN" target="_blank" rel="noreferrer">Sajin Saju</a>
          <a href="https://github.com/nickyim" target="_blank" rel="noreferrer">Nicholas Yim</a>
          <a href="https://github.com/aseefdurrani" target="_blank" rel="noreferrer">Aseef Durrani</a>
          <a href="https://github.com/justinklee1253" target="_blank" rel="noreferrer">Justin Kyuhyung Lee</a>
        </div>
    </div>
  );
}