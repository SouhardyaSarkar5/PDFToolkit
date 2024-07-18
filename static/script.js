function displayFileNames(input) {
    var fileList = document.getElementById('file-list');
    fileList.innerHTML = '';
    for (var i = 0; i < input.files.length; i++) {
        var fileItem = document.createElement('div');
        fileItem.textContent = input.files[i].name;
        fileList.appendChild(fileItem);
    }
}

function displayFileName(input) {
    var fileList = document.getElementById('split-file-list');
    fileList.innerHTML = '';
    if (input.files.length > 0) {
        var fileItem = document.createElement('div');
        fileItem.textContent = input.files[0].name;
        fileList.appendChild(fileItem);
    }
}

function displayFileName(input, fileListId) {
    const fileList = document.getElementById(fileListId);
    fileList.innerHTML = '';
    for (let i = 0; i < input.files.length; i++) {
        const li = document.createElement('li');
        li.textContent = input.files[i].name;
        fileList.appendChild(li);
    }
}

