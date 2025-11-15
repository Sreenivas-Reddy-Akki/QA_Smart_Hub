document.addEventListener("DOMContentLoaded", () => {
    const generateButton = document.getElementById("generate");
    const promptInput = document.getElementById("prompt");
    const resultDiv = document.getElementById("result");

    // Helper function to update the result div with specific states
    const updateResult = (message, state = 'default') => {
        // Reset classes before setting new ones
        resultDiv.className = 'result-box';

        if (state === 'loading') {
            resultDiv.classList.add('loading');
            resultDiv.innerHTML = "⏳ Generating, please wait...";
        } else if (state === 'error') {
            resultDiv.classList.add('error');
            // Use innerText for safety when displaying error messages from the catch block
            resultDiv.innerText = `❌ Error: ${message}`;
        } else if (state === 'warning') {
            resultDiv.classList.add('warning');
            resultDiv.innerText = `⚠️ Warning: ${message}`;
        } else {
            // Success state - assumes message is the generated result
            resultDiv.innerText = message;
        }
    };


    generateButton.addEventListener("click", async () => {
        const prompt = promptInput.value.trim();

        // 1. Simple validation
        if (prompt === "") {
            updateResult("Please enter a testing idea or scenario.", 'warning');
            return;
        }

        updateResult(null, 'loading');

        try {
            // Using modern JSON headers and JSON body is generally cleaner and better for Flask/FastAPI
            const response = await fetch("/generate", {
                method: "POST",
                // Change to application/json and use JSON.stringify
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt }) // Send prompt as JSON object
            });

            if (!response.ok) {
                // Check if the server provided an error message in the body
                const errorData = await response.json().catch(() => ({ message: `HTTP Error ${response.status}` }));
                throw new Error(errorData.message || `Server responded with status: ${response.statusText}`);
            }

            const data = await response.json();

            // 2. Check for the expected result field
            if (data.result) {
                // Use the successful result, preserving formatting (like newlines)
                updateResult(data.result, 'success');
            } else {
                updateResult("Generation complete, but received an unexpected response format.", 'warning');
            }

        } catch (error) {
            console.error("Fetch error:", error);
            // 3. Display specific error message from the thrown error
            updateResult(error.message || "An unknown error occurred.", 'error');
        }
    });
});