document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/alumni")
        .then(response => response.json())
        .then(data => {
            const alumniList = document.getElementById("alumni-list");
            alumniList.innerHTML = "<ul>" + data.map(alumnus => `
                <li>
                    ${alumnus.first_name} ${alumnus.last_name} - ${alumnus.position} at ${alumnus.company} (${alumnus.graduation_year})
                </li>
            `).join("") + "</ul>";
        });
});
