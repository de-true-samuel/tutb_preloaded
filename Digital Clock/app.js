const clockCntr = document.getElementById("clock-container");
const clock = document.getElementById("clock");
const dateCntr = document.getElementById("dateCntr");
const timeButton = document.getElementById("timeButton");
const timeline = document.getElementById("timeline");

let time = new Date();
let is24hrs = false;

setInterval(updateTime, 1000);
updateTime();

setInterval(showDate, 3600*1000);
showDate();

timeButton.addEventListener("click", () => {
  is24hrs = !is24hrs;
  updateTime();
});

function formatTime(num) {
  return num < 10 ? "0" + num : num;
}

//function for showing the time
function updateTime() {
  let date = new Date();
  let hour = date.getHours();
  let minute = date.getMinutes();
  let second = date.getSeconds();
  let ampm = "";

  if(!is24hrs) {
    ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12;
    if(hour === 0) {
      hour = 12;
    }
  }
  clock.textContent = `${formatTime(hour)} : ${formatTime(minute)} : ${formatTime(second)}`;
  timeline.textContent = ampm;
}

//function for showing the date
function showDate() {
  const time = new Date();
  const day = time.getDay();
  const date = time.getDate();
  const month = time.getMonth();
  const year = time.getFullYear();
  dateCntr.textContent = `${formatDay(day)}, ${formatMonth(month)} ${formatDate(date)}, ${year}`;
}

//function for formatting the date
function formatDay(dayIndex) {
  let DayList = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  day = DayList[dayIndex];
  return day;
}

function formatMonth(monthIndex) {
  let monthArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  return monthArr[monthIndex];
}

function formatDate(date) {
  let newDate = date.toString();
  if(newDate.endsWith("11") || newDate.endsWith("12") || newDate.endsWith("13")) {return date + "th";}
  if (newDate.charAt(newDate.length - 1) === "1") {return date + "st";}
  else if(newDate.charAt(newDate.length - 1) === "2") {return date + "nd";}
  else if (newDate.charAt(newDate.length - 1) === "3") {return date + "rd";}
  else {return date + "th";}
}

