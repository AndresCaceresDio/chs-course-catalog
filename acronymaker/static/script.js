const maxCells = 23;
let cellCount = 2;
let offset = 0;

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', function(event) {
        if (event.target.classList.contains('wordInput') && event.key === 'Enter') {
            event.preventDefault();
            event.target.blur();
        }
    }, true);

    document.getElementById('synonymForm').addEventListener('submit', (event) => {
        event.preventDefault();
        document.getElementById('acronymResults').innerHTML = '';
        const orderedCheckbox = document.querySelector('input[name="ordered"]');
        const ordered = orderedCheckbox && orderedCheckbox.checked ? 'yes' : 'no';
        const words = [];
        const synonyms = [];

        const wordInputs = Array.from(document.getElementsByClassName('wordInput'));
        wordInputs.forEach((input) => {
            const wordValue = input.value.trim();
            if (wordValue) {
                words.push(wordValue);
                const outputArea = input.nextElementSibling;
                const synonymList = Array.from(outputArea.querySelectorAll('.synonymBubble span')).map((span) => span.textContent.trim());
                synonyms.push(synonymList);
            }
        });

        submitSynonyms(words, synonyms, ordered);
    });

}, false);

function submitSynonyms(words, synonyms, ordered) {
    offset = 0
    const selectMenu = document.getElementById('languageSelect');
    const selectedValue = selectMenu.options[selectMenu.selectedIndex].value;
    fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                words_list: words,
                synonyms_list: synonyms,
                ordered: ordered,
                offset: offset,
                language: selectedValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                offset = data.next_offset;
                displayAcronyms(data.acronyms, words, synonyms, ordered, "submit");
            } else if (data.status === 'failure') {
                message = data.message;
                displayError(message);
            }
        })
        .catch(err => console.error(err));
        };

function displayError(message) {
    const resultsContainer = document.getElementById('acronymResults');
    resultsContainer.innerHTML = '';
    const noneTextArea = document.createElement('textarea');
    noneTextArea.value = message;
    noneTextArea.className = 'outputText';
    noneTextArea.readOnly = true;
    resultsContainer.appendChild(noneTextArea);
}


function loadMoreOnClick(words, synonyms, ordered, existingContainer) {
    const selectMenu = document.getElementById('languageSelect');
    const selectedValue = selectMenu.options[selectMenu.selectedIndex].value;
    fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                words_list: words,
                synonyms_list: synonyms,
                ordered: ordered,
                offset: offset,
                language: selectedValue
            })
        })
        .then(response => response.json())
        .then(data => {
            offset = data.next_offset;
            const newAcronyms = data.acronyms;
            if (newAcronyms.length > 0) {
                displayAcronyms(newAcronyms, words, synonyms, ordered, "resubmit", existingContainer);

                if (newAcronyms.length >= 30) {
                    const loadMoreButton = document.createElement('button');
                    loadMoreButton.textContent = 'Load More';
                    loadMoreButton.className = 'navigatorBtn';
                    loadMoreButton.onclick = function() {
                        loadMoreOnClick(words, synonyms, ordered, existingContainer);
                    };
                    existingContainer.appendChild(loadMoreButton);
                }
            } else {
                const loadMoreButton = existingContainer.querySelector('.navigatorBtn');
                if (loadMoreButton) {
                    loadMoreButton.remove();
                }
            }
        })
        .catch(err => console.error(err));
}


function displayAcronyms(acronyms, words, synonyms, ordered, status, existingContainer = "") {
    if (status === "submit") {
        const resultsContainer = document.getElementById('acronymResults');
        resultsContainer.innerHTML = '';
        if (acronyms.length == 0) {
            const noneTextArea = document.createElement('textarea');
            noneTextArea.value = "No acronyms can be made from that combination. Try adding more words/synonyms or shuffling (if it's ordered).";
            noneTextArea.className = 'outputText';
            noneTextArea.readOnly = true;
            resultsContainer.appendChild(noneTextArea);
        } else {
            acronyms.forEach(acronym => {
                const resultContainer = document.createElement('div');
                resultContainer.className = 'resultContainer';

                const acronymTextArea = document.createElement('textarea');
                acronymTextArea.className = 'outputText';
                acronymTextArea.value = acronym;
                acronymTextArea.readOnly = true;

                const copyButton = document.createElement('button');
                copyButton.className = 'copyBtn';
                copyButton.onclick = function() {
                    acronymTextArea.select();
                    document.execCommand('copy');

                    const copiedPopup = document.createElement('div');
                    copiedPopup.textContent = 'Copied';
                    copiedPopup.className = 'copiedPopup';
                    document.body.appendChild(copiedPopup);

                    setTimeout(() => {
                        copiedPopup.remove();
                    }, 1500);
                };

                const iconOne = document.createElement('i');
                iconOne.className = 'fa-regular fa-copy';
                copyButton.appendChild(iconOne);

                const deleteButton = document.createElement('button');
                deleteButton.className = 'delBtn';
                deleteButton.onclick = function() {
                    resultContainer.remove();
                };
                const iconTwo = document.createElement('i');
                iconTwo.className = 'fa-solid fa-trash';
                deleteButton.appendChild(iconTwo);

                resultContainer.appendChild(acronymTextArea);
                resultContainer.appendChild(copyButton);
                resultContainer.appendChild(deleteButton);

                resultsContainer.appendChild(resultContainer);
            });

            const loadMoreButton = document.createElement('button');
            loadMoreButton.textContent = 'Load More';
            loadMoreButton.className = 'navigatorBtn';
            loadMoreButton.onclick = function() {
                loadMoreOnClick(words, synonyms, ordered, resultsContainer);
            };

            resultsContainer.appendChild(loadMoreButton);
        }
    } else if (status === "resubmit") {
        const loadMoreButton = existingContainer.querySelector('.navigatorBtn');
        acronyms.forEach(acronym => {
            const resultContainer = document.createElement('div');
            resultContainer.className = 'resultContainer';

            const acronymTextArea = document.createElement('textarea');
            acronymTextArea.className = 'outputText';
            acronymTextArea.value = acronym;
            acronymTextArea.readOnly = true;

            const copyButton = document.createElement('button');
            copyButton.className = 'copyBtn';
            copyButton.onclick = function() {
                acronymTextArea.select();
                document.execCommand('copy');

                const copiedPopup = document.createElement('div');
                copiedPopup.textContent = 'Copied';
                copiedPopup.className = 'copiedPopup';
                document.body.appendChild(copiedPopup);

                setTimeout(() => {
                    copiedPopup.remove();
                }, 1500);
            };

            const iconOne = document.createElement('i');
            iconOne.className = 'fa-regular fa-copy';
            copyButton.appendChild(iconOne);

            const deleteButton = document.createElement('button');
            deleteButton.className = 'delBtn';
            deleteButton.onclick = function() {
                resultContainer.remove();
            };
            const iconTwo = document.createElement('i');
            iconTwo.className = 'fa-solid fa-trash';
            deleteButton.appendChild(iconTwo);

            resultContainer.appendChild(acronymTextArea);
            resultContainer.appendChild(copyButton);
            resultContainer.appendChild(deleteButton);

            existingContainer.insertBefore(resultContainer, loadMoreButton);
        });
    }
}

function getSynonyms(input) {
    const outputArea = input.nextElementSibling;
    outputArea.innerHTML = '';
    const wordInputs = Array.from(document.getElementsByClassName('wordInput'));
    const duplicateWords = [];
    wordInputs.forEach((input) => {
        duplicateWords.push(input.value.toLowerCase());
    });
    const synonymBubbles = Array.from(document.getElementsByClassName('synonymBubble'));
    const existingSynonyms = [];
    synonymBubbles.forEach((bubble) => {
        existingSynonyms.push(bubble.textContent.trim().slice(0, -1).toLowerCase());
    });
    if (duplicateWords.filter(word => word.toLowerCase() === input.value.trim().toLowerCase()).length > 1 || existingSynonyms.includes(input.value.trim().toLowerCase())) {
        input.value = '';
        return;
    }
    if (input.value.trim() !== '') {
        const addButton = document.createElement('button');
        addButton.className = 'addSynonymBtn';
        addButton.textContent = '+';
        addButton.type = 'button';
        addButton.onclick = () => createEditableBubble(outputArea);
        outputArea.appendChild(addButton);
    }
    const nextInput = input.parentNode.nextElementSibling?.querySelector('.wordInput');
    if (nextInput) {
        nextInput.focus();
    }
}


function createEditableBubble(outputArea) {
    const existingSynonyms = outputArea.querySelectorAll('.synonymBubble').length;
    if (existingSynonyms < 10) {
        const editableBubble = document.createElement('input');
        editableBubble.type = 'text';
        editableBubble.className = 'synonymBubble editMode';
        editableBubble.onblur = () => saveSynonym(editableBubble);
        editableBubble.oninput = () => adjustWidthOfInput(editableBubble);
        editableBubble.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                saveSynonym(editableBubble);
            }
        });

        outputArea.insertBefore(editableBubble, outputArea.lastChild);
        editableBubble.focus();
    }
}

function saveSynonym(editableBubble) {
    const word = editableBubble.value.trim();
    const parentCell = editableBubble.closest('.cell');
    const wordInput = parentCell.querySelector('.wordInput');
    const existingSynonyms = parentCell.querySelectorAll('.synonymBubble span');
    const isDuplicate = Array.from(existingSynonyms).some(span => span.textContent.trim().toLowerCase() === word.toLowerCase());

    if (word.toLowerCase() && word.toLowerCase() !== wordInput.value.trim().toLowerCase() && !isDuplicate) {
        editableBubble.replaceWith(createSynonymBubble(word));
    } else {
        editableBubble.remove();
    }
}


function adjustWidthOfInput(input) {
    const tempSpan = document.createElement('span');
    tempSpan.style.position = 'absolute';
    tempSpan.style.height = 'auto';
    tempSpan.style.width = 'auto';
    tempSpan.style.whiteSpace = 'nowrap';
    tempSpan.textContent = input.value.replace(/ /g, "\u00a0");
    document.body.appendChild(tempSpan);

    const inputWidth = tempSpan.offsetWidth + 30;

    input.style.width = `${inputWidth}px`;

    document.body.removeChild(tempSpan);
}

function createSynonymBubble(word) {
    const bubble = document.createElement('div');
    bubble.className = 'synonymBubble';

    const wordSpan = document.createElement('span');
    wordSpan.textContent = word;
    bubble.appendChild(wordSpan);

    const removeBtn = document.createElement('button');
    removeBtn.className = 'removeBtn';
    removeBtn.textContent = 'x';
    removeBtn.onclick = () => bubble.remove();
    bubble.appendChild(removeBtn);
    return bubble;
}

function removeCell(cell) {
    event.preventDefault();
    const grid = document.querySelector('.grid');
    if (cellCount > 2) {
        grid.removeChild(cell);
        cellCount--;
    }
}

function addCell() {
    if (cellCount < maxCells) {
        const grid = document.querySelector('.grid');
        const cell = document.createElement('div');
        cell.className = 'cell';
        const removeButton = document.createElement('button');
        removeButton.className = 'removeBtn';
        removeButton.type = 'button';
        removeButton.textContent = 'x';
        removeButton.onclick = () => removeCell(cell);
        const wordInput = document.createElement('input');
        wordInput.placeholder = "Enter a word";
        wordInput.type = 'text';
        wordInput.className = 'wordInput';
        wordInput.onblur = () => getSynonyms(wordInput);
        wordInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                event.target.blur();
            }
        });

        const outputArea = document.createElement('div');
        outputArea.className = 'outputArea';
        cell.appendChild(removeButton);
        cell.appendChild(wordInput);
        cell.appendChild(outputArea);
        grid.insertBefore(cell, document.getElementById('addCellBtn'));
        cellCount++;
    }
}

function shuffleGrid() {
    const grid = document.querySelector('.grid');
    const cells = Array.from(grid.children).filter(cell => !cell.classList.contains('add-cell'));
    let shuffled = false;

    while (!shuffled) {
        let originalOrder = cells.map((cell) => cell.querySelector('.wordInput')?.value || '');
        for (let i = cells.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cells[i], cells[j]] = [cells[j], cells[i]];
        }
        let newOrder = cells.map((cell) => cell.querySelector('.wordInput')?.value || '');
        if (!arraysEqual(originalOrder, newOrder)) {
            shuffled = true;
        }
    }
    const newGrid = document.createElement('div');
    newGrid.className = 'grid';
    cells.forEach(cell => newGrid.appendChild(cell));
    newGrid.appendChild(document.getElementById('addCellBtn'));
    grid.replaceWith(newGrid);
}

function arraysEqual(arr1, arr2) {
    if (arr1.length !== arr2.length) return false;
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) return false;
    }
    return true;
}
