let fromDate, toDate;

document.getElementById('from-date').addEventListener('change', function() {
  fromDate = new Date(this.value);
  if (toDate) {
    displayCalendar(fromDate, toDate);
  } else {
    displayCalendar(fromDate);
  }
});

document.getElementById('to-date').addEventListener('change', function() {
  toDate = new Date(this.value);
  if (fromDate) {
    displayCalendar(fromDate, toDate);
  }
});

document.getElementById('prev-btn').addEventListener('click', function() {
  if (fromDate) {
    displayCalendar(fromDate, toDate);
  }
});

document.getElementById('next-btn').addEventListener('click', function() {
  if (toDate) {
    displayCalendar(toDate, fromDate);
  }
});

function displayCalendar(startDate, endDate = null) {
  const options = { year: 'numeric', month: 'long' };
  const monthYear = startDate.toLocaleDateString('en-US', options);
  const calendarDiv = document.getElementById('calendar');
  calendarDiv.innerHTML = '<h3 class="text-xl font-semibold mb-3">' + monthYear + '</h3>';

  // Calendar grid logic
  let daysInMonth = new Date(startDate.getFullYear(), startDate.getMonth() + 1, 0).getDate();
  let firstDay = new Date(startDate.getFullYear(), startDate.getMonth(), 1).getDay();

  let calendarHTML = '<div class="grid grid-cols-7 gap-2">';
  let dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Display day names
  for (let day of dayNames) {
    calendarHTML += '<div class="text-center py-2">' + day + '</div>';
  }

  // Empty spaces before the first day of the month
  for (let i = 0; i < firstDay; i++) {
    calendarHTML += '<div></div>';
  }

  // Highlight dates between fromDate and toDate
  for (let day = 1; day <= daysInMonth; day++) {
    let currentDate = new Date(startDate.getFullYear(), startDate.getMonth(), day);
    let highlightClass = '';

    if (endDate && fromDate && toDate) {
      // Highlight if the current date is between fromDate and toDate
      let start = fromDate < toDate ? fromDate : toDate;
      let end = fromDate > toDate ? fromDate : toDate;
      if (currentDate >= start && currentDate <= end) {
        highlightClass = 'highlight';
      }
    }

    calendarHTML += '<div class="text-center py-2 ' + highlightClass + '">' + day + '</div>';
  }

  calendarHTML += '</div>';
  calendarDiv.innerHTML += calendarHTML;
}