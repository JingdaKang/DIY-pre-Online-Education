<template>
    <el-dialog title="试卷详情页" center="true" :visible.sync="dialogVisible">
      <div><span style="font-size: large">试卷名：{{name}}</span></div>
      <br/>
      <el-row>{{count}}. {{content}} ({{score}}分)</el-row>
      <br/>
      <div v-show="choiceShow">
        A. {{choice1}}<br/>
        B. {{choice2}}<br/>
        C. {{choice3}}<br/>
        D. {{choice4}}<br/>
      </div>
      <br/>
      <img :src="pic" width="200" height="200" v-show="imgShow">
      <br/>
      <el-pagination layout="prev, pager, next"
                     background
                     @current-change="gotoPage"
                     :current-page.sync="count"
                     :total="total"
                     :page-size="1">
      </el-pagination>
    </el-dialog>
</template>

<script>
export default {
  name: 'ShowPaper',
  data () {
    return {
      name: '',
      count: '',
      total: '',
      content: '',
      choice1: '',
      choice2: '',
      choice3: '',
      choice4: '',
      score: '',
      pic: '',
      dialogVisible: true,
      choiceShow: true,
      imgShow: false
    }
  },
  methods: {
    getQuestion () {
      this.axios.get('/exam/getquestion', {
        params: {
          'pid': this.$route.query.pid,
          'count': this.$route.query.count
        }
      }).then(response => {
        console.log(response)
        let type = response.data.type
        console.log(type)
        if (type === '1') {
          this.choice1 = response.data.choice1
          this.choice2 = response.data.choice2
          this.choice3 = response.data.choice3
          this.choice4 = response.data.choice4
          this.choiceShow = true
        } else if (type === '2') {
          this.choice1 = response.data.choice1
          this.choice2 = response.data.choice2
          this.choice3 = response.data.choice3
          this.choice4 = response.data.choice4
          this.choiceShow = true
        } else {
          this.choiceShow = false
        }
        this.content = response.data.content
        this.score = response.data.score
        this.total = response.data.total
        console.log(response.data.img)
        if (response.data.img !== '') {
          this.imgShow = true
          this.pic = '/media/' + response.data.img
        } else {
          this.imgShow = false
        }
      })
    },
    gotoPage (count) {
      this.$router.push({
        url: '/showPaper',
        query: {
          pid: this.$route.query.pid,
          name: this.$route.query.name,
          count: count
        }
      })
      this.getQuestion()
    },
    before () {
      this.$router.push({
        url: '/showPaper',
        query: {
          pid: this.$route.query.pid,
          name: this.$route.query.name,
          count: this.count - 1
        }
      })
      this.getQuestion()
    },
    next () {
      this.$router.push({
        url: '/showPaper',
        query: {
          pid: this.$route.query.pid,
          name: this.$route.query.name,
          count: this.count + 1
        }
      })
      this.getQuestion()
    }
  },
  mounted () {
    this.name = this.$route.query.name
    this.count = this.$route.query.count
    this.getQuestion()
    this.dialogVisible = true
  }
}
</script>

<style scoped>

</style>
