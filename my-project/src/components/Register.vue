<template>
  <div>
    <div class="col-md-2"></div>
    <div class="col-md-8">
      <div class="text-center">
        <h1>用户注册</h1>
      </div>

      <div id="alert_area"></div>

      <div>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="col-md-2 control-label">用户名</label>
            <div class="col-md-10">
              <input type="text" class="form-control" name="username" value=""
                     v-model="username"
                     placeholder="用户名">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-2 control-label">密码</label>
            <div class="col-md-10">
              <input type="password" class="form-control" name="password" value=""
                     v-model="password"
                     placeholder="密码">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-2 control-label">确认密码</label>
            <div class="col-md-10">
              <input type="password" class="form-control" name="confirm_password" value=""
                     v-model="confirm_password"
                     placeholder="确认密码">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-2 control-label">验证码</label>
            <div class="col-md-2">
              <img id="img_validate_code" :src="validate_code_img"
                   style="cursor: pointer;" v-on:click.prevent="update_validate_code_img">
            </div>
            <div class="col-md-8">
              <input type="text" class="form-control" name="validate_code" value=""
                     v-model="validate_code"
                     placeholder="验证码">
            </div>
          </div>
          <div class="form-group">
            <div class="col-md-2"></div>
            <div class="col-md-4 text-left">
              <button type="button" class="btn btn-lg btn-danger btn-block" v-on:click.prevent="do_cls">清空</button>
            </div>
            <div class="col-md-2"></div>
            <div class="col-md-4 text-right">
              <button type="submit" class="btn btn-lg btn-primary btn-block" v-on:click.prevent="do_register">注册
              </button>
            </div>
          </div>
          <input type="hidden" name="_csrf_token" value=""/>
        </form>

      </div>
    </div>
    <div class="col-md-2"></div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {update_validate_code} from '../common/validate_code'
  export default {
    name: 'register',
    data () {
      return {
        username: "",
        password: "",
        confirm_password: "",
        validate_code: "",
        validate_code_img: null,
      }
    },
    mounted () {
      update_validate_code(this)
    },
    methods: {
      do_register() {
        let data = {
          "username": this.username,
          "password": this.password,
          "validate_code": this.validate_code
        };
        let json = JSON.stringify(data)
        axios({
            method: "post",
            url: "/api/register/",
            headers: {
              'Content-Type': 'application/json;charset=UTF-8'
            },
            data: json
          }
        ).then(function (response) {
          console.log(response.data)
          if(response.data.status === "ok"){
            this.$router.push("/login")
          }else{
            update_validate_code(this)
          }
        }.bind(this)).catch(function (err) {
          console.log(err)
          update_validate_code(this)
        });
      },
      do_cls(){
        this.username = ""
        this.password = ""
        this.confirm_password = ""
        this.validate_code = ""
      },
      update_validate_code_img(){
        update_validate_code(this)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
</style>
