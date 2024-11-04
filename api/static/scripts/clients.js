document.addEventListener('DOMContentLoaded', () => {
    fetchClientsData();

    // Event listener for search button click to filter clients
    document.getElementById('search-button').addEventListener('click', () => {
        const query = document.getElementById('search-box').value.toLowerCase();
        filterClients(query);
    });
});

function fetchClientsData() {
    console.log("Fetching clients data..."); // Debugging message
    fetch('https://autolinkservice.co/client/clients')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Data fetched:", data); // Debugging message
            const tableBody = document.querySelector('#clients-table tbody');
            tableBody.innerHTML = '';  // Clear existing rows

            data.forEach(client => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${client.first_name}</td>
                    <td>${client.model}</td>
                    <td>${client.license_plate}</td>
                    <td>
                        <button class="add-to-queue-button" data-client-info='${JSON.stringify(client)}'>Add to Queue</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            document.querySelectorAll('.add-to-queue-button').forEach(button => {
                button.addEventListener('click', () => {
                    const clientInfo = JSON.parse(button.getAttribute('data-client-info'));
                    const queueItem = {
                        name: clientInfo.first_name,
                        model: clientInfo.model,
                        license_plate: clientInfo.license_plate
                    };
                    addToQueue(queueItem);
                });
            });
        })
        .catch(error => console.error('Error fetching clients data:', error));
}

function filterClients(query) {
    const rows = document.querySelectorAll('#clients-table tbody tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const name = cells[0].innerText.toLowerCase();
        const model = cells[1].innerText.toLowerCase();
        const licensePlate = cells[2].innerText.toLowerCase();
        if (name.includes(query) || model.includes(query) || licensePlate.includes(query)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function addToQueue(queueItem) {
    console.log("Adding to queue:", queueItem); // Debugging message
    fetch('https://autolinkservice.co/queue/queue/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(queueItem)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        showPopup('Client added to queue!');
    })
    .catch(error => {
        console.error('Error adding client to queue:', error);
        showPopup('Error adding client to queue.');
    });
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

function closePopup() {
    document.getElementById('popup-alert').style.display = 'none';
}
