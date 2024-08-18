"use client";

import Image from "next/image";

//CSS
import styles from "../styles/Product.module.css";

export default function Product({ src, txt }) {
  return (
    <div className={styles.Product}>
      <div className={styles.Product_Overlay}>
        <p>{txt}</p>
      </div>
      <div className={styles.Product_Image}>
        <Image src={src} alt={txt}/>
      </div>
    </div>
  );
}
