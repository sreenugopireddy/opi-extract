async function loadFiles() {
  const tbody = document.querySelector("#filesTable tbody");
  tbody.innerHTML = "<tr><td colspan='5'>Loading...</td></tr>";

  try {
    const res = await fetch("/files");
    if (!res.ok) {
      tbody.innerHTML = `<tr><td colspan='5'>Error: ${res.statusText}</td></tr>`;
      return;
    }
    const data = await res.json();
    if (!data.length) {
      tbody.innerHTML = "<tr><td colspan='5'>No files uploaded yet.</td></tr>";
      return;
    }
    tbody.innerHTML = "";
    for (const r of data) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.id}</td>
        <td>${r.original_filename}</td>
        <td>${r.system_filename}</td>
        <td>${r.file_size_bytes}</td>
        <td>${new Date(r.uploaded_at).toLocaleString()}</td>
      `;
      tbody.appendChild(tr);
    }
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan='5'>Failed to load: ${e}</td></tr>`;
  }
}

window.addEventListener("DOMContentLoaded", loadFiles);
