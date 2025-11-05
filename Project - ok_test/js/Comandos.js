document.querySelectorAll('.card img').forEach(img => {
    img.addEventListener('click', (event) => {
        // Adiciona o comportamento de zoom
        const zoomedImg = document.createElement('div');
        zoomedImg.style.position = 'fixed';
        zoomedImg.style.top = '0';
        zoomedImg.style.left = '0';
        zoomedImg.style.width = '100%';
        zoomedImg.style.height = '100%';
        zoomedImg.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        zoomedImg.style.display = 'flex';
        zoomedImg.style.alignItems = 'center';
        zoomedImg.style.justifyContent = 'center';
        zoomedImg.style.zIndex = '1000';
        zoomedImg.innerHTML = `<img src="${img.src}" alt="${img.alt}" style="max-width: 90%; max-height: 90%; border-radius: 10px;">`;

        // Fecha o zoom ao clicar fora da imagem
        zoomedImg.addEventListener('click', () => {
            zoomedImg.remove();
        });

        document.body.appendChild(zoomedImg);

        // Impede o redirecionamento ao clicar na imagem ampliada
        event.stopPropagation();
    });

    img.addEventListener('dblclick', () => {
        const species = img.alt;
        const guideUrl = `../Html/${species.replace(/\s+/g, '-').toLowerCase()}.html`;
        window.location.href = guideUrl;
    });
});