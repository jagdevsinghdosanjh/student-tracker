const token = localStorage.getItem('token');
fetch('/scores/analytics/subject-averages', {
  headers: { 'Authorization': 'Bearer ' + token }
})
.then(res => res.json())
.then(data => {
  const subjects = data.map(x => x.subject);
  const averages = data.map(x => x.average);
  new Chart(document.getElementById('subjectChart'), {
    type: 'bar',
    data: {
      labels: subjects,
      datasets: [{ label: 'Average %', data: averages, backgroundColor: 'steelblue' }]
    },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
  });
});
