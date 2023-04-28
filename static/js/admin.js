document.addEventListener('DOMContentLoaded', () => {
    fetch('/records')
        .then((response) => response.json())
        .then((records) => {
            populateRecordsTable(records);
        })
        .catch((error) => {
            console.error('Error fetching records:', error);
        });
});

function playAudio(id) {
    const audio = document.getElementById(`audio-${id}`);
    const btn = document.getElementById(`btn-audio-${id}`);


    if (audio.paused) {
        audio.play();
        btn.innerHTML = '&#9209;'
    } else {
        audio.pause();
        btn.innerHTML = '&#9654;'
    }
}

function populateRecordsTable(records) {
    const tableBody = document.querySelector('#recordsTable tbody');

    records.forEach((record) => {

        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${record.id}</td>
            <td>${record.date}</td>

            <td><audio id="audio-${record.id}" src="${record.record_file}" preload="none" style="display:none;"></audio>
            <button id="btn-audio-${record.id}" class="play-btn" onclick="playAudio('${record.id}')">&#9654;</button>
            <a href="${record.record_file}" download class="download-btn">&#x21E9;</a>
            </td>

            <td>${record.transcript}</td>
            <td>${record.aggreement_price}</td>
        `;

        tableBody.appendChild(row);
    });
}