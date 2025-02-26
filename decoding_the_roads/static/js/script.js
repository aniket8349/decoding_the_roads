document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const analysisButtons = document.querySelectorAll('#analysis-button');
    const graphContainers = document.querySelectorAll('.graph-container');
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


    // Toggle sidebar on smaller screens
    if (window.innerWidth <= 768) {
        const sidebarToggle = document.createElement('button');
        sidebarToggle.textContent = 'Menu';
        sidebarToggle.classList.add('sidebar-toggle'); // Add a class for styling
        document.body.insertBefore(sidebarToggle, document.body.firstChild); // Insert at the beginning of the body

        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            sidebarToggle.classList.toggle('active'); // Toggle active state of the button
        });

        // Add close button to the sidebar itself
        const sidebarClose = document.createElement('button');
        sidebarClose.textContent = 'Close';
        sidebarClose.classList.add('sidebar-close');
        sidebar.insertBefore(sidebarClose, sidebar.firstChild);

        sidebarClose.addEventListener('click', () => {
            sidebar.classList.add('collapsed');
            sidebarToggle.classList.remove('active'); // Hide the toggle button
        });

    }


});