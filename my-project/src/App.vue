<template>
  <div id="app">
    <img src="./assets/logo.png">
    <p>
      <!-- 使用 router-link 组件来导航. -->
      <!-- 通过传入 `to` 属性指定链接. -->
      <!-- <router-link> 默认会被渲染成一个 `<a>` 标签 -->
      <router-link to="/">Go to index</router-link>
      <router-link to="/2">Go to 2</router-link>
      <router-link to="/3">Go to 3</router-link>
    </p>
    <!-- 路由出口 -->
    <common-component></common-component>
    <!-- 路由匹配到的组件将渲染在这里 -->
    <router-view></router-view>
    <h1>hahaha</h1>
  </div>
</template>

<script>
  import common from './components/common.vue'
  export default {
    name: 'app',
    components: {
        "common-component" : common
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
