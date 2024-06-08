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
      { regNo: "142222104061", dob: "2004-10-08", total_number: 0, attend: 0 },
      { regNo: "142222104062", dob: "2003-10-04", total_number: 0, attend: 0 },
      { regNo: "142222104063", dob: "2005-06-25", total_number: 0, attend: 0 },
      { regNo: "142222104064", dob: "2004-08-27", total_number: 0, attend: 0 },
      { regNo: "142222104065", dob: "2004-01-26", total_number: 0, attend: 0 },
      { regNo: "142222104066", dob: "2005-03-07", total_number: 0, attend: 0 },
      { regNo: "142222104067", dob: "2004-08-28", total_number: 0, attend: 0 },
      { regNo: "142222104068", dob: "2005-04-03", total_number: 0, attend: 0 },
      { regNo: "142222104069", dob: "2005-06-24", total_number: 0, attend: 0 },
      { regNo: "142222104070", dob: "2005-06-24", total_number: 0, attend: 0 },
      { regNo: "142222104071", dob: "2004-08-01", total_number: 0, attend: 0 },
      { regNo: "142222104072", dob: "2005-06-25", total_number: 0, attend: 0 },
      { regNo: "142222104073", dob: "2005-03-17", total_number: 0, attend: 0 },
      { regNo: "142222104074", dob: "2005-03-08", total_number: 0, attend: 0 },
      { regNo: "142222104075", dob: "2005-03-17", total_number: 0, attend: 0 },
      { regNo: "142222104076", dob: "2004-12-08", total_number: 0, attend: 0 },
      { regNo: "142222104077", dob: "2005-02-19", total_number: 0, attend: 0 },
      { regNo: "142222104078", dob: "2004-12-15", total_number: 0, attend: 0 },
      { regNo: "142222104079", dob: "2004-12-25", total_number: 0, attend: 0 },
      { regNo: "142222104080", dob: "2005-04-03", total_number: 0, attend: 0 },
      { regNo: "142222104081", dob: "2005-05-02", total_number: 0, attend: 0 },
      { regNo: "142222104082", dob: "2004-11-25", total_number: 0, attend: 0 },
      { regNo: "142222104083", dob: "2004-01-30", total_number: 0, attend: 0 },
      { regNo: "142222104084", dob: "2004-09-03", total_number: 0, attend: 0 },
      { regNo: "142222104085", dob: "2004-06-14", total_number: 0, attend: 0 },
      { regNo: "142222104086", dob: "2005-09-21", total_number: 0, attend: 0 },
      { regNo: "142222104087", dob: "2004-09-13", total_number: 0, attend: 0 },
      { regNo: "142222104088", dob: "2004-09-12", total_number: 0, attend: 0 },
      { regNo: "142222104089", dob: "2004-05-06", total_number: 0, attend: 0 },
      { regNo: "142222104090", dob: "2005-06-23", total_number: 0, attend: 0 },
      { regNo: "142222104091", dob: "2004-09-14", total_number: 0, attend: 0 },
      { regNo: "142222104092", dob: "2004-08-17", total_number: 0, attend: 0 },
      { regNo: "142222104093", dob: "2005-02-23", total_number: 0, attend: 0 },
      { regNo: "142222104094", dob: "2005-07-10", total_number: 0, attend: 0 },
      { regNo: "142222104095", dob: "2005-09-30", total_number: 0, attend: 0 },
      { regNo: "142222104096", dob: "2004-04-11", total_number: 0, attend: 0 },
      { regNo: "142222104097", dob: "2004-04-09", total_number: 0, attend: 0 },
      { regNo: "142222104098", dob: "2005-10-08", total_number: 0, attend: 0 },
      { regNo: "142222104099", dob: "2003-06-13", total_number: 0, attend: 0 },
      { regNo: "142222104100", dob: "2004-11-14", total_number: 0, attend: 0 },
      { regNo: "142222104101", dob: "2004-09-20", total_number: 0, attend: 0 },
      { regNo: "142222104102", dob: "2004-12-13", total_number: 0, attend: 0 },
      { regNo: "142222104103", dob: "2003-11-01", total_number: 0, attend: 0 },
      { regNo: "142222104104", dob: "2004-11-17", total_number: 0, attend: 0 },
      { regNo: "142222104105", dob: "2005-04-22", total_number: 0, attend: 0 },
      { regNo: "142222104106", dob: "2004-06-25", total_number: 0, attend: 0 },
      { regNo: "142222104107", dob: "2004-10-15", total_number: 0, attend: 0 },
      { regNo: "142222104108", dob: "2004-11-09", total_number: 0, attend: 0 },
      { regNo: "142222104109", dob: "2004-10-18", total_number: 0, attend: 0 },
      { regNo: "142222104110", dob: "2005-06-12", total_number: 0, attend: 0 },
      { regNo: "142222104111", dob: "2004-07-11", total_number: 0, attend: 0 },
      { regNo: "142222104112", dob: "2005-05-20", total_number: 0, attend: 0 },
      { regNo: "142222104113", dob: "2004-09-17", total_number: 0, attend: 0 },
      { regNo: "142222104114", dob: "2004-09-26", total_number: 0, attend: 0 },
      { regNo: "142222104115", dob: "2004-11-22", total_number: 0, attend: 0 },
      { regNo: "142222104116", dob: "2004-11-27", total_number: 0, attend: 0 },
      { regNo: "142222104117", dob: "2003-08-31", total_number: 0, attend: 0 },
      { regNo: "142222104118", dob: "2004-01-27", total_number: 0, attend: 0 },
      { regNo: "142222104119", dob: "2004-10-08", total_number: 0, attend: 0 },
      { regNo: "142222104120", dob: "2005-03-04", total_number: 0, attend: 0 },
      { regNo: "142222104305", dob: "2004-12-16", total_number: 0, attend: 0 },
      { regNo: "142222104306", dob: "2005-08-28", total_number: 0, attend: 0 },
      { regNo: "142222104307", dob: "2001-05-13", total_number: 0, attend: 0 }
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
