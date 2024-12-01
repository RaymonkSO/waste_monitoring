import React from "react";
import bin from "./pic/recycle-bin.png";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";
import "react-notifications/lib/notifications.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
const Home = ({ data }) => {
  const percentage = data;
  return (
    <div className="bg-[#B0ECAB] w-[343px] h-[346px] rounded-[20px] mt-[38px] ml-[1%]">
      <h1 className="text-pretty font-semibold text-[23px] text-center pt-[65px]">
        Nearest Bin Around You
      </h1>
      <div className="flex gap-15  mt-[13%]">
        <div>
          {" "}
          <p className="pl-[62px] w-[100%] text-[15px] font-light">
            {" "}
            Trash level
          </p>
          <div
            style={{
              position: "relative",
              width: "70px",
              height: "100px",
              marginLeft: "62px",
              marginTop: "30px",
            }}
          >
            <CircularProgressbar
              value={percentage}
              circleRatio={0.5}
              strokeWidth={15}
              styles={buildStyles({
                rotation: 3 / 4,
                strokeLinecap: "butt",
                trailColor: "#C4C4C4",
                pathColor: "green",
                textColor: "transparent",
              })}
            />
            <div
              style={{
                position: "absolute",
                top: "27%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                fontSize: "10px",
                color: "black",
              }}
            >
              {`${percentage}%`}
            </div>
          </div>
        </div>

        <img src={bin} className="w-[120px] h-[142px] ml-[60px] "></img>
        <p className="mt-[43%] ml-[-30%] font-light ">50m away</p>
      </div>
      <div className="flex gap-[50px] mt-[27px] mb-[120px]">
        <Link to="/other">
          <div className="w-[145px] h-[115px] bg-[#00340A] rounded-[20px] mt-[30px]">
            <h1 className=" text-white text-[12px] font-semibold text-center pt-[10px]">
              Other bin location
            </h1>
            <div className="flex pt-[10px]">
              <img className=" w-[56px] ml-[30px] h-[50px]" src={bin}></img>
              <img className=" w-[56px] ml-[-20px] h-[50px]" src={bin}></img>
            </div>
          </div>
        </Link>
        <Link to="/prediction">
          <div className="w-[145px] h-[115px] bg-[rgb(0,52,10)] rounded-[20px] mt-[30px]">
            <h1 className=" text-white text-[12px] font-semibold text-center pt-[10px]">
              bin prediction
            </h1>
            <img
              className="w-[56px] ml-[50px] mt-[10px] h-[50px]"
              src={bin}
            ></img>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Home;
