"use client";
import { UserButton, useUser } from "@clerk/nextjs";
import styles from "./Header.module.css";

export default function Header() {
  const { user } = useUser();

  return (
    <div className={styles.header}>
      <div className={styles.userInfo}>
        <div className={styles.userName}>{user?.firstName} {user?.lastName}</div>
        <div className={styles.userEmail}>{user?.primaryEmailAddress?.emailAddress}</div>
      </div>
      <UserButton afterSignOutUrl="/" />
    </div>
  );
}
