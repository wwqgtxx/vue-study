import store from '../store'

let socketio_check_csrftoken = function (socket) {
  socket.emit("check_csrf_token", store.state._csrf_token, function (message) {
    if (message === true) {
      console.info("socket.io successful check csrf token!")
    }
    else {
      console.info("socket.io check csrf token failed!");
    }
  });
}

export {socketio_check_csrftoken}

