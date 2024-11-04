document.addEventListener('DOMContentLoaded', () => {
    fetchQueueData();
    setInterval(resetVisitsCount, 86400000);   // Refresh every 24 hours
});

document.getElementById('add-client-button').addEventListener('click', function() {
    const clientName = document.getElementById('client-name').value;
    if (clientName) {
        fetch(`https://autolinkservice.co/queue/queue/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: clientName })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchQueueData();
            showPopup('Client added to queue!');
        })
        .catch(error => {
            console.error('Error adding client to queue:', error);
            showPopup('Error adding client to queue.');
        });
    }
});

function fetchQueueData() {
    fetch('https://autolinkservice.co/queue/queue')
        .then(response => response.json())
        .then(data => {
            if (!data.queue || !data.ongoingServices) {
                throw new Error('Invalid response structure');
            }

            const queueTableBody = document.querySelector('#queue-table-body');
            const ongoingServicesTableBody = document.querySelector('#ongoing-services-table-body');
            queueTableBody.innerHTML = '';  // Clear existing rows
            ongoingServicesTableBody.innerHTML = '';  // Clear existing rows

            // Populate Queue Table
            data.queue.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.model}</td>
                    <td>${item.license_plate}</td>
                    <td>
                        <button class="start-service-button">Start Service</button>
                    </td>
                `;
                queueTableBody.appendChild(row);
            });

            // Populate Ongoing Services Table
            data.ongoingServices.forEach(item => {
                const remainingTime = calculateRemainingTime(item);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.model}</td>
                    <td>${item.license_plate}</td>
                    <td>
                        <select class="service-dropdown">
                            <option value="Select Service">Select Service</option>
                            <option value="Oil Change" data-time="35" ${item.service === "Oil Change" ? "selected" : ""}>Oil Change</option>
                            <option value="Front Train" data-time="90" ${item.service === "Front Train" ? "selected" : ""}>Front Train</option>
                            <option value="ABS" data-time="30" ${item.service === "ABS" ? "selected" : ""}>ABS</option>
                            <option value="Check Engine" data-time="40" ${item.service === "Check Engine" ? "selected" : ""}>Check Engine</option>
                            <option value="Test" data-time="1" ${item.service === "Test" ? "selected" : ""}>Test</option>
                        </select>
                    </td>
                    <td class="timer-cell">${formatTime(remainingTime)}</td>
                    <td>
                        <select class="status-dropdown">
                            <option value="Pending" ${item.status === "Pending" ? "selected" : ""}>Pending</option>
                            <option value="In Process" ${item.status === "In Process" ? "selected" : ""}>In Process</option>
                            <option value="Completed" ${item.status === "Completed" ? "selected" : ""}>Completed</option>
                        </select>
                    </td>
                    <td>
                        <button class="update-button">Update</button>
                    </td>
                `;
                ongoingServicesTableBody.appendChild(row);
            });

            document.querySelectorAll('.start-service-button').forEach((button, index) => {
                button.addEventListener('click', () => {
                    const row = queueTableBody.rows[index];
                    const clientName = row.querySelector('td').innerText;
                    const model = row.cells[1].innerText;
                    const license_plate = row.cells[2].innerText;
                    fetch(`https://autolinkservice.co/queue/start_service`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ name: clientName, model: model, license_plate: license_plate })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                        fetchQueueData();
                        showPopup('Service started!');
                    })
                    .catch(error => {
                        console.error('Error starting service:', error);
                        showPopup('Error starting service.');
                    });
                });
            });

            document.querySelectorAll('.service-dropdown').forEach((dropdown, index) => {
                dropdown.addEventListener('change', () => {
                    const selectedOption = dropdown.options[dropdown.selectedIndex];
                    const time = selectedOption.getAttribute('data-time');
                    const timerCell = ongoingServicesTableBody.rows[index].querySelector('.timer-cell');
                    if (time) {
                        const serviceData = {
                            name: ongoingServicesTableBody.rows[index].cells[0].innerText,
                            model: ongoingServicesTableBody.rows[index].cells[1].innerText,
                            license_plate: ongoingServicesTableBody.rows[index].cells[2].innerText,
                            service: selectedOption.value,
                            startTime: Date.now(),
                            duration: time,
                            status: "Pending"
                        };
                        localStorage.setItem(`serviceData_${serviceData.name}`, JSON.stringify(serviceData));
                        timerCell.innerText = `00:${time}`;
                    }
                });
            });

            document.querySelectorAll('.update-button').forEach((button, index) => {
                button.addEventListener('click', () => {
                    const row = ongoingServicesTableBody.rows[index];
                    const statusDropdown = row.querySelector('.status-dropdown');
                    const serviceDropdown = row.querySelector('.service-dropdown');
                    const timerCell = row.querySelector('.timer-cell');
                    const clientName = row.cells[0].innerText;
                    const model = row.cells[1].innerText;
                    const license_plate = row.cells[2].innerText;

                    if (statusDropdown.value === 'In Process') {
                        const selectedOption = serviceDropdown.options[serviceDropdown.selectedIndex];
                        const time = selectedOption.getAttribute('data-time');
                        if (time) {
                            const serviceData = {
                                name: clientName,
                                model: model,
                                license_plate: license_plate,
                                service: selectedOption.value,
                                startTime: Date.now(),
                                duration: time,
                                status: "In Process"
                            };
                            localStorage.setItem(`serviceData_${clientName}`, JSON.stringify(serviceData));
                            startTimer(timerCell, time);
                            updateServiceOnServer(serviceData);
                            showPopup('Service updated!');
                        }
                    }

                    if (statusDropdown.value === 'Completed') {
                        const serviceData = {
                            name: clientName,
                            model: model,
                            license_plate: license_plate,
                            service: serviceDropdown.value,
                            status: "Completed"
                        };
                        fetch(`https://autolinkservice.co/queue/queue/${clientName}`, {
                            method: 'DELETE'
                        })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            }
                            throw new Error('Network response was not ok.');
                        })
                        .then(data => {
                            console.log(data.message);
                            localStorage.removeItem(`serviceData_${clientName}`);
                            showPopup('Service completed.');
                            sendEmail();
                            fetchQueueData();
                        })
                        .catch(error => {
                            console.error('Error deleting client from queue:', error);
                            showPopup('Error completing service.');
                        });
                    }
                });
            });

            restoreTimerState();
            fetchStats();
        })
        .catch(error => console.error('Error fetching queue data:', error));
}

function calculateRemainingTime(service) {
    const elapsedTime = (Date.now() - service.startTime) / 1000; // in seconds
    const remainingTime = (service.duration * 60) - elapsedTime;
    return remainingTime > 0 ? remainingTime : 0;
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

function restoreTimerState() {
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('serviceData_')) {
            const serviceData = JSON.parse(localStorage.getItem(key));
            const row = Array.from(document.querySelectorAll('#ongoing-services-table-body tr')).find(tr => {
                return tr.cells[0].innerText === serviceData.name &&
                       tr.cells[1].innerText === serviceData.model &&
                       tr.cells[2].innerText === serviceData.license_plate;
            });

            if (row) {
                const remainingTime = calculateRemainingTime(serviceData);
                if (remainingTime > 0) {
                    const timerCell = row.querySelector('.timer-cell');
                    row.querySelector('.service-dropdown').value = serviceData.service;
                    row.querySelector('.status-dropdown').value = serviceData.status;
                    startTimer(timerCell, remainingTime / 60);
                } else {
                    localStorage.removeItem(key);
                }
            }
        }
    }
}

function updateServiceOnServer(serviceData) {
    fetch(`https://autolinkservice.co/queue/update_service`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(serviceData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => console.error('Error updating service:', error));
}

function fetchStats() {
    fetch('https://autolinkservice.co/queue/stats')
        .then(response => response.json())
        .then(data => {
            updateCounters(data.queue_count, data.visits_count);
        })
        .catch(error => console.error('Error fetching stats:', error));
}

function updateCounters(queueCount, visitsCount) {
    document.getElementById('queue-count').innerText = queueCount;
    document.getElementById('visits-count').innerText = visitsCount;
}

function resetVisitsCount() {
    fetch('https://autolinkservice.co/queue/reset_visits_count', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchStats();  // Refresh the stats to show the updated visits count
    })
    .catch(error => console.error('Error resetting visits count:', error));
}

function startTimer(cell, minutes) {
    let time = minutes * 60;
    const interval = setInterval(() => {
        const mins = Math.floor(time / 60);
        const secs = Math.floor(time % 60);
        cell.innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        time--;

        if (time < 0) {
            clearInterval(interval);
            if (cell.innerText !== 'Completed') {
                showPopup('Service updated!');
                // If the timer wasn't updated to 'Completed', start a new countdown of 15 minutes
                startExtraTimer(cell, 15);
            }
        }
    }, 1000);
}

function startExtraTimer(cell, minutes) {
    let time = minutes * 60;
    const interval = setInterval(() => {
        const mins = Math.floor(time / 60);
        const secs = Math.floor(time % 60);
        cell.innerText = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        time--;

        if (time < 0) {
            clearInterval(interval);
        }
    }, 1000);
}

function showPopup(message) {
    const popup = document.getElementById('popup-alert');
    const popupMessage = document.getElementById('popup-message');
    popupMessage.innerText = message;
    popup.style.display = 'block';

    // Hide the popup after 5 seconds
    setTimeout(() => {
        popup.style.display = 'none';
    }, 2000);
}

function sendEmail() {
    fetch('https://autolinkservice.co/queue/send-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: 'manuelmoralesdiaz0@gmail.com',
            service: {
                name: 'Service Update',
                model: 'Your car model',
                license_plate: 'Your license plate',
                service: 'Service completed',
                status: 'Completed'
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Email sent:', data.message);
    })
    .catch(error => console.error('Error sending email:', error));
}

function closePopup() {
    document.getElementById('popup-alert').style.display = 'none';
}
