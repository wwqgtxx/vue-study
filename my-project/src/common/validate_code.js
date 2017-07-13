import axios from 'axios'

let update_validate_code = async function (vue) {
  try{
    let response = await axios({
        method: "post",
        url: "/api/validate_code/"
      }
    )
    console.log(response.data)
    vue.validate_code_img = "data:image/jpeg;base64," + response.data.encode_img
  }
  catch (err){
    console.log(err)
  }
}

export {update_validate_code}
