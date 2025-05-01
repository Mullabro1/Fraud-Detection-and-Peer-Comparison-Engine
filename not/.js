let clickCount = 0;
const maxClicks = 150;
const maxRequestsBeforeTimeout = 60;
const timeoutDuration = 30000; // 30,000ms = 30 seconds

function clickLoadMore() {
  const loadMoreButton = document.querySelector('#loadMoreNew a');

  if (loadMoreButton && clickCount < maxClicks) {
    loadMoreButton.click();
    clickCount++;
    console.log(`Clicked the 'Load more' button! Click count: ${clickCount}`);

    // If 60 requests have been made, wait for 30 seconds before continuing
    if (clickCount % maxRequestsBeforeTimeout === 0) {
      console.log("Reached 60 requests, waiting for 30 seconds...");
      setTimeout(clickLoadMore, timeoutDuration);
    } else {
      // Otherwise, just continue immediately (with a 3-second delay to ensure page loads)
      setTimeout(clickLoadMore, 3000);
    }
  } else {
    console.log(`Finished clicking or 'Load more' button not found. Total clicks: ${clickCount}`);
  }
}

// Start the loop
clickLoadMore();
/*const data = Array.from(document.querySelectorAll('.category-card.search-card.new-eco-card')).map(card => ({
  incubator: card.querySelector('h3')?.innerText.trim() || '',
  location: Array.from(card.querySelectorAll('.location span'))
    .map(s => s.innerText.trim())
    .filter(Boolean)
    .join(', '),
  incubee: card.querySelector('a.img-wrap')?.href || ''
}));

console.log(data);  // This will log the scraped data from the page
// Create and download a JSON file from the scraped data
const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'incubators.json';
a.click();
URL.revokeObjectURL(url);
 */