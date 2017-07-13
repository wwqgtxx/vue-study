<template>
  <div>
    <div class="col-md-2"></div>
    <div class="col-md-8">
      <div class="text-center">
        <h1>用户设置</h1>
      </div>

      <div id="alert_area"></div>

      <div>
        <div class="text-left">
          <h2>修改用户名</h2>
        </div>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="col-md-2 control-label">用户名</label>
            <div class="col-md-8">
              <input type="text" class="form-control" name="username" value=""
                     v-model="username"
                     placeholder="用户名">
            </div>
            <div class="col-md-2">
              <button type="submit" class="btn btn-lg btn-primary btn-block" v-on:click.prevent="do_submit1">>确定
              </button>
            </div>
          </div>
        </form>
        <div class="text-left">
          <h2>修改密码</h2>
        </div>
        <form class="form-horizontal">
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
            <div class="col-md-2"></div>
            <div class="col-md-4 text-left">
              <button type="button" class="btn btn-lg btn-danger btn-block" v-on:click.prevent="do_cls">清空</button>
            </div>
            <div class="col-md-2"></div>
            <div class="col-md-4 text-right">
              <button type="submit" class="btn btn-lg btn-primary btn-block" v-on:click.prevent="do_submit2">确定
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
        this.username = this.$store.state.username
    },
    methods: {
      do_submit1() {
        let data = {
          "username": this.username,
        };
        let json = JSON.stringify(data)
        axios({
            method: "post",
            url: "/api/user_settings/",
            headers: {
              'Content-Type': 'application/json;charset=UTF-8'
            },
            data: json
          }
        ).then(function (response) {
          console.log(response.data)
          if(response.data.status === "ok"){
              this.$store.commit("change_name",this.username)
          }else{
              this.username = this.$store.state.username
          }
        }.bind(this)).catch(function (err) {
          console.log(err)
          this.username = this.$store.state.username
        });
      },
      do_submit2() {
        let data = {
          "password": this.password,
        };
        let json = JSON.stringify(data)
        axios({
            method: "post",
            url: "/api/user_settings/",
            headers: {
              'Content-Type': 'application/json;charset=UTF-8'
            },
            data: json
          }
        ).then(function (response) {
          console.log(response.data)
          if(response.data.status === "ok"){
            this.$store.dispatch("logout")
          }else{
          }
        }.bind(this)).catch(function (err) {
          console.log(err)
        });
      },
      do_cls(){
        this.username = ""
        this.password = ""
        this.confirm_password = ""
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
</style>
