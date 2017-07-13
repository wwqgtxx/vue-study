<template>
  <div>
    <div>
      <h1>用户登录</h1>
    </div>

    <div id="alert_area"></div>

    <div>
      <form class="form-inline">
        <div class="form-group">
          <label>用户名</label>
          <input type="text" class="form-control" name="username" value=""
                 v-model="username"
                 placeholder="用户名">
        </div>
        <div class="form-group">
          <label>密码</label>
          <input type="password" class="form-control" name="password" value=""
                 v-model="password"
                 placeholder="密码">
        </div>
        <div class="form-group">
          <label>验证码</label>
          <img id="img_validate_code" :src="validate_code_img"
               style="cursor: pointer;"
               v-on:click.prevent="update_validate_code_img"
          >
          <input type="text" class="form-control" name="validate_code" value=""
                 v-model="validate_code"
                 placeholder="验证码">
        </div>
        <button type="submit" class="btn btn-default btn-lg" v-on:click.prevent="do_login">登录</button>
        <router-link tag="button" class="btn btn-info btn-lg" to="/register">注册新用户</router-link>
        <input type="hidden" name="_csrf_token" value=""/>
      </form>

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {update_validate_code} from '../common/validate_code'
  export default {
    name: 'login',
    data () {
      return {
        username: "",
        password: "",
        validate_code: "",
        validate_code_img: null,
      }
    },
    mounted () {
      update_validate_code(this)
    },
    methods: {
      do_login() {
        let data = {
          "username": this.username,
          "password": this.password,
          "validate_code": this.validate_code
        };
        let json = JSON.stringify(data)
        axios({
            method: "post",
            url: "/api/login/",
            headers: {
              'Content-Type': 'application/json;charset=UTF-8'
            },
            data: json
          }
        ).then(function (response) {
          console.log(response.data)
          if(response.data.status === "ok"){
              this.$store.commit("login",response.data)
              this.$router.push("/")
          }else{
            update_validate_code(this)
          }
        }.bind(this)).catch(function (err) {
          console.log(err)
          update_validate_code(this)
        });
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
