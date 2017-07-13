<template>
  <div v-bind:class="classObject">
    <h2 class="text-center" v-text="nav_item_text"></h2>
    <div class="col-sm-1"></div>
    <div class="col-sm-10">
      <div v-for="item in page_texts">
        <p class="h4" v-text="item"></p>
      </div>
      <p>&nbsp;</p>
      <p>&nbsp;</p>
      <p>&nbsp;</p>
      <p>&nbsp;</p>
    </div>
  </div>
</template>

<script>
  import json from "../json/index_data.json"
  export default {
    name: 'index',
    data () {
      return {
        id: 1
      }
    },
    computed: {
      page_texts(){
        return json[`page_${this.id}_texts`]
      },
      nav_item_text(){
        return json["nav_item_texts"][this.id - 1]
      },
      classObject: function () {
        let map = {};
        map[`page_${this.id}_div`] = true
        return map
      }
    },
    mounted () {
      console.info(this.$route.params)
      if (this.$route.params.id !== undefined) {
        this.id = this.$route.params.id;
      } else {
        this.$router.replace("/page/1")
      }

    },
    watch: {
      '$route' (to, from) {
        // 对路由变化作出响应...
        console.info(to.params)
        if (to.params.id !== undefined) {
          this.id = to.params.id;
        } else {
          this.$router.replace("/page/1")
        }
      }
    },
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
