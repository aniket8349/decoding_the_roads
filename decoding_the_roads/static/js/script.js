document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const analysisButtons = document.querySelectorAll('#sidebar-btn');
    const graphContainers = document.querySelectorAll('#graph-container');
    let activeGraph = document.querySelector('.graph-container.active'); // Store the initially active graph

    analysisButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.dataset.target;

            // Hide all graph containers
            graphContainers.forEach(container => {
                container.classList.remove('active');
            });

            // Show the selected graph container
            const targetContainer = document.getElementById(target);
            if (targetContainer) {
                targetContainer.classList.add('active');
                activeGraph = targetContainer; // Update the active graph
            }

            // Close the sidebar on smaller screens after a button is clicked
            if (window.innerWidth <= 768) {
                sidebar.classList.add('collapsed');
                sidebarToggle.classList.remove('active'); // Hide the toggle button
            }
        });
    });

});