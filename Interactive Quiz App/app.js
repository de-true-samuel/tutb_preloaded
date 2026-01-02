const mainCntr = document.getElementById("main-container");
const startCntr = document.getElementById("start-container");
const quizScreen = document.getElementById("quiz-screen");
const quizCntr = document.getElementById("quiz-container");
const startBtn = document.getElementById("startBtn");
const quesIndicator = document.getElementById("ques-indicator");
const questions = document.getElementById("question");
const optionCntr = document.getElementById("opt-container");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");
const submitBtn = document.getElementById("submit");
const scoreBoard = document.getElementById("score-board");
const totalScore = document.getElementById("total-score");
const restartBtn = document.getElementById("restart");
const homePageBtn = document.getElementById("home-page");
const feedbackCntr = document.getElementById("feedback-cntr");
const warning = document.getElementById("warning");
const confirmSubmit = document.getElementById("confirm-submit");
const dontSubmit = document.getElementById("dont-submit");
const correctSummary = document.getElementById("correct-summary");
const blocker = document.getElementById("blocker");

const quizSet = [
  {
    question: "What is the main function of an operating system?",
    options: ['Manage hardware resources', 'Provide internet connectivity', 'Create documents', 'Run antivirus software'],
    ans: 'Manage hardware resources'
  },
  {
    question: "Which operating system is known for its open-source nature?",
    options: ['Windows', 'macOS', 'Linux', 'Chrome OS'],
    ans: 'Linux'
  },
  {
    question: "What does CPU stand for in operating systems?",
    options: ['Central Processing Unit', 'Computer Power Unit', 'Central Program Utility', 'Core Processing Unit'],
    ans: 'Central Processing Unit'
  },
  {
    question: "Which scheduling algorithm allocates the CPU to the process that requests it first?",
    options: ['Round Robin', 'Shortest Job First', 'First-Come, First-Served', 'Priority Scheduling'],
    ans: 'First-Come, First-Served'
  },
  {
    question: "What is virtual memory?",
    options: ['Memory stored in the cloud', 'A technique that uses disk space as RAM', 'Memory used by virtual machines', 'A type of ROM'],
    ans: 'A technique that uses disk space as RAM'
  },
  {
    question: "Which Windows version introduced the Start Menu?",
    options: ['Windows 95', 'Windows XP', 'Windows 7', 'Windows 10'],
    ans: 'Windows 95'
  },
  {
    question: "What is the kernel of an operating system?",
    options: ['The user interface', 'The core component that manages hardware', 'The file system', 'The application launcher'],
    ans: 'The core component that manages hardware'
  },
  {
    question: "Which file system is commonly used in modern Windows versions?",
    options: ['FAT32', 'NTFS', 'EXT4', 'HFS+'],
    ans: 'NTFS'
  },
  {
    question: "What is multitasking in operating systems?",
    options: ['Running multiple CPUs', 'Executing multiple tasks simultaneously', 'Using multiple monitors', 'Installing multiple OS'],
    ans: 'Executing multiple tasks simultaneously'
  },
  {
    question: "Which macOS version was named after a big cat?",
    options: ['macOS Sierra', 'macOS High Sierra', 'macOS Mojave', 'macOS Catalina'],
    ans: 'macOS Catalina'
  }
];

let totalQuestion = quizSet.length;
let questionIndex = 0;
let score = 0;

const userAns = {

};

startBtn.addEventListener("click", startQuiz);
nextBtn.addEventListener("click", clickNext);
prevBtn.addEventListener("click", clickPrev);
submitBtn.addEventListener("click", clickSubmit);

confirmSubmit.addEventListener("click", () => {
  blocker.classList.add("hidden");
  warning.classList.add("hidden");
  quizScreen.classList.add("hidden");
  scoreBoard.classList.remove("hidden");
  totalScore.textContent = `You scored: ${score} / ${totalQuestion}`;
  showCorrectSum();
});

dontSubmit.addEventListener("click", () => {
  warning.classList.add("hidden");
  blocker.classList.add("hidden");
});

restartBtn.addEventListener("click", () => {
  scoreBoard.classList.add("hidden");
  clearUserAns();
  optionCntr.textContent = "";
  questionIndex = 0;
  startQuiz();
  score = 0;
});

homePageBtn.addEventListener("click", () => {
  scoreBoard.classList.add("hidden");
  startCntr.classList.remove("hidden");
  questionIndex = 0;
  score = 0;
  clearUserAns();
});

//Function for the start button
function startQuiz() {
  startCntr.classList.add("hidden");
  quizScreen.classList.remove("hidden");
  quesIndicator.textContent = `Question 1 of ${totalQuestion}`;
  questions.textContent = quizSet[0].question;
  showOptions();
  prevBtn.disabled = true;
  nextBtn.disabled = false;
};

//Function for "Next" button
function clickNext() {
  questionIndex++;
  showQuestion();
};

//function for "Prev" button
function clickPrev() {
  questionIndex--;
  showQuestion();
};


//You wanted to add the are sure div
function clickSubmit() {
  warning.classList.remove("hidden");
  blocker.classList.remove("hidden");
};

//function for questionNumber
function questionNum() {
  return questionIndex + 1;
};

//fucntion to show questions
function showQuestion() {
  feedbackCntr.innerHTML = "";
  quesIndicator.textContent = `Question ${questionNum()} of ${totalQuestion}`;
  questions.textContent = quizSet[questionIndex].question;
  showOptions();
  prevBtn.disabled = questionIndex <= 0;
  nextBtn.disabled = questionIndex >= totalQuestion - 1;
  if(userAns[questionNum()]) {
    let allOptions = optionCntr.querySelectorAll("button");
    allOptions.forEach(btn => {
      btn.disabled = true;
      if(userAns[questionNum()] == btn.textContent) {
        if(btn.textContent == quizSet[questionIndex].ans) btn.classList.toggle("correct-option");
        else {
          btn.classList.toggle("wrong-option");
          giveFeedback();
        };
      };
    });
  };
};

//function for creating the options
function showOptions() {
  optionCntr.innerHTML = "";
  quizSet[questionIndex].options.forEach((option) => {
    let button = document.createElement("button");
    button.textContent = option;

    button.addEventListener("click", () => {
      if (button.textContent == quizSet[questionIndex].ans) {
        button.classList.add("correct-option");
        score++;
        console.log(score);
      }
      if (button.textContent != quizSet[questionIndex].ans) {
        button.classList.add("wrong-option");
        giveFeedback();
      }
      
      let allOptions = optionCntr.querySelectorAll("button");
      allOptions.forEach(btn => {
        btn.disabled = true;
      });
      
      userAns[questionNum()] = option;
      console.log(userAns);
    });
    optionCntr.appendChild(button);
  });
};

//function to give answer for wrong options
function giveFeedback() {
  let feedback = document.createElement("p");
  feedback.classList.add("correct-ans");
  feedback.textContent = `\u{2705}Correct Answer: ${quizSet[questionIndex].ans}`;
  feedbackCntr.appendChild(feedback);
};

function clearUserAns() {
  for(answer in userAns) {
    delete userAns[answer];
  };
  console.log(userAns);
};

function showCorrectSum() {
   for (let i = correctSummary.children.length - 1; i > 0; i--) {
        correctSummary.children[i].remove();
    }
  for(key in quizSet) {
    let ansCntr = document.createElement("div");
    let CSquestion = document.createElement("p");
    let CSanswer = document.createElement("p");
    correctSummary.appendChild(ansCntr);
    CSquestion.textContent = `${parseInt(key) + 1}  ${quizSet[key].question}`;
    CSanswer.textContent = `\u{2192} ${quizSet[key].ans}`;
    ansCntr.appendChild(CSquestion);
    ansCntr.appendChild(CSanswer);
  };
};
