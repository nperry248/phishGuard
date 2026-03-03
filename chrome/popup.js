const resultEl = document.getElementById('result')
const urlEl = document.getElementById('urlDisplay')

chrome.runtime.sendMessage({ action: 'getPrediction' }, function(response) {
  if (!response) {
    showError('Could not connect to the extension.')
    return
  }

  // Show the URL being checked
  if (response.url) {
    urlEl.textContent = response.url
  }

  if (response.result === 'safe') {
    resultEl.className = 'result safe'
    resultEl.innerHTML = `
      <div class="result-icon">✓</div>
      <div>This site looks safe</div>
      <div class="sub">No phishing indicators detected</div>
    `
  } else if (response.result === 'unsafe') {
    resultEl.className = 'result unsafe'
    resultEl.innerHTML = `
      <div class="result-icon">⚠</div>
      <div>Potential phishing site</div>
      <div class="sub">Proceed with caution</div>
    `
  } else {
    showError('Could not analyze this URL.')
  }
})

function showError(msg) {
  urlEl.textContent = '—'
  resultEl.className = 'result error'
  resultEl.innerHTML = `<div>${msg}</div>`
}
