<template>
  <div>
    <nav class="navbar navbar-default" role="navigation">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                  data-target="#bs-example-navbar-collapse-1">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">{{ name }}</a>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav">
            <router-link tag="li" to="/1"><a>1</a></router-link>
            <router-link tag="li" to="/2"><a>2</a></router-link>
            <router-link tag="li" to="/3"><a>3</a></router-link>
            <!--<li class="dropdown">-->
            <!--<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <span class="caret"></span></a>-->
            <!--<ul class="dropdown-menu" role="menu">-->
            <!--<li><a href="#">Action</a></li>-->
            <!--<li><a href="#">Another action</a></li>-->
            <!--<li><a href="#">Something else here</a></li>-->
            <!--<li class="divider"></li>-->
            <!--<li><a href="#">Separated link</a></li>-->
            <!--<li class="divider"></li>-->
            <!--<li><a href="#">One more separated link</a></li>-->
            <!--</ul>-->
            <!--</li>-->
          </ul>
          <!--<form class="navbar-form navbar-left" role="search">-->
          <!--<div class="form-group">-->
          <!--<input type="text" class="form-control" placeholder="Search">-->
          <!--</div>-->
          <!--<button type="submit" class="btn btn-default">Submit</button>-->
          <!--</form>-->
          <!--<ul class="nav navbar-nav navbar-right">-->
          <!--<li><a href="#">Link</a></li>-->
          <!--<li class="dropdown">-->
          <!--<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <span class="caret"></span></a>-->
          <!--<ul class="dropdown-menu" role="menu">-->
          <!--<li><a href="#">Action</a></li>-->
          <!--<li><a href="#">Another action</a></li>-->
          <!--<li><a href="#">Something else here</a></li>-->
          <!--<li class="divider"></li>-->
          <!--<li><a href="#">Separated link</a></li>-->
          <!--</ul>-->
          <!--</li>-->
          <!--</ul>-->
          <ul class="nav navbar-nav navbar-right">
            <li><a>系统时间：{{system_time}}</a></li>
            <li v-if="is_admin"><a href="/admin/">后台管理</a></li>
            <router-link tag="li" to="/user_settings" v-if="username"><a>当前用户：{{username}}</a></router-link>
            <li v-if="username"  v-on:click.prevent="do_logout"><a href="#">登出</a></li>
            <router-link tag="li" to="/login" v-if="!username"><a>登录</a></router-link>
            <router-link tag="li" to="/register" v-if="!username"><a>注册</a></router-link>

          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>
  </div>
</template>

<script>
  import moment from 'moment'
  export default {
    name: 'hello',
    data () {
      return {
        name: 'TEST',
        system_time: '',
        worker: null
      }
    },
    created () {
      let tick = ()=> {
        this.system_time = moment().format('YYYY-MM-DD HH:mm:ss')
      }
      tick();
      this.worker = setInterval(tick, 1000)
    },
    destroyed (){
      clearInterval(this.worker)
    },
    computed: {
      username(){
        return this.$store.state.username
      },
      is_admin(){
        return this.$store.state.is_admin
      }
    },
    methods: {
      do_logout() {
        this.$store.dispatch("logout")
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
