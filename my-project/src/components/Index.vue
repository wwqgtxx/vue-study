<template>
  <div>
    <div class="col-sm-2">
      <nav class="navbar navbar-default" role="navigation">
        <ul class="nav nav-pills nav-stacked">
          <router-link tag="li" role="presentation" to="/page/1"><a>{{nav_item_texts[0]}}</a></router-link>
          <router-link tag="li" role="presentation" to="/page/2"><a>{{nav_item_texts[1]}}</a></router-link>
          <router-link tag="li" role="presentation" to="/page/3"><a>{{nav_item_texts[2]}}</a></router-link>
          <router-link tag="li" role="presentation" to="/page/4"><a>{{nav_item_texts[3]}}</a></router-link>
          <router-link tag="li" role="presentation" to="/page/5"><a>{{nav_item_texts[4]}}</a></router-link>
          <router-link tag="li" role="presentation" to="/page/6"><a>{{nav_item_texts[5]}}</a></router-link>
        </ul>
      </nav>
    </div>
    <div class="col-sm-10">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import echarts from 'echarts'
  import moment from 'moment'
  import Cookie from 'js-cookie'
  import json from "../json/index_data.json"
  export default {
    name: 'index',
    data () {
      return {
        nav_item_texts: json["nav_item_texts"],
      }
    },
    mounted () {

    },
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
  @import "../assets/less/index";
</style>
