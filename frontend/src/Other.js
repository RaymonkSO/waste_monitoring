import React from "react";
import bin from "./pic/recycle-bin.png";

const Other = () => {
  return (
    <div>
      <div className=" bg-[#B0ECAB] w-[370px] mt-[9%] h-[120px] gap-5 rounded-md flex ">
        <div>
          <h1 className="font-light text-sm ml-[29px] mt-[9%]">Bin A</h1>
          <img src={bin} className="h-[70px] mt-[10%] ml-[13px]"></img>
        </div>
        <div className="mt-[10%] font-semibold text-[12px]">
          <h1>location : in front Yeung lt 11 AC1</h1>
          <h1> distance : 130m away</h1>
        </div>
      </div>
      <div className=" bg-[#abecde] w-[370px] mt-[3%] h-[120px] gap-5 rounded-md flex ">
        <div>
          <h1 className="font-light text-sm ml-[29px] mt-[9%]">Bin B</h1>
          <img src={bin} className="h-[70px] mt-[10%] ml-[13px]"></img>
        </div>
        <div className="mt-[10%] font-semibold text-[12px]">
          <h1>location : in front Yeung lt 5 AC1</h1>
          <h1> distance : 230m away</h1>
        </div>
      </div>
      <div className=" bg-[#abbaec] w-[370px] mt-[3%] h-[120px] gap-5 rounded-md flex ">
        <div>
          <h1 className="font-light text-sm ml-[29px] mt-[9%]">Bin C</h1>
          <img src={bin} className="h-[70px] mt-[10%] ml-[13px]"></img>
        </div>
        <div className="mt-[10%] font-semibold text-[12px]">
          <h1>location : in front LI505 AC2</h1>
          <h1> distance : 530m away</h1>
        </div>
      </div>
    </div>
  );
};

export default Other;
