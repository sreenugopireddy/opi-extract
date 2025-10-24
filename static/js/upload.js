document.getElementById("uploadBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!fileInput.files.length) {
    status.textContent = "Please select a file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  status.textContent = "Uploading...";

  try {
    const res = await fetch("/upload-document", {
      method: "POST",
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      status.textContent = "Error: " + (err.detail || res.statusText);
      return;
    }
    const data = await res.json();
    status.textContent = `Uploaded: ${data.original_filename} (${data.file_size_bytes} bytes)`;
  } catch (e) {
    status.textContent = "Upload failed: " + e;
  }
});
