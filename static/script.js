document.getElementById("generate").addEventListener("click", async () => {
    const prompt = document.getElementById("prompt").value;
    // Updated selector to use the class on the new HTML structure
    const resultDiv = document.getElementById("result");

    // Simple validation
    if (prompt.trim() === "") {
        resultDiv.innerHTML = "<p style='color: red;'>Please enter a testing idea or scenario.</p>";
        return;
    }

    resultDiv.innerHTML = "⏳ Generating, please wait...";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            // Use application/json for modern APIs, or keep x-www-form-urlencoded if your Flask/Backend expects it
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ prompt })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();

        // Check if the expected result field exists
        if (data.result) {
            resultDiv.innerText = data.result;
        } else {
            resultDiv.innerHTML = "<p style='color: orange;'>Generation complete, but received an unexpected response format.</p>";
        }

    } catch (error) {
        console.error("Fetch error:", error);
        resultDiv.innerHTML = `<p style='color: red;'>❌ Error generating ideas: ${error.message}. Please check the backend service.</p>`;
    }
});