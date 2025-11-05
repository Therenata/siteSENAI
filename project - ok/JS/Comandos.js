document.querySelectorAll('.card img').forEach(img => {
    img.addEventListener('click', () => {
        const species = img.alt;
        const guideUrl = `../Html/${species.replace(/\s+/g, '-').toLowerCase()}.html`;
        window.location.href = guideUrl;
    });
});