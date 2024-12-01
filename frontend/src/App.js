import logo from "./logo.svg";
import "./App.css";
import Home from "./User";
import bin from "./pic/recycle-bin.png";
import Prediction from "./Prediction";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";

import "react-notifications/lib/notifications.css";
import { useEffect, useState } from "react";
import axios from "axios";
import Game from "./Game";
import Other from "./Other";
import { GiGamepad } from "react-icons/gi";
import { FaHome } from "react-icons/fa";
import { FaUserCircle } from "react-icons/fa";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function App() {
  const [percentage, setPercentage] = useState(null);
  const [prediction, setPrediction] = useState([]);
  const createNotification = (type) => {
    return () => {
      switch (type) {
        case "warning":
          NotificationManager.warning(
            "Bin A is almost full!",
            "Close after 3000ms",
            3000
          );
          break;
        case "error":
          NotificationManager.error("Error message", "Click me!", 5000, () => {
            alert("callback");
          });
          break;
        default:
          break;
      }
    };
  };
  useEffect(() => {
    const fetchPercentage = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/fill-levels/",
          {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
            withCredentials: false,
          }
        );
        const latestData = response.data.reduce((latest, current) =>
          current.id > latest.id ? current : latest
        );

        const latestFillLevel = latestData.fill_level;
        setPercentage(latestFillLevel);
        console.log(percentage);

        if (percentage > 75) {
          createNotification("warning")();
        }
      } catch (error) {
        console.error("Error fetching percentage:", error);
      }
    };
    const interval = setInterval(() => {
      fetchPercentage();
    }, 60000);
    return () => clearInterval(interval);
  }, []);
  console.log(percentage);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/fill-predictions/",
          {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
            withCredentials: false,
          }
        );
        setPrediction(response.data);
      } catch (error) {
        console.error("Error fetching percentage:", error);
      }
    };
    const interval = setInterval(() => {
      fetchPrediction();
    }, 60000);
    return () => clearInterval(interval);
  }, []);
  console.log(prediction);

  return (
    <BrowserRouter>
      <div className="h-[802px] w-[402px] bg-slate-200 justify-items-center ml-[35%]">
        <div className=" pt-[5%] flex justify-items-end gap-[220px]">
          <h1>15 : 10</h1>
          <div>
            <h1 className="ml-[-23px]"> Vanessa </h1>
            <FaUserCircle className="ml-[43px] mt-[-18px]" />
          </div>
        </div>

        <h1 className="pt-[30px] ml-[-140px] text-[24px] font-bold">
          Good Afternoon!
        </h1>
        <h1 className="text-[10px] ml-[-194px] font-semibold">
          Thursday 28 November 2024
        </h1>
        <NotificationContainer style={{ top: "50px", right: "30px" }} />
        <div className="pt-[0px]">
          {/* <Home data={percentage}></Home> */}
          {/* <Game></Game> */}
          {/* <Other></Other> */}

          {/* <Prediction></Prediction> */}

          <Routes>
            <Route path="/" element={<Home data={percentage} />} />
            <Route path="/other" element={<Other />} />
            <Route
              path="/prediction"
              element={<Prediction data={prediction} />}
            />
            <Route path="/game" element={<Game />} />
          </Routes>
        </div>

        <div className=" flex justify-items-center h-[50px] rounded-lg  bg-white w-full mt-[210px]">
          <Link to="/game">
            <GiGamepad size={44} className="ml-[130px]" />
          </Link>
          <Link to="/">
            <FaHome size={40} className="ml-[39px]" />
          </Link>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
