document.addEventListener('DOMContentLoaded', function() {
    var isCategoriaFilha = document.querySelector('#id_is_categoria_filha');
    var categoriaPai = document.querySelector('#id_categoria_pai').parentNode.parentNode;
    if (!isCategoriaFilha.checked) {
        categoriaPai.style.display = 'none';
    }
    isCategoriaFilha.addEventListener('change', function() {
        if (isCategoriaFilha.checked) {
            categoriaPai.style.display = '';
        } else {
            categoriaPai.style.display = 'none';
        }
    });
});