<template>
  <div id="app">
    <div class="container-fluid">
      <!-- 导航栏 -->
      <navbar></navbar>
      <!-- 路由出口 -->
      <!-- 路由匹配到的组件将渲染在这里 -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue'
  export default {
    name: 'app',
    components: {
      "navbar": Navbar
    }
  }
</script>

<style>
  /*#app {*/
  /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
  /*-webkit-font-smoothing: antialiased;*/
  /*-moz-osx-font-smoothing: grayscale;*/
  /*text-align: center;*/
  /*color: #2c3e50;*/
  /*margin-top: 60px;*/
  /*}*/
</style>
