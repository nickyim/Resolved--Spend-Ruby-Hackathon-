"use client";
import { useUser, SignInButton, SignUpButton, UserButton, useClerk } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import axios from "axios";

import styles from './page.module.css'

export default function Home() {
  const { isSignedIn, user } = useUser();
  const router = useRouter();
  const { signUp } = useClerk();

  useEffect(() => {
    if (isSignedIn && user) {
      // Check if the user exists in your database
      axios
        .get(`http://127.0.0.1:5000/api/user?clerkId=${user.id}`)
        .then(response => {
          console.log('User exists:', response.data);
          router.push('/dashboard'); //redirect user to dashboard after verifying 
        })
        .catch(error => {
          if (error.response && error.response.status === 404) {
            // User doesn't exist, so create them
            axios.post('http://127.0.0.1:5000/api/register', {
              clerkId: user.id,
              email: user.primaryEmailAddress.emailAddress,
            })
            .then(response => {
              if (response && response.status === 201) {
                console.log('User created successfully');
                router.push('/dashboard'); //
              }
            })
            .catch(err => {
              console.error('Error during registration:', err);
            });
          } else {
            console.error('Error fetching user:', error);
          }
        });
    }
  }, [isSignedIn, user]);
    
  return (
    <div className={styles.Initial_LandingPage}>
      {!isSignedIn ? (
        <div className={styles.LandingPage}>
          <div className={styles.LandingPage_Header}>
            <div className={styles.LandingPage_Header_Content}>
              <h1>Resolved</h1>
              <div className={styles.LandingPage_Header_Authentication}>
                <SignInButton mode="modal">
                  <button className={styles.LandingPage_Header_Authentication_Login}>Log in</button>
                </SignInButton>
                <SignUpButton mode="modal">
                  <button className={styles.LandingPage_Header_Authentication_SignUp}>Get started</button>
                </SignUpButton>
              </div>
            </div>
          </div>
          <div className={styles.LandingPage_Content}>
            <h2>All-in-one platform for complaint categorization</h2>
            <h6>Itemize your complaints to products and sub-products for easy filtering and comprehension</h6>
          </div>
        </div>
      ) : (
        <UserButton afterSignOutUrl="/" />
      )}
    </div>
  );
}
