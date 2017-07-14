<template>
  <div>
    <div class="alert alert-warning" v-for="(item, index) in message">
      <a href="#" class="close" data-dismiss="alert">
        &times;
      </a>
      <strong>警告！</strong>{{item}}
    </div>
  </div>
</template>

<script>
  export default {
    name: 'warning_alert',
    props: ['message'],
    data () {
      return {}
    },
    computed: {},
    watch: {},
    mounted () {},
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
</style>
