function enterFocusMode() {
    document.getElementById("focusMode").style.display = "block";
    startTimer();
}
function exitFocusMode() {
    document.getElementById("focusMode").style.display = "none";
}
function startTimer() {
    var timerElement = document.getElementById("timer");
    var minutes = 24;
    var seconds = 59;

    var interval = setInterval(function () {
        timerElement.textContent =
            minutes.toString().padStart(2, "0") +
            ":" +
            seconds.toString().padStart(2, "0");
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
        }
        if (minutes < 0) {
            clearInterval(interval);
            timerElement.textContent = "Time's up!";
        }
    }, 1000);
}
