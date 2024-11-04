document.addEventListener('DOMContentLoaded', () => {
    fetchQueueData();
    fetchOngoingServicesData();
    setInterval(updateTimers, 1000);
    setInterval(fetchOngoingServicesData, 4000)
    setInterval(fetchQueueData, 4000)  // Update the timers every second
});

function fetchQueueData() {
    fetch('https://autolinkservice.co/queue/queue')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#queue-table-body');
            tableBody.innerHTML = '';  // Clear existing rows

            data.queue.forEach(client => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${client.name}</td>
                    <td>${client.model}</td>
                    <td>${client.license_plate}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching queue data:', error));
}

function fetchOngoingServicesData() {
    fetch('https://autolinkservice.co/queue/queue')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#ongoing-services-table-body');
            tableBody.innerHTML = '';  // Clear existing rows

            data.ongoingServices.forEach(service => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${service.name}</td>
                    <td>${service.model}</td>
                    <td>${service.license_plate}</td>
                    <td>${service.service}</td>
                    <td class="timer-cell" data-start-time="${service.start_time * 1000}" data-duration="${service.duration * 60}">${formatTime(service.duration * 60)}</td>
                `; //aqui fue que hice cambio
                tableBody.appendChild(row);
            });

            updateTimers();  // Initial call to update timers
            setInterval(updateTimers, 1000);  // Update the timers every second
        })
        .catch(error => console.error('Error fetching ongoing services data:', error));
}

function formatTime(timeInSeconds) {
    const mins = Math.floor(timeInSeconds / 60);
    const secs = Math.floor(timeInSeconds % 60);
    return `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

function updateTimers() {
    const timerCells = document.querySelectorAll('.timer-cell');
    timerCells.forEach(cell => {
        const startTime = parseInt(cell.getAttribute('data-start-time'));
        const duration = parseInt(cell.getAttribute('data-duration'));
        const elapsed = ((Date.now() + startTime) / 1000); //aqui fue que hice cambio
        const remainingTime = duration - elapsed % 1000; //aqui fue que hice cambio
        if (remainingTime > 0) {
            cell.innerText = formatTime(remainingTime);
        } else {
            cell.innerText = "0:00";
        }
    });
}
