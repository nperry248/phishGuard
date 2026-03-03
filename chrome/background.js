// Update this after deploying to Render
const API_URL = 'https://phishguard-yn8k.onrender.com'

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'getPrediction') {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const url = tabs[0].url
      const endpoint = `${API_URL}/?url=${encodeURIComponent(url)}`

      fetch(endpoint)
        .then(res => {
          if (!res.ok) {
            console.error('API error:', res.status, res.statusText)
            return res.text().then(t => { throw new Error(`HTTP ${res.status}: ${t.slice(0, 200)}`) })
          }
          return res.json()
        })
        .then(data => {
          const result = data.prediction ? 'unsafe' : 'safe'
          sendResponse({ result, url })
        })
        .catch(err => {
          console.error('PhishGuard fetch error:', err)
          sendResponse({ result: 'error', url })
        })
    })

    return true // keeps the message channel open for async response
  }
})
