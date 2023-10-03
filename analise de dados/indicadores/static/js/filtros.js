function filtrarTabela() {
  // console.log('primeiro teste da func filtrarTabela()');
    var input, filtro, tabela, linhas, celulas, i, j;
    input = document.getElementById("filtroTabela");
    filtro = input.value.toUpperCase();
    tabela = document.getElementById("aprendizes");
    linhas = tabela.getElementsByTagName("tr");
    
    for (i = 1; i < linhas.length; i++) {
      //console.log('Dentro do laço');
      celulas = linhas[i].getElementsByTagName("td");
      for (j = 0; j < celulas.length; j++) {
        if (celulas[j].innerHTML.toUpperCase().indexOf(filtro) > -1) {
          linhas[i].style.display = "";
          break;
        } else {
          linhas[i].style.display = "none";
        }
      }
    }
  }