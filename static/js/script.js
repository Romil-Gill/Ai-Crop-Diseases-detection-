document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const preview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const prompt = document.getElementById('drop-zone-prompt');
    const historyBody = document.getElementById('historyBody');
    const contactForm = document.getElementById('contactForm');

    // --- DETECTION LOGIC ---
    if (dropZone) {
        dropZone.onclick = () => fileInput.click();
        fileInput.onchange = (e) => handleFile(e.target.files[0]);

        function handleFile(file) {
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                    prompt.classList.add('hidden');
                    analyzeBtn.disabled = false;
                };
                reader.readAsDataURL(file);
            }
        }

        analyzeBtn.onclick = async () => {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            document.getElementById('loader').classList.remove('hidden');
            analyzeBtn.disabled = true;

            try {
                const response = await fetch('/predict', { method: 'POST', body: formData });
                const data = await response.json();
                
                document.getElementById('res-label').innerText = data.prediction;
                document.getElementById('res-conf').innerText = data.confidence + "%";
                document.getElementById('result-card').classList.remove('hidden');

                saveToHistory(data);
            } catch (err) { alert("Server error"); }
            finally { document.getElementById('loader').classList.add('hidden'); }
        };
    }

    // --- HISTORY LOGIC ---
    function saveToHistory(data) {
        let history = JSON.parse(localStorage.getItem('leafHistory')) || [];
        history.unshift({
            date: new Date().toLocaleString(),
            crop: data.prediction.split('-')[0],
            diagnosis: data.prediction,
            confidence: data.confidence + "%",
            isHealthy: data.prediction.toLowerCase().includes('healthy')
        });
        localStorage.setItem('leafHistory', JSON.stringify(history.slice(0, 10)));
    }

    if (historyBody) {
        const history = JSON.parse(localStorage.getItem('leafHistory')) || [];
        if (history.length === 0) document.getElementById('noHistoryMsg').classList.remove('hidden');
        
        historyBody.innerHTML = history.map(item => `
            <tr>
                <td>${item.date}</td>
                <td><span class="badge-crop">${item.crop}</span></td>
                <td>
                    <span class="status-badge ${item.isHealthy ? 'status-healthy' : 'status-disease'}">
                        ${item.diagnosis}
                    </span>
                </td>
                <td>
                    <div class="conf-bar-bg"><div class="conf-bar-fill" style="width: ${item.confidence}"></div></div>
                    ${item.confidence}
                </td>
            </tr>
        `).join('');
    }

    // Clear History
    const clearBtn = document.getElementById('clearHistoryBtn');
    if (clearBtn) {
        clearBtn.onclick = () => {
            localStorage.removeItem('leafHistory');
            location.reload();
        };
    }
});