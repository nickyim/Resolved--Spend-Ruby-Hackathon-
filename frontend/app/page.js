"use client";
import { useUser, SignInButton, SignUpButton, UserButton, useClerk } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import axios from "axios";

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
    <div style={{
        backgroundSize: "cover",
        backgroundPosition: "center",
        height: "100vh",
        position: "relative",
      }}
    ><div
        style={{
          position: "absolute",
          top: "20px",
          right: "20px",
        }}
      >
        {isSignedIn ? (
          <UserButton afterSignOutUrl="/" />
        ) : (
          <div style={{display: "flex", gap: "10px" }}><SignInButton mode="modal"><button className="auth-button">Login</button></SignInButton><SignUpButton mode="modal"><button className="auth-button">Sign up</button></SignUpButton></div>
        )}
      </div>

      {!isSignedIn && (
        <div className="landing-content"><h1 className="landing-title">Ruby Hack TEMP TITLE</h1><p className="landing-subtitle">[SUBTITLE HERE]</p></div>
      )}
    </div>
  );
}
