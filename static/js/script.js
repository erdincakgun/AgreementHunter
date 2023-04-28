const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');

dropzone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFiles(files);
});

dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropzone.classList.add('active');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('active');
});

dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropzone.classList.remove('active');
    const files = event.dataTransfer.files;
    handleFiles(files);
});

function showProgressBar() {
    const progressBar = document.getElementById('uploadProgress');
    progressBar.value = 0;
    progressBar.style.display = 'block';
}

function hideProgressBar() {
    const progressBar = document.getElementById('uploadProgress');
    progressBar.style.display = 'none';
}

function validateFileType(file) {
    const allowedExtensions = /(\.wav)$/i;
    return allowedExtensions.exec(file.name);
}

function updateDropzoneText(text) {
    const dropzoneText = dropzone.querySelector('p');
    dropzoneText.innerText = text;
}

function handleFiles(files) {
    if (files.length === 0) {
        alert('No files selected');
        return;
    }

    const file = files[0];

    if (!validateFileType(file)) {
        alert('Invalid file type. Please upload a .wav file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    showProgressBar();
    updateDropzoneText('Processing...');

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable) {
            const progressBar = document.getElementById('uploadProgress');
            const progress = Math.round((event.loaded * 100) / event.total);
            progressBar.value = progress;
        }
    });

    xhr.addEventListener('load', (event) => {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            console.log('File uploaded successfully:', response);
            window.location.href = '/admin';
        } else {
            console.error('Error uploading file:', xhr.statusText);
            alert('Error uploading file:', xhr.statusText)
        }
        hideProgressBar();
        updateDropzoneText('Drag and drop files here or click to upload');
    });

    xhr.addEventListener('error', () => {
        console.error('Error uploading file:', xhr.statusText);
        hideProgressBar();
        updateDropzoneText('Drag and drop files here or click to upload');
        alert('Error uploading file:', xhr.statusText)
    });

    xhr.open('POST', '/upload', true);
    xhr.send(formData);
}
