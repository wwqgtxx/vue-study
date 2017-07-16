<template>
  <div>
    <h1>{{time}}</h1>
  </div>
</template>

<script>
  import echarts from 'echarts'
  import moment from 'moment'
  import io from 'socket.io-client'
  import {socketio_check_csrftoken} from '../common/socketio_csrf_helper'
  export default {
    name: 'test',
    data () {
      return {
        time: "",
        socket: null,
        worker: null
      }
    },
    mounted () {
      let socket = io("/test")
      this.socket = socket
      socket.on('connect', function () {
        socketio_check_csrftoken(socket)
      })
      socket.on('disconnect', function () {
        console.info("disconnect")
      });
      socket.on('update_time',(json)=>{
        this.time = moment(json.timestamp, "x").format('YYYY-MM-DD HH:mm:ss');
      })
      let tick = ()=> {
        socket.emit("gettime",(json)=>{
          console.log(json)
        })
      }
      tick();
      this.worker = setInterval(tick, 1000)
    },
    destroyed(){
      if (this.socket) {
        this.socket.close()
      }
      if (this.worker){
        clearInterval(this.worker)
      }
    },
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
  @import "../assets/less/index";
</style>
