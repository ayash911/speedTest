
async function startTest() {
    const resultsDiv = document.getElementById("results");
    const startButton = document.getElementById("startButton");

    startButton.disabled = true;
    resultsDiv.innerHTML = `<div class="spinner"></div><p>Testing... Please wait.</p>`;
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    try {
      const response = await fetch("/start-test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ timezone }),
      });
      const data = await response.json();

      if (data.error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
      } else {
        resultsDiv.innerHTML = `
          <h2>Test Results</h2>
          <p><strong>Download Speed:</strong> ${data.download_speed} Mbps</p>
          <p><strong>Upload Speed:</strong> ${data.upload_speed} Mbps</p>
          <p><strong>Ping:</strong> ${data.ping} ms</p>
          <p><strong>Server Name:</strong> ${data.server_name}</p>
          <p><strong>Server Location:</strong> ${data.server_country}</p>
          <p><strong>Server Host:</strong> ${data.server_host}</p>
          <p><strong>Timestamp:</strong> ${data.timestamp}</p>
          <p><strong>Client IP:</strong> ${data.client_ip}</p>
          <p><strong>ISP:</strong> ${data.isp}</p>
        `;
      }
    } catch (error) {
      resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    } finally {
      startButton.disabled = false;
    }
  }
