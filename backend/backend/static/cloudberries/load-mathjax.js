window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
    },
    svg: {
        fontCache: 'global'
    },
    startup: {
        ready: () => {
        MathJax.startup.defaultReady();
        MathJax.startup.promise.then(() => {
            console.log('MathJax initial typesetting complete');
        });
        }
    }
};

(function () {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
    script.async = true;
    document.head.appendChild(script);
})();