<template>
  <div class="hello">
    <h1>the count is:{{ msg }}</h1>
    <h2>the double_count is:{{ msg2 }}</h2>
  </div>
</template>

<script>
  export default {
    name: 'hello',
    computed:{
        msg(){
            return this.$store.state.count
        },
        msg2(){
            return this.$store.getters.double_count
        }

    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
