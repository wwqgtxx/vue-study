<template>
  <div v-bind:class="classObject">
    <h2 class="text-center" v-text="nav_item_text"></h2>
    <form class="form-horizontal" v-on:submit.prevent="submit">
      <div class="form-group">
        <label class="col-sm-2 control-label">标 题：</label>
        <div class="col-sm-8">
          <input type="text" class="form-control"
                 name="title" placeholder="请输入你的标题" v-model="input_title">
        </div>
      </div>
      <div class="form-group">
        <label class="col-sm-2 control-label">内 容：</label>
        <div class="col-sm-8">
                                <textarea class="form-control" rows="6"
                                          name="text" placeholder="请输入你的意见" v-model="text"></textarea>
        </div>
      </div>
      <input type="hidden" name="_csrf_token" value=""/>
      <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-default">提交</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
  import json from "../json/index_data.json"
  export default {
    name: 'index',
    data () {
      return {
        id: 6,
        nav_item_text: "问题反馈",
        input_title: "",
        text: ""
      }
    },
    computed: {
      classObject: function () {
        let map = {};
        map['page_' + this.id + '_div'] = true
        return map
      }
    },
    mounted () {
    },
    watch: {},
    methods: {
      submit: function (event) {
        let data = {
          "title": this.input_title,
          "text": this.text
        };
        alert(JSON.stringify(data))
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
