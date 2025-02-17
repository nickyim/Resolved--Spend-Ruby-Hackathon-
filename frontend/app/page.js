"use client";
import {
  useUser,
  SignInButton,
  SignUpButton,
  UserButton,
  useClerk,
} from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Image from "next/image";
import axios from "axios";

//CSS
import styles from "./page.module.css";

//Images
import DashboardImg from "../public/images/DashboardImg.png";
import chartImg from "../public/images/chartImg.png";
import InputTypesImg from "../public/images/InputTypesImg.png";
import ImageFeatureImg from "../public/images/image.jpg";
import AudioFeatureImg from "../public/images/audio.jpg";
import TextFeatureImg from "../public/images/Text3.jpg";
import VideoFeatureImg from "../public/images/video.jpg";

//Components
import Product from "../Components/Product";
import Footer from "../Components/Footer";

export default function Home() {
  const { isSignedIn, user } = useUser();
  const router = useRouter();
  const { signUp } = useClerk();

  useEffect(() => {
    if (isSignedIn && user) {
      // Check if the user exists in your database
      axios
        .get(`${process.env.NEXT_PUBLIC_API_URL}/api/user?clerkId=${user.id}`)
        .then((response) => {
          console.log("User exists:", response.data);
          router.push("/dashboard"); //redirect user to dashboard after verifying
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            // User doesn't exist, so create them
            axios
              .post(`${process.env.NEXT_PUBLIC_API_URL}/api/register`, {
                clerkId: user.id,
                email: user.primaryEmailAddress.emailAddress,
              })
              .then((response) => {
                if (response && response.status === 201) {
                  console.log("User created successfully");
                  router.push("/dashboard"); //
                }
              })
              .catch((err) => {
                console.error("Error during registration:", err);
              });
          } else {
            console.error("Error fetching user:", error);
          }
        });
    }
  }, [isSignedIn, user, router]);

  return (
    <div className={styles.Initial_LandingPage}>
      {!isSignedIn ? (
        <div className={styles.LandingPage}>
          <div className={styles.LandingPage_Header}>
            <div className={styles.LandingPage_Header_Content}>
              <h1>Resolved</h1>
              <div className={styles.LandingPage_Header_Authentication}>
                <SignInButton mode="modal">
                  <button
                    className={styles.LandingPage_Header_Authentication_Login}
                  >
                    Log in
                  </button>
                </SignInButton>
                <SignUpButton mode="modal">
                  <button
                    className={styles.LandingPage_Header_Authentication_SignUp}
                  >
                    Get started
                  </button>
                </SignUpButton>
              </div>
            </div>
          </div>
          <div className={styles.LandingPage_Content}>
            <div className={styles.LandingPage_Content_Intro}>
              <h1>All-in-one platform for complaint categorization</h1>
              <h6>
                Itemize your complaints to products and sub-products for easy
                filtering and comprehension
              </h6>
              <div className={styles.LandingPage_Content_Intro_Features}>
                <Product src={TextFeatureImg} txt={"Text"} />
                <Product src={AudioFeatureImg} txt={"Audio"} />
                <Product src={VideoFeatureImg} txt={"Video"} />
                <Product src={ImageFeatureImg} txt={"Image"} />
              </div>
            </div>
            <div className={styles.LandingPage_Content_Product_Dashboard}>
              <h2>Resolved Offers a User Friendly Layout</h2>
              <Image
                src={DashboardImg}
                alt="Dashboard preview"
                className={styles.LandingPage_Content_DashboardImg}
              />
            </div>
          </div>
          <Footer />
        </div>
      ) : (
        <UserButton afterSignOutUrl="/" />
      )}
    </div>
  );
}
