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
  import {createDisconnectAlert, createMessageDialog} from '../common/dialog'
  export default {
    name: 'test',
    data () {
      return {
        time: "",
        socket: null,
        worker: null,
        fail_alert: null
      }
    },
    mounted () {
//      this.$confirm("hello")
      let socket = io("/test")
      this.socket = socket
      socket.on('connect', () => {
        console.log(this.fail_alert)
        if (this.fail_alert) {
          this.fail_alert.close()
          this.fail_alert = null
        }
        socketio_check_csrftoken(socket)
      })
      socket.on('disconnect', () => {
        console.info("disconnect")
        if (!this.fail_alert) {
          this.fail_alert = createDisconnectAlert()
        }
        console.log(this.fail_alert)

      });
      socket.on('update_time', (json) => {
        this.time = moment(json.timestamp, "x").format('YYYY-MM-DD HH:mm:ss');
      })
      let tick = () => {
        socket.emit("gettime", (json) => {
          console.log(json)
        })
      }
      tick();
      this.worker = setInterval(tick, 1000)
    },
    destroyed(){
      if (this.fail_alert) {
        this.fail_alert.close()
      }
      this.fail_alert = true
      if (this.worker) {
        clearInterval(this.worker)
      }
      if (this.socket) {
        this.socket.close()
      }
    },
    methods: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
  @import "../assets/less/index";
</style>
