<template>
  <el-dialog title="考试信息确认" center="true" :visible.sync="dialogVisible">
    <span>亲爱的{{username}}同学，你即将进入“{{name}}”的考试界面，该考试共{{count}}道题目</span>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" v-on:click="showQuestion">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'DoExam',
  data () {
    return {
      dialogVisible: false,
      username: '',
      name: '',
      count: '',
      pid: '',
      eid: ''
    }
  },
  methods: {
    findPaper () {
      this.axios.post('/exam/selectpaper', {eid: this.$route.query.eid})
        .then(response => {
          this.name = response.data.name
          this.count = response.data.count
          this.pid = response.data.pid
          this.eid = response.data.eid
          this.dialogVisible = true
        })
    },
    showQuestion () {
      this.$router.push({
        path: '/showQuestion',
        query: {
          eid: this.eid,
          pid: this.pid,
          total: this.count,
          count: '1'
        }
      })
    }
  },
  mounted: function () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findPaper()
  }
}
</script>

<style scoped>

</style>
