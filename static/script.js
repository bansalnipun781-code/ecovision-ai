document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadSection = document.getElementById('uploadSection');
    const resultSection = document.getElementById('resultSection');
    const imagePreview = document.getElementById('imagePreview');
    const resetBtn = document.getElementById('resetBtn');

    const loadingState = document.getElementById('loadingState');
    const resultContent = document.getElementById('resultContent');
    const recommendationCard = document.getElementById('recommendationCard');

    const classificationBadge = document.getElementById('classificationBadge');
    const classificationText = document.getElementById('classificationText');
    const materialType = document.getElementById('materialType');
    const confidenceValue = document.getElementById('confidenceValue');
    const confidenceFill = document.getElementById('confidenceFill');
    const recommendationList = document.getElementById('recommendationList');

    // Mock Data for AI Predictions
    const mockPredictions = [
        {
            type: "Plastic Bottle (PET)",
            recyclable: true,
            confidence: 98,
            steps: [
                "Empty all liquids before recycling.",
                "Crush the bottle to save space.",
                "Leave the cap on, it's recyclable too!",
                "Place in the blue mixed-recycling bin."
            ],
            fact: "Recycling a single plastic bottle can conserve enough energy to light a 60W light bulb for up to 6 hours."
        },
        {
            type: "Cardboard Box",
            recyclable: true,
            confidence: 95,
            steps: [
                "Remove any plastic tape or labels if possible.",
                "Flatten the box completely.",
                "Keep it dry; wet cardboard is often unrecyclable.",
                "Place in the paper/cardboard recycling bin."
            ],
            fact: "Recycling 1 ton of cardboard saves 46 gallons of oil and 9 cubic yards of landfill space."
        },
        {
            type: "Styrofoam Container",
            recyclable: false,
            confidence: 92,
            steps: [
                "Cannot be recycled in standard curbside bins.",
                "Place in the general waste/trash bin.",
                "Alternatively, check for local specialized drop-off facilities."
            ],
            fact: "Styrofoam takes over 500 years to decompose in a landfill. Consider using reusable containers next time!"
        },
        {
            type: "Aluminum Can",
            recyclable: true,
            confidence: 99,
            steps: [
                "Rinse out any remaining liquid.",
                "Do not crush (unless local guidelines specify otherwise).",
                "Place in the metal/mixed recycling bin."
            ],
            fact: "Aluminum can be recycled infinitely without loss of quality. Recycling one can saves enough energy to run a TV for 3 hours."
        }
    ];

    // Event Listeners for Drag & Drop
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, () => {
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        fileInput.value = '';

        // Reset UI states
        loadingState.classList.remove('hidden');
        resultContent.classList.add('hidden');
        recommendationCard.classList.add('hidden');
        confidenceFill.style.width = '0%';
    });

    // File Handling and UI Update
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            showAnalysis();
        };
        reader.readAsDataURL(file);
    }

    function showAnalysis() {
        uploadSection.classList.add('hidden');
        resultSection.classList.remove('hidden');

        // Simulate AI Processing time
        setTimeout(() => {
            displayResults();
        }, 2000);
    }

    function displayResults() {
        // Pick a random mock prediction
        const prediction = mockPredictions[Math.floor(Math.random() * mockPredictions.length)];

        // Hide loading, show results
        loadingState.classList.add('hidden');
        resultContent.classList.remove('hidden');
        recommendationCard.classList.remove('hidden');

        // Populate Data
        materialType.textContent = prediction.type;
        confidenceValue.textContent = `${prediction.confidence}%`;

        // Setup Badge
        if (prediction.recyclable) {
            classificationBadge.className = 'classification-badge recyclable';
            classificationBadge.innerHTML = '<i class="fa-solid fa-recycle"></i><span id="classificationText">Recyclable</span>';
        } else {
            classificationBadge.className = 'classification-badge non-recyclable';
            classificationBadge.innerHTML = '<i class="fa-solid fa-trash-can"></i><span id="classificationText">Non-Recyclable</span>';
        }

        // Animate Confidence Meter
        setTimeout(() => {
            confidenceFill.style.width = `${prediction.confidence}%`;
            // Change color based on recyclable status
            if (!prediction.recyclable) {
                confidenceFill.style.background = 'linear-gradient(90deg, #f59e0b, #ef4444)';
            } else {
                confidenceFill.style.background = 'linear-gradient(90deg, var(--accent-color), var(--primary-green))';
            }
        }, 100);

        // Populate Recommendations
        recommendationList.innerHTML = '';
        prediction.steps.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            recommendationList.appendChild(li);
        });

        // Update Eco Fact
        const ecoFactElement = recommendationCard.querySelector('.eco-fact');
        ecoFactElement.innerHTML = `<strong><i class="fa-solid fa-earth-americas"></i> Eco Impact:</strong> ${prediction.fact}`;
    }
});
