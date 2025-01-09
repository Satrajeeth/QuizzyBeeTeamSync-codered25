document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please select a file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Upload file
    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (response.ok) {
            alert("File uploaded successfully!");
            document.getElementById("mcqSection").style.display = "block";
            window.filePath = result.file_path; // Save the uploaded file path
        } else {
            alert(result.error || "Failed to upload file");
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});

document.getElementById("generateMcqsBtn").addEventListener("click", async () => {
    const numQuestions = document.getElementById("numQuestions").value;

    // Generate MCQs
    try {
        const response = await fetch("/generate_mcqs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                file_path: window.filePath,
                num_questions: parseInt(numQuestions),
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("MCQs generated successfully!");
            document.getElementById("results").style.display = "block";
            document.getElementById("downloadText").href = "/" + result.text_file;
            document.getElementById("downloadPdf").href = "/" + result.pdf_file;
        } else {
            alert(result.error || "Failed to generate MCQs");
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});
