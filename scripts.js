document.addEventListener("DOMContentLoaded", function () {
  const popupContainer = document.getElementById("popupContainer");
  const popupContent = document.getElementById("popupContent");
  const backgroundBlur = document.getElementById("backgroundBlur");
  const container = document.getElementById("formContainer");
  const closePopupButton = document.getElementById("closePopup");
  const dataForm = document.getElementById("dataForm");

  backgroundBlur.style.opacity = "0.8";
  setTimeout(() => {
    backgroundBlur.style.opacity = "0";
    container.style.display = "block";
    setTimeout(() => {
      showPopup(
        `This attendance percentage was actually correct according to the attendance sheet that I handle every day with subject staff. However, in the master attendance, the possibility is that you should get an attendance percentage of more than 0.5 to 1% compared to this.`
      );
    }, 1000);
  }, 1000);

  closePopupButton.addEventListener("click", closePopup);

  dataForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const regNo = document.getElementById("regNo").value;
    const dob = document.getElementById("dob").value;
    if (validateInput(regNo, dob)) {
      fetchAttendanceData(regNo, dob)
        .then((data) => {
          const attendancePercentage = calculateAttendancePercentage(
            data.attend,
            data.total_number
          );
          showPopup(
            `Dear ${
              data.name
            },<br>Your attendance percentage is ${attendancePercentage.toFixed(
              2
            )}% (${attendancePercentage.toFixed(0)}%).`
          );
        })
        .catch((error) => {
          console.error("Error fetching attendance data:", error);
          alert("Error fetching attendance data. Please try again.");
        });
    } else {
      alert("Please fill in all fields with valid data.");
    }
  });

  function closePopup() {
    popupContainer.style.display = "none";
  }

  function showPopup(message) {
    popupContent.innerHTML = `<p>${message}</p>`;
    popupContainer.style.display = "flex";

    if (!message.includes("Dear")) {
      popupContent.innerHTML += `
          <button style="background: linear-gradient(to right, #FF6F61, #6E8B9E); border-radius: 15px" id="agreeButton">Agree and Continue</button>
        `;

      const agreeButton = document.getElementById("agreeButton");
      agreeButton.addEventListener("click", function () {
        clearCache();
        closePopup();
      });
    }
  }

  function validateInput(regNo, dob) {
    return regNo && dob && !isNaN(regNo);
  }

  function calculateAttendancePercentage(attend, totalNumber) {
    return (attend / totalNumber) * 100;
  }

  function fetchAttendanceData(regNo, dob) {
    return fetch(`data/users.json?timestamp=${new Date().getTime()}`)
      .then(response => response.json())
      .then(users => {
        return new Promise((resolve, reject) => {
          const user = users.find(u => u.regNo === regNo && u.dob === dob);
          if (user) {
            // Adding a timestamp to the resolved data to ensure cache busting
            user.timestamp = new Date().getTime();
            resolve(user);
          } else {
            reject("User not found");
          }
        });
      });
  }

  function clearCache() {
    if ("caches" in window) {
      caches.keys().then((names) => {
        names.forEach((name) => {
          caches.delete(name);
        });
      });
    }
    localStorage.clear();
    sessionStorage.clear();
  }
});
