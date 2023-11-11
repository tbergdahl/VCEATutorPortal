document.querySelector('#closeSidebarBtn').addEventListener('click', function() {
    var sidebar = document.querySelector('#sidebar');
    var closeBtn = document.querySelector('#closeSidebarBtn');
    var openBtn = document.querySelector('#openSidebarBtn');
    var wrapper = document.querySelector(".wrapper");

    // Toggle the collapsed class on wrapper
    wrapper.classList.toggle("collapsed");

    // Toggle the closed class on sidebar
    sidebar.classList.toggle('closed');

    if (sidebar.classList.contains('closed')) {
        sidebar.style.width = '50px';  // Closed width
        closeBtn.style.display = 'none';  // Hide close button
        openBtn.style.display = 'block';  // Show menu button
    } else {
        sidebar.style.width = '250px';  // Opened width
        closeBtn.style.display = 'block';  // Show close button
        openBtn.style.display = 'none';  // Hide menu button
    }
});

// Event listener to open the sidebar when the menu button is clicked
document.querySelector('#openSidebarBtn').addEventListener('click', function() {
    var sidebar = document.querySelector('#sidebar');
    var closeBtn = document.querySelector('#closeSidebarBtn');
    var openBtn = document.querySelector('#openSidebarBtn');
    var wrapper = document.querySelector(".wrapper");

    wrapper.classList.remove("collapsed");
    sidebar.classList.remove('closed');
    sidebar.style.width = '250px';  // Opened width
    closeBtn.style.display = 'block';  // Show close button
    openBtn.style.display = 'none';  // Hide menu button
});

function fetchPDFPreview(reportType) {
    var pdfPreview = document.getElementById('pdf-preview');
    pdfPreview.src = 'data:image/jpeg;base64,YOUR_BASE64_ENCODED_IMAGE';
    pdfPreview.style.display = 'block';
}


// Ensure this ID matches the ID of your report selection dropdown in the HTML
document.addEventListener('DOMContentLoaded', function() {
    var reportSelectField = document.getElementById('id_of_your_report_select_field');
    if (reportSelectField) {
        reportSelectField.addEventListener('change', function() {
            fetchPDFPreview(this.value);
        });
    }
});