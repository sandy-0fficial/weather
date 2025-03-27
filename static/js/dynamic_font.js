// Function to detect brightness of background and change font color
function adjustFontColor() {
    const body = document.body;
    const bgColor = window.getComputedStyle(body).backgroundColor;
    
    // Convert background color to RGB
    const rgb = bgColor.match(/\d+/g);
    
    if (rgb) {
        const r = parseInt(rgb[0]);
        const g = parseInt(rgb[1]);
        const b = parseInt(rgb[2]);

        // Calculate the brightness of the color
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;

        // If brightness is low, add dark class; otherwise add light class
        if (brightness < 125) {
            body.classList.add('dark');
            body.classList.remove('light');
        } else {
            body.classList.add('light');
            body.classList.remove('dark');
        }
    }
}

// Call the function when the page loads
window.onload = adjustFontColor;
