const frameElement = document.getElementById('frame');
const ws = new WebSocket('ws://localhost:8200/v1/detect/ws');

ws.onopen = function(event) {
  console.log('WebSocket connection established');
};

ws.onmessage = function(event) {
  const frameData = event.data;

  // Convert base64 string back to binary
  const byteString = atob(frameData);
  const byteNumbers = new Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    byteNumbers[i] = byteString.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);

  // Create a Blob object from the binary data
  const frameBlob = new Blob([byteArray], { type: 'image/jpeg' });

  // Get the URL of the Blob object
  const frameUrl = URL.createObjectURL(frameBlob);

  // Set the src property of the image element to the Blob object.
  frameElement.src = frameUrl;
};

ws.onclose = function(event) {
  console.log('WebSocket connection closed');
};

ws.onerror = function(event) {
  console.error('WebSocket error:', event);
};
