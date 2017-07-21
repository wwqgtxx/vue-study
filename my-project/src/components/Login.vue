<template>
  <div>
    <div>
      <h1>用户登录</h1>
    </div>

    <warning-alert v-bind:message="warning_message"></warning-alert>

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
  import WarningAlert from './WarningAlert.vue'
  export default {
    name: 'login',
    data () {
      return {
        username: "",
        password: "",
        validate_code: "",
        validate_code_img: null,
        warning_message: [],
      }
    },
    mounted () {
      update_validate_code(this)
    },
    methods: {
      async do_login() {
        if (this.username === "") {
          this.warning_message.push("用户名不可为空，请填写用户名。")
          return;
        }
        if (this.password === "") {
          this.warning_message.push("密码不可为空，请输入密码。")
          return;
        }
        if (this.validate_code === "") {
          this.warning_message.push("验证码不可为空，请输入验证码。")
          return;
        }
        let data = {
          "username": this.username,
          "password": this.password,
          "validate_code": this.validate_code
        };
        let json = JSON.stringify(data)
        try {
          let response = await axios({
              method: "post",
              url: "/api/login/",
              headers: {
                'Content-Type': 'application/json;charset=UTF-8'
              },
              data: json
            }
          )
          console.log(response.data)
          if (response.data.status === "ok") {
            this.$store.commit("login", response.data)
            if (this.$route.query.redirect) {
              this.$router.push(this.$route.query.redirect)
            }
            else {
              this.$router.push("/")
            }
            return
          }
          else {
            let reason = response.data.reason
            this.warning_message.splice(0)
            switch (reason) {
              case "no_validate_code":
              {
                this.warning_message.push("验证码不可为空，请输入验证码。")
                break
              }
              case "error_validate_code":
              {
                this.warning_message.push("验证码输入错误，请重新输入验证码。")
                break
              }
              case "error_user":
              {
                this.warning_message.push("用户名或密码错误，请重新输入。")
                break
              }
              default:
              {
                this.warning_message.push("未知错误")
                break
              }
            }
          }
        } catch (err) {
          this.warning_message.splice(0)
          this.warning_message.push("未知错误")
          console.log(err)
        }
        update_validate_code(this)
      },
      update_validate_code_img(){
        update_validate_code(this)
      }
    },
    components: {
      "warning-alert": WarningAlert
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
</style>
