let createDisconnectAlert = function () {
  return $.alert({
    title: '错误',
    content: '连接服务器出错',
    type: 'red',
    buttons: {
      yes: {
        btnClass: 'hide' // hide is a bootstrap class to hide elements
      }
    }
  })
}
let createMessageDialog = function (title, content) {
  return $.dialog({
    title: title,
    content: content,
    backgroundDismiss: true,
    animationSpeed: 500
  })
}

export {createDisconnectAlert, createMessageDialog}
