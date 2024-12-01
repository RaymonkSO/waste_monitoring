import React from "react";
import bin from "./pic/recycle-bin.png";
import SemiCircleProgress from "react-semicircle-progressbar";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import axios from "axios";

const Prediction = ({ data = [] }) => {
  return (
    <div>
      <h1 className="font-bold text-[24px] text-center mt-[12%]">
        Today's Prediction
      </h1>
      <div className="bg-[#B0ECAB] w-[343px] h-[346px] rounded-[20px]  mt-[10px] ml-[1%]">
        <div className="flex gap-y-0  ml-[10%] justify-items-end">
          <div className="mt-[7%] ">
            {data.map((item) => {
              const fillTime = item.fill_date.substring(0, 5);
              const percentage = Math.round(item.fill_level * 10) / 10;
              return (
                <div key={item.id} className="flex mb-[10px] ">
                  <h1 className="  w-[75px] font-thin">{fillTime}</h1>
                  <div
                    style={{
                      position: "relative",
                      width: "50px",
                      height: "30px",
                      marginLeft: "1px",
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
                        top: "22px",
                        left: "50%",
                        transform: "translate(-50%, -50%)",
                        fontSize: "6px",
                        color: "black",
                      }}
                    >
                      {`${percentage}%`}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <img
            className="w-[160px] pl-[13%] h-[242px]  pt-[100px]"
            src={bin}
          ></img>
        </div>
      </div>
    </div>
  );
};

export default Prediction;
