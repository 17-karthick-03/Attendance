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
          const attendancePercentage = calculateAttendancePercentage(data.attend, data.total_number);
          const searchCount = recordUserSearch(regNo, dob);
          showPopup(`Dear ${data.name},<br>Your attendance percentage is ${attendancePercentage.toFixed(2)}% (${attendancePercentage.toFixed(0)}%).<br>You have searched ${searchCount} times.`);
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
    popupContent.innerHTML = `
      <p>${message}</p>
    `;
    popupContainer.style.display = "flex";
  
    if (!message.includes("Dear")) {
      popupContent.innerHTML += `
        <button style="background: linear-gradient(to right, #FF6F61, #6E8B9E); border-radius: 15px" id="agreeButton">Agree and Continue</button>
      `;
      
      const agreeButton = document.getElementById("agreeButton");
      agreeButton.addEventListener("click", function () {
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
    const users = [
      { regNo: "142222104061", dob: "2004-10-08", name: "HEMNATH N", total_number: 0, attend: 0 },
      { regNo: "142222104062", dob: "2003-10-04", name: "JAHANKUMAR B", total_number: 0, attend: 0 },
      { regNo: "142222104063", dob: "2005-06-25", name: "JANANI R", total_number: 0, attend: 0 },
      { regNo: "142222104064", dob: "2004-08-27", name: "JAYACHANDRAN S", total_number: 0, attend: 0 },
      { regNo: "142222104065", dob: "2004-01-26", name: "JAYAM ARUN VIKRAM S", total_number: 0, attend: 0 },
      { regNo: "142222104066", dob: "2005-03-07", name: "JAYAPRIYA B", total_number: 0, attend: 0 },
      { regNo: "142222104067", dob: "2004-08-28", name: "JAYASHRUDHI S D", total_number: 0, attend: 0 },
      { regNo: "142222104068", dob: "2005-04-03", name: "JEEVANANTHAM B", total_number: 0, attend: 0 },
      { regNo: "142222104069", dob: "2005-06-24", name: "JEEVARAJ S P", total_number: 0, attend: 0 },
      { regNo: "142222104070", dob: "2005-06-24", name: "JESHWA S", total_number: 0, attend: 0 },
      { regNo: "142222104071", dob: "2004-08-01", name: "JOTHI PRAKASH N", total_number: 0, attend: 0 },
      { regNo: "142222104072", dob: "2005-06-25", name: "KABILAN R", total_number: 0, attend: 0 },
      { regNo: "142222104073", dob: "2005-03-17", name: "KARTHICK S", total_number: 0, attend: 0 },
      { regNo: "142222104074", dob: "2005-03-08", name: "KARTHIK S G", total_number: 0, attend: 0 },
      { regNo: "142222104075", dob: "2005-03-17", name: "KARTHIKEYAN D", total_number: 0, attend: 0 },
      { regNo: "142222104076", dob: "2004-12-08", name: "KATHEEB ANSARI", total_number: 0, attend: 0 },
      { regNo: "142222104077", dob: "2005-02-19", name: "KAVEEYA M", total_number: 0, attend: 0 },
      { regNo: "142222104078", dob: "2004-12-15", name: "KAVIYA S", total_number: 0, attend: 0 },
      { regNo: "142222104079", dob: "2004-12-25", name: "KAVYAA K", total_number: 0, attend: 0 },
      { regNo: "142222104080", dob: "2005-04-03", name: "KISHORE M", total_number: 0, attend: 0 },
      { regNo: "142222104081", dob: "2005-05-02", name: "KISHORE M", total_number: 0, attend: 0 },
      { regNo: "142222104082", dob: "2004-11-25", name: "LATCHIYASRI K", total_number: 0, attend: 0 },
      { regNo: "142222104083", dob: "2004-01-30", name: "LINGEESHWAR T S", total_number: 0, attend: 0 },
      { regNo: "142222104084", dob: "2004-09-03", name: "LOGESHWARAN S", total_number: 0, attend: 0 },
      { regNo: "142222104085", dob: "2004-06-14", name: "LOKESH SUNDAR R U", total_number: 0, attend: 0 },
      { regNo: "142222104086", dob: "2005-09-21", name: "MADHESH KUMAR S", total_number: 0, attend: 0 },
      { regNo: "142222104087", dob: "2004-09-13", name: "MADHUMITHA S", total_number: 0, attend: 0 },
      { regNo: "142222104088", dob: "2004-09-12", name: "MANOJ R", total_number: 0, attend: 0 },
      { regNo: "142222104089", dob: "2004-05-06", name: "MAARISHWARAN S V", total_number: 0, attend: 0 },
      { regNo: "142222104090", dob: "2005-06-23", name: "MEITHAVAM T", total_number: 0, attend: 0 },
      { regNo: "142222104091", dob: "2004-09-14", name: "MOHAMED HARUN RAZEED T", total_number: 0, attend: 0 },
      { regNo: "142222104092", dob: "2004-08-17", name: "MONIKA S", total_number: 0, attend: 0 },
      { regNo: "142222104093", dob: "2005-02-23", name: "MUKESHH R", total_number: 0, attend: 0 },
      { regNo: "142222104094", dob: "2005-07-10", name: "MUKESH KUMAR B", total_number: 0, attend: 0 },
      { regNo: "142222104095", dob: "2005-09-30", name: "MURALI KRISHNA L K", total_number: 0, attend: 0 },
      { regNo: "142222104096", dob: "2004-10-04", name: "NAUSHEEN BEGUM S", total_number: 0, attend: 0 },
      { regNo: "142222104097", dob: "2004-04-09", name: "NAVEEN S", total_number: 0, attend: 0 },
      { regNo: "142222104098", dob: "2005-10-08", name: "NAVEEN KUMAR S", total_number: 0, attend: 0 },
      { regNo: "142222104099", dob: "2003-06-13", name: "NIKHIL B", total_number: 0, attend: 0 },
      { regNo: "142222104100", dob: "2004-11-14", name: "NISHA M", total_number: 0, attend: 0 },
      { regNo: "142222104101", dob: "2004-09-20", name: "NITHISH KANNA P", total_number: 0, attend: 0 },
      { regNo: "142222104102", dob: "2004-12-13", name: "PAVITHRA A", total_number: 0, attend: 0 },
      { regNo: "142222104103", dob: "2003-11-01", name: "PAVITHRA K", total_number: 0, attend: 0 },
      { regNo: "142222104104", dob: "2004-11-17", name: "PONKIRRUTHICK K", total_number: 0, attend: 0 },
      { regNo: "142222104105", dob: "2005-04-22", name: "POORNIMA S M", total_number: 0, attend: 0 },
      { regNo: "142222104106", dob: "2004-06-25", name: "PRANAV R", total_number: 0, attend: 0 },
      { regNo: "142222104107", dob: "2004-10-15", name: "PRANAVAKUMAR S", total_number: 0, attend: 0 },
      { regNo: "142222104108", dob: "2004-11-09", name: "PRASANNAKUMAR K K", total_number: 0, attend: 0 },
      { regNo: "142222104109", dob: "2004-10-18", name: "PRASANNARAJ G", total_number: 0, attend: 0 },
      { regNo: "142222104110", dob: "2005-06-12", name: "PRAVEEN RAJ P", total_number: 0, attend: 0 },
      { regNo: "142222104111", dob: "2004-07-11", name: "PRITHIV RITHAN S", total_number: 0, attend: 0 },
      { regNo: "142222104112", dob: "2005-05-20", name: "PUGAZHMANI T", total_number: 0, attend: 0 },
      { regNo: "142222104113", dob: "2004-09-17", name: "RAGUL P", total_number: 0, attend: 0 },
      { regNo: "142222104114", dob: "2004-09-26", name: "RAGUL R", total_number: 0, attend: 0 },
      { regNo: "142222104115", dob: "2004-11-22", name: "RAGUNATH R", total_number: 0, attend: 0 },
      { regNo: "142222104116", dob: "2004-11-27", name: "RAJALAKSHMI V", total_number: 0, attend: 0 },
      { regNo: "142222104117", dob: "2003-08-31", name: "RAAJASRI C", total_number: 0, attend: 0 },
      { regNo: "142222104118", dob: "2004-01-27", name: "RAMYA V S", total_number: 0, attend: 0 },
      { regNo: "142222104119", dob: "2004-10-08", name: "RANJITH KUMAR M", total_number: 0, attend: 0 },
      { regNo: "142222104120", dob: "2005-03-04", name: "RISHAP M", total_number: 0, attend: 0 },
      { regNo: "142222104305", dob: "2004-12-16", name: "GOPINATH V", total_number: 0, attend: 0 },
      { regNo: "142222104306", dob: "2005-08-28", name: "GURU PRASANTH V", total_number: 0, attend: 0 },
      { regNo: "142222104307", dob: "2001-05-13", name: "JEROME SAMUEL D", total_number: 0, attend: 0 }
    ];

    return new Promise((resolve, reject) => {
      const user = users.find((u) => u.regNo === regNo && u.dob === dob);
      if (user) {
        resolve(user);
      } else {
        reject("User not found");
      }
    });
  }

  function recordUserSearch(regNo, dob) {
    const searches = JSON.parse(localStorage.getItem("userSearches")) || [];
    const currentUserSearches = searches.filter((search) => search.regNo === regNo && search.dob === dob);
    searches.push({ regNo, dob, timestamp: new Date().toISOString() });
    localStorage.setItem("userSearches", JSON.stringify(searches));
    return currentUserSearches.length + 1;
  }
});
