const btnsExcluir = document.querySelectorAll("#excluindo");

const notificacaoSwal = (titleText, text, icon) => {
    Swal.fire({
      titleText: titleText,
      text: text,
      icon: icon,
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sim, exclua este registro!'
    }).then((result) => {
      if(result.isConfirmed){
        Swal.fire(
            'Excluido!',
            'Este registro foi excluído.',
            'success',
            window.location.href = "/listar-solicitacao/",


        )
      }
    })
}


// Update do status da solicitaçao
//const getLocalStorage = () => localSorage.getItem('dbvettore') ?? []
//const setLocalStorage = () => localSorage.setItem('dbvettoe', dbStatus)
//
//const updatedbStatus = (, status) => {
//    const dbvettoe = getLocalStorage()
//    dbvettoe[] = status
//    setLocalStorage(dbvettoe)
//}




