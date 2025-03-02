document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const resultsContent = document.getElementById('results-content');

    // Preview images
    function previewImage(input, previewId) {
        const preview = document.getElementById(previewId);
        const file = input.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            }
            reader.readAsDataURL(file);
        }
    }

    // Set up image preview listeners
    document.getElementById('before-image').addEventListener('change', function() {
        previewImage(this, 'before-preview');
    });

    document.getElementById('after-image').addEventListener('change', function() {
        previewImage(this, 'after-preview');
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        
        const formData = new FormData(form);
        
        try {
            console.log('Sending request...');
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            console.log('Response received:', response);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Data received:', data);
            
            // Format and display results
            let htmlContent = '<div class="analysis-summary">';
            htmlContent += `<p>Total blocks analyzed: ${data.total_blocks}</p>`;
            
            data.results.forEach((result, index) => {
                htmlContent += `
                    <div class="block-result">
                        <h3>Block ${index + 1}</h3>
                        <p><strong>Position:</strong> x: ${result.position[0]}, y: ${result.position[1]}</p>
                        <p><strong>Analysis:</strong></p>
                        <pre>${result.analysis}</pre>
                    </div>
                `;
            });
            
            htmlContent += '</div>';
            resultsContent.innerHTML = htmlContent;
            results.classList.remove('hidden');
            
        } catch (error) {
            console.error('Error:', error);
            resultsContent.innerHTML = `
                <div class="error-message">
                    Error: ${error.message}
                    <br>
                    Please try again or contact support if the problem persists.
                </div>
            `;
            results.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    });
}); 