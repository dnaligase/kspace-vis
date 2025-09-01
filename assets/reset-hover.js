document.addEventListener('DOMContentLoaded', function () {
    const graph = document.getElementById('heatmap');
    if (graph) {
        graph.on('plotly_unhover', function () {
            const event = new CustomEvent('resetHover', { detail: {} });
            window.dispatchEvent(event);
        });
    }
});
