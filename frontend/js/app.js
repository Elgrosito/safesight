const frameElement = document.getElementById('frame');
const ws = new WebSocket('ws://localhost:8200/v1/detect/ws');

ws.onopen = function(event) {
  console.log('WebSocket connection established');
    // Mapeo de paths a canales
    const channelMapping = {
      '/frontend/video-page-2.html': 1,
      '/frontend/video-page-3.html': 2
    };

    const URLactual = window.location;

    // Busca el canal en el mapeo, default a 0 si no se encuentra
    const channel = channelMapping[URLactual.pathname] || 0;
    ws.send(channel);
};

ws.onerror = function(event) {
  console.error('WebSocket error:', event);
};

ws.onclose = function(event) {
  console.log('WebSocket connection closed');
};

ws.onmessage = function(event) {
  // if (!listening) return;
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

function initProcess() {
  listening = true;
}

function stopProcess() {
  listening = false;
  frameElement.src = 'https://imgsvr.radiocut.site/get/thumb/900/900/cuts_logos/80/2f/802fb220-63ef-42d5-b105-1b225223c1ee.jpg';
}
