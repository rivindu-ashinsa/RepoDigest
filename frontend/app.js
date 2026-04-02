const API_BASE = "http://127.0.0.1:8000";

const form = document.getElementById("generate-form");
const repoUrlInput = document.getElementById("repo-url");
const useHfInput = document.getElementById("use-hf");
const generateBtn = document.getElementById("generate-btn");
const clearLogsBtn = document.getElementById("clear-logs-btn");
const copyMdBtn = document.getElementById("copy-md-btn");
const logsEl = document.getElementById("logs");
const markdownOutputEl = document.getElementById("markdown-output");
const progressBarEl = document.getElementById("progress-bar");
const progressTextEl = document.getElementById("progress-text");
const liveStatusEl = document.getElementById("live-status");

let latestMarkdown = "";

function nowTime() {
  return new Date().toLocaleTimeString();
}

function addLog(message, kind = "info") {
  const line = document.createElement("div");
  line.className = `log-entry ${kind}`;
  line.textContent = `[${nowTime()}] ${message}`;
  logsEl.appendChild(line);
  logsEl.scrollTop = logsEl.scrollHeight;
}

function setStatus(text) {
  liveStatusEl.textContent = text;
}

function setProgress(current, total) {
  const safeTotal = Math.max(0, Number(total) || 0);
  const safeCurrent = Math.max(0, Number(current) || 0);
  const pct = safeTotal > 0 ? Math.min(100, (safeCurrent / safeTotal) * 100) : 0;
  progressBarEl.style.width = `${pct}%`;
  progressTextEl.textContent = `${safeCurrent} / ${safeTotal} files`;
}

function renderMarkdown(markdownText) {
  const rawHtml = marked.parse(markdownText || "");
  const cleanHtml = DOMPurify.sanitize(rawHtml);
  markdownOutputEl.innerHTML = cleanHtml;
}

async function generateReadmeStream(payload) {
  const response = await fetch(`${API_BASE}/api/generate-readme-stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // Keep fallback message
    }
    throw new Error(message);
  }

  if (!response.body) {
    throw new Error("Streaming response body is empty.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffered = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }

    buffered += decoder.decode(value, { stream: true });
    const lines = buffered.split("\n");
    buffered = lines.pop() || "";

    for (const line of lines) {
      if (!line.trim()) {
        continue;
      }

      const event = JSON.parse(line);
      const type = event.type || "status";

      if (type === "status") {
        setStatus("Running");
        addLog(event.message || "Status update");
      } else if (type === "scan") {
        setProgress(event.current, event.total);
        addLog(event.message || `Scanning ${event.file}`);
      } else if (type === "progress") {
        setProgress(event.current, event.total);
        addLog(event.message || `Processed ${event.file}`);
      } else if (type === "result") {
        latestMarkdown = event.readme_content || "";
        renderMarkdown(latestMarkdown);
        copyMdBtn.disabled = latestMarkdown.length === 0;
        addLog(`README generated from ${event.file_count} files.`);
      } else if (type === "done") {
        setStatus("Completed");
        addLog(event.message || "Done");
      } else if (type === "error") {
        setStatus("Failed");
        addLog(event.message || "Unknown error", "error");
        throw new Error(event.message || "Generation failed.");
      }
    }
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const repoUrl = repoUrlInput.value.trim();
  if (!repoUrl) {
    addLog("Repository URL is required.", "error");
    return;
  }

  generateBtn.disabled = true;
  copyMdBtn.disabled = true;
  latestMarkdown = "";
  markdownOutputEl.innerHTML = "";
  setProgress(0, 0);
  setStatus("Starting");
  addLog(`Starting generation for: ${repoUrl}`);

  try {
    await generateReadmeStream({
      repo_url: repoUrl,
      use_hf_model: useHfInput.checked,
    });
  } catch (error) {
    setStatus("Failed");
    addLog(error.message || "Unexpected error", "error");
  } finally {
    generateBtn.disabled = false;
  }
});

clearLogsBtn.addEventListener("click", () => {
  logsEl.innerHTML = "";
  addLog("Logs cleared.");
});

copyMdBtn.addEventListener("click", async () => {
  if (!latestMarkdown) {
    return;
  }
  try {
    await navigator.clipboard.writeText(latestMarkdown);
    addLog("Raw README markdown copied to clipboard.");
  } catch {
    addLog("Failed to copy markdown to clipboard.", "error");
  }
});

addLog("UI ready. Enter a repository URL and click Generate README.");
