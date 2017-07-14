<template>
  <div class="not-found">
    Can't found the path: <b>{{ $route.fullPath }}</b>
    <div>
      Please check the url or Redirect to home page:
      <router-link to="/" replace>Home</router-link>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'NotFound',
    data () {return {}},
    mounted () {},
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
</style>
