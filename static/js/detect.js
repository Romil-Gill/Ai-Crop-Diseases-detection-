document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const preview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const prompt = document.getElementById('drop-zone-prompt');

    // 1. CLICK TO UPLOAD
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    // 2. DRAG & DROP LOGIC
    ['dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    dropZone.addEventListener('dragover', () => dropZone.classList.add('drop-zone--over'));
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drop-zone--over'));
    
    dropZone.addEventListener('drop', (e) => {
        dropZone.classList.remove('drop-zone--over');
        const file = e.dataTransfer.files[0];
        handleFile(file);
    });

    // 3. FILE PREVIEW
    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                previewContainer.classList.remove('hidden');
                prompt.classList.add('hidden');
                analyzeBtn.disabled = false;
            };
            reader.readAsDataURL(file);
            // Sync the input file if it was dropped
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        }
    }

    // 4. API CALL TO FLASK
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // UI Transition
        document.getElementById('loader').classList.remove('hidden');
        document.getElementById('result-card').classList.add('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Display Results
            document.getElementById('res-label').innerText = data.prediction;
            document.getElementById('res-conf').innerText = data.confidence + "%";
            document.getElementById('result-card').classList.remove('hidden');

            // UPDATE LOCAL HISTORY
            updateLocalStorage(data);

        } catch (error) {
            console.error("Error:", error);
            alert("Analysis failed. Is the Flask server running?");
        } finally {
            document.getElementById('loader').classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });
});

function updateLocalStorage(data) {
    let history = JSON.parse(localStorage.getItem('leafHistory')) || [];
    const entry = {
        timestamp: new Date().toLocaleString(),
        crop: data.prediction.split('-')[0],
        condition: data.prediction,
        confidence: data.confidence + "%"
    };
    history.unshift(entry);
    localStorage.setItem('leafHistory', JSON.stringify(history.slice(0, 20))); // Keep last 20
}