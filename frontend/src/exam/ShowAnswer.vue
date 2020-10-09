<template>
    <el-form :model="Answer" ref="Answer">
      <el-form-item label="题目： ">
        {{this.Answer.content}}
      </el-form-item>
      <el-form-item label="分值： ">
        {{this.Answer.score}}
      </el-form-item>
      <el-form-item label="参考答案： ">
        {{this.Answer.answer}}
      </el-form-item>
      <el-form-item label="学生答案： ">
        {{this.Answer.stuanswer}}
      </el-form-item>
      <el-form-item label="得分： ">
        <el-col :span="4">
          <el-input type="number" v-model="Answer.stuscore"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
        <el-button type="primary" v-on:click="next" v-if="this.count < this.total">下一题</el-button>
        <el-button type="success" v-on:click="complete" v-if="this.count === this.total">完成</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="text" v-on:click="upCloud">点此将优秀答案上传至云笔记</el-button>
      </el-form-item>
    </el-form>
</template>

<script>
export default {
  name: 'ShowAnswer',
  data () {
    return {
      Answer: {
        content: '',
        score: '',
        answer: '',
        stuanswer: '',
        stuscore: ''
      },
      examname: '',
      qid: '',
      count: '',
      total: '',
      aid: ''
    }
  },
  methods: {
    getAnswer () {
      this.axios.get('/exam/getanswer', {
        params: {
          username: this.$route.query.username,
          examname: this.examname,
          count: this.$route.query.count
        }
      }).then(response => {
        let retdata = response.data
        this.Answer.content = retdata.content
        this.Answer.score = retdata.score
        this.Answer.answer = retdata.answer
        this.Answer.stuanswer = retdata.stuanswer
        this.total = retdata.total
        this.qid = retdata.qid
        this.count = retdata.count
        this.aid = retdata.aid
        console.log(this.count)
        console.log(this.total)
      })
    },
    addScore () {
      this.axios.post('/exam/addscore', {
        examname: this.examname,
        qid: this.qid,
        username: this.$route.query.username,
        score: this.Answer.stuscore
      })
    },
    next () {
      let max = parseInt(this.Answer.score)
      if (this.Answer.stuscore > max) {
        alert('学生得分不能大于题目分值')
      } else {
        this.addScore()
        this.$router.push({
          path: '/showAnswer',
          query: {
            username: this.$route.query.username,
            examname: this.examname,
            count: this.count + 1
          }
        })
        this.Answer.stuscore = ''
      }
      this.getAnswer()
    },
    before () {
      let max = parseInt(this.Answer.score)
      if (this.Answer.stuscore > max) {
        alert('学生得分不能大于题目分值')
      } else {
        this.addScore()
        this.$router.push({
          path: '/showAnswer',
          query: {
            username: this.$route.query.username,
            examname: this.examname,
            count: this.count - 1
          }
        })
        this.Answer.stuscore = ''
      }
      this.getAnswer()
    },
    complete () {
      let max = parseInt(this.Answer.score)
      if (this.Answer.stuscore > max) {
        alert('学生得分不能大于题目分值')
      } else {
        this.addScore()
        this.axios.post('/exam/addallscore', {
          examname: this.examname,
          username: this.$route.query.username
        })
      }
      this.$router.push('/selectScore')
    },
    upCloud () {
      this.axios.post('/exam/teachercloud', {
        teacher: this.username,
        student: this.$route.query.username,
        aid: this.aid
      }).then(response => {
        alert(response.data.msg)
      })
      this.$router.push({
        path: '/showAnswer',
        query: {
          username: this.$route.query.username,
          examname: this.examname,
          count: this.count
        }
      })
      this.getAnswer()
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.examname = this.$route.query.examname
    this.count = this.$route.query.count
    this.total = this.$route.query.total
    this.getAnswer()
  }
}
</script>

<style scoped>

</style>
