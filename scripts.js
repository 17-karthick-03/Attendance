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
    }, 2000);
  }, 2000);

  closePopupButton.addEventListener("click", closePopup);
  window.addEventListener("click", function (event) {
    if (event.target === popupContainer) {
      closePopup();
    }
  });

  dataForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const regNo = document.getElementById("regNo").value;
    const dob = document.getElementById("dob").value;
    if (validateInput(regNo, dob)) {
      fetchAttendanceData(regNo, dob)
        .then((data) => {
          const attendancePercentage = calculateAttendancePercentage(data.attend, data.total_number);
          showPopup(`Your attendance percentage is ${attendancePercentage.toFixed(2)}%.`);
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
  }

  function validateInput(regNo, dob) {
    return regNo && dob && !isNaN(regNo);
  }

  function calculateAttendancePercentage(attend, totalNumber) {
    return (attend / totalNumber) * 100;
  }

  function fetchAttendanceData(regNo, dob) {
    const users = [
      { regNo: "12345", dob: "2024-06-08", total_number: 60, attend: 50 },
      { regNo: "67890", dob: "2024-06-07", total_number: 60, attend: 55 },
      { regNo: "11223", dob: "2024-06-06", total_number: 60, attend: 40 },
      { regNo: "44556", dob: "2024-06-05", total_number: 60, attend: 45 },
      { regNo: "77889", dob: "2024-06-04", total_number: 60, attend: 60 },
      { regNo: "99001", dob: "2024-06-03", total_number: 60, attend: 35 },
    ];

    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const user = users.find(user => user.regNo === regNo && user.dob === dob);
        if (user) {
          resolve(user);
        } else {
          reject("Invalid registration number or date of birth");
        }
      }, 1000);
    });
  }
});
