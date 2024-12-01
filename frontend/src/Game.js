import React from "react";
import { useState } from "react";

const Game = () => {
  const [score, setScore] = useState(0);
  const [question, setQuestion] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const questions = [
    {
      text: "Which of the following materials is commonly not recyclable ?",
      options: [
        { id: 0, text: "Aluminum cans", isCorrect: false },
        { id: 1, text: "Glass bottles", isCorrect: false },
        { id: 2, text: "Pizza boxes with grease stains", isCorrect: true },
      ],
    },
    {
      text: "What is the primary benefit of recycling paper?",
      options: [
        { id: 0, text: "Reduces the need for landfills", isCorrect: true },
        { id: 1, text: "Increases air pollution", isCorrect: false },
        { id: 2, text: " Increases energy consumption", isCorrect: false },
      ],
    },
    {
      text: "Which of the following is an example of a biodegradable material?",
      options: [
        { id: 0, text: "Plastic bottle", isCorrect: false },
        { id: 1, text: "Paper bag", isCorrect: true },
        { id: 2, text: "Styrofoam container", isCorrect: false },
      ],
    },
  ];
  const optionClicked = (isCorrect) => {
    if (isCorrect) {
      setScore(score + 1);
    }
    if (question + 1 < questions.length) {
      setQuestion(question + 1);
    } else {
      setShowResults(true);
    }
  };
  return (
    <div>
      <h1 className="text-center text-xl font-bold mt-[20%]">
        {" "}
        Waste Recycling Quiz !
      </h1>
      <h2 className="font-thin text-sm text-center mt-[2%]">
        {" "}
        Current Score: {score}
      </h2>

      {showResults ? (
        <div>
          <h1 className="text-center mt-[10%] text-base font-thin">
            Final Result
          </h1>
          <h1 className="text-center mt-[2%] text-lg font-semibold">
            {score} out of {questions.length} correct
          </h1>
          <div className="bg-yellow-500 w-[350px] h-[100px] ml-[2%] mt-[3%] mb-[5%] rounded-xl">
            <h1 className=" font-light text-[10px] text-justify font-mono text-white pt-3 px-2">
              {" "}
              Question 1 answer is Pizza boxes with grease stains Pizza boxes
              are often contaminated with grease or food residue, making them
              unsuitable for recycling in most curbside programs.
            </h1>
          </div>
          <div className="bg-lime-600 w-[350px] h-[100px] ml-[2%] mt-[3%] mb-[5%] rounded-xl">
            <h1 className=" font-light text-[10px] text-justify font-mono text-white pt-3 px-2">
              {" "}
              Question 2 answer is Reduces the need for landfills. Recycling
              paper helps divert it from landfills, reducing waste and
              conserving resources by reusing fibers.
            </h1>
          </div>
          <div className="bg-teal-600 w-[350px] h-[100px] ml-[2%] mt-[1%] mb-[5%] rounded-xl">
            <h1 className=" font-light text-[10px] text-justify font-mono text-white pt-3 px-2">
              {" "}
              Question 3 answer is Paper bag Paper bags are biodegradable,
              meaning they can decompose naturally in the environment, unlike
              plastic bags or Styrofoam.
            </h1>
          </div>
        </div>
      ) : (
        <div>
          <h1 className="font-thin text-sm text-center mt-[1%]">
            {" "}
            Question: {question + 1} out of {questions.length}
          </h1>

          <h1 className=" text-center text-[12px] font-semibold mt-[8%]">
            {" "}
            {questions[question].text}
          </h1>

          <div className=" py-3 justify-items-center ">
            {questions[question].options.map((option) => {
              return (
                <div
                  key={option.id}
                  onClick={() => optionClicked(option.isCorrect)}
                  className="  text-xs mb-2 text-center font-normal text-white  rounded-xl h-[30px] w-[300px] bg-[#46b15b]"
                >
                  <h1 className="pt-[6px]">{option.text}</h1>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <h1 className="mt-[4%] text-[12px]">Feedback form</h1>
      <form className="w-[350px] text-sm">
        <input className=" w-[350px] text-sm rounded-md h-[40px]" type="text" />
      </form>
      <button className="text-[10px] rounded-md bg-[#00340A] w-[45px] text-white">
        submit
      </button>
    </div>
  );
};

export default Game;
