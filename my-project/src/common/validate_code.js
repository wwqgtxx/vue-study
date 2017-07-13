import axios from 'axios'

let update_validate_code = function (vue) {
  axios({
      method: "post",
      url: "/api/validate_code/"
    }
  ).then(function (response) {
    console.log(response.data)
    vue.validate_code_img = "data:image/jpeg;base64," + response.data.encode_img
  }.bind(this)).catch(function (err) {
    console.log(err)
  })
}

export {update_validate_code}
