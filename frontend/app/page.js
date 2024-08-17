"use client";
import { useUser, SignInButton, SignUpButton, UserButton } from"@clerk/nextjs";
import { useRouter } from"next/navigation";

export default function Home() {
  const { isSignedIn } = useUser();
  const router = useRouter();


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
