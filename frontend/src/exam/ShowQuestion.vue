<template>
  <div>
    <!--    单选-->
    <div id="simple" v-show="simpleShow">
      <el-form>
        <el-form-item>
          （单项选择题）{{this.count}}. {{content}} （{{score}}分）
        </el-form-item>
        <el-form-item>
          <el-radio v-model="answer" :label="1" border>A.{{choice1}}</el-radio>
        </el-form-item>
        <el-form-item>
          <el-radio v-model="answer" :label="2" border>B.{{choice2}}</el-radio>
        </el-form-item>
        <el-form-item>
          <el-radio v-model="answer" :label="3" border>C.{{choice3}}</el-radio>
        </el-form-item>
        <el-form-item>
          <el-radio v-model="answer" :label="4" border>D.{{choice4}}</el-radio>
        </el-form-item>
        <el-form-item>
          <img :src="pic" width="200" height="200" v-show="imgShow">
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
          <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total">下一题</el-button>
          <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total">提交试卷</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!--    多选-->
    <div id="multiple" v-show="multipleShow">
      <el-form>
        <el-form-item>
          （多项选择题）{{this.count}}. {{content}} （{{score}}分）
        </el-form-item>
        <el-checkbox-group v-model="answerList" style="display: block">
          <el-form-item>
            <el-checkbox label="A" border>A.{{choice1}}</el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-checkbox label="B" border>B.{{choice2}}</el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-checkbox label="C" border>C.{{choice3}}</el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-checkbox label="D" border>D.{{choice4}}</el-checkbox>
          </el-form-item>
        </el-checkbox-group>
        <el-form-item>
          <img :src="pic" width="200" height="200" v-show="imgShow">
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
          <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total">下一题</el-button>
          <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total">提交试卷</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!--    填空-->
    <div id="blank" v-show="blankShow">
      <el-form>
        <el-form-item>
          （填空题）{{this.count}}. {{content}} （{{score}}分）
        </el-form-item>
        <el-form-item>
          <img :src="pic" width="200" height="200" v-show="imgShow">
        </el-form-item>
        <el-form-item>
          <el-input type="text" v-model="answer" placeholder="请输入答案"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
          <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total">下一题</el-button>
          <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total">提交试卷</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!--    判断-->
    <div id="judge" v-show="judgeShow">
      <el-form>
        <el-form-item>
          （判断题）{{this.count}}. {{content}} （{{score}}分）
        </el-form-item>
        <el-form-item>
          <img :src="pic" width="200" height="200" v-show="imgShow">
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="answer">
            <el-radio label="1">正确</el-radio>
            <el-radio label="0">错误</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
          <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total">下一题</el-button>
          <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total">提交试卷</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!--    主观-->
    <div id="subjective" v-show="subjectiveShow">
      <el-form>
        <el-form-item>
          （主观题）{{this.count}}. {{content}} （{{score}}分）
        </el-form-item>
        <el-form-item>
          <img :src="pic" width="200" height="200" v-show="imgShow">
        </el-form-item>
        <el-form-item>
          <el-input type="textarea" :rows="10" v-model="answer" placeholder="请输入答案"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" v-on:click="before" v-if="this.count > 1">上一题</el-button>
          <el-button type="primary" v-on:click="next" v-if="this.nextcount <= this.total">下一题</el-button>
          <el-button type="success" v-on:click="subPaper" v-if="this.nextcount > this.total">提交试卷</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!--    分页-->
    <div>
      <el-pagination layout="prev, pager, next"
                     background
                     @current-change="gotoPage"
                     :current-page.sync="count"
                     :total="total"
                     :page-size="1">
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShowQuestion',
  data () {
    return {
      eid: '',
      qid: '',
      username: '',
      answer: '',
      answerList: [],
      simpleShow: false,
      multipleShow: false,
      blankShow: false,
      judgeShow: false,
      subjectiveShow: false,
      choice1: '',
      choice2: '',
      choice3: '',
      choice4: '',
      content: '',
      count: '',
      nextcount: '',
      total: '',
      score: '',
      pic: '',
      imgShow: false
    }
  },
  methods: {
    getQuestion () {
      this.axios.get('/exam/getquestion', {
        params: {
          pid: this.$route.query.pid,
          total: this.$route.query.total,
          count: this.$route.query.count
        }
      })
        .then(response => {
          let type = response.data.type
          this.content = response.data.content
          this.qid = response.data.qid
          this.score = response.data.score
          if (response.data.img !== '') {
            this.imgShow = true
            this.pic = '/media/' + response.data.img
          } else {
            this.imgShow = false
          }
          if (type === '1') {
            this.simpleShow = true
            this.multipleShow = false
            this.blankShow = false
            this.judgeShow = false
            this.subjectiveShow = false
            this.choice1 = response.data.choice1
            this.choice2 = response.data.choice2
            this.choice3 = response.data.choice3
            this.choice4 = response.data.choice4
          } else if (type === '2') {
            this.simpleShow = false
            this.multipleShow = true
            this.blankShow = false
            this.judgeShow = false
            this.subjectiveShow = false
            this.choice1 = response.data.choice1
            this.choice2 = response.data.choice2
            this.choice3 = response.data.choice3
            this.choice4 = response.data.choice4
          } else if (type === '3') {
            this.simpleShow = false
            this.multipleShow = false
            this.blankShow = true
            this.judgeShow = false
            this.subjectiveShow = false
          } else if (type === '4') {
            this.simpleShow = false
            this.multipleShow = false
            this.blankShow = false
            this.judgeShow = true
            this.subjectiveShow = false
          } else if (type === '5') {
            this.simpleShow = false
            this.multipleShow = false
            this.blankShow = false
            this.judgeShow = false
            this.subjectiveShow = true
          }
          this.count = this.$route.query.count
          this.nextcount = response.data.nextcount
          this.answerList = []
        })
    },
    before () {
      this.updateAnswer()
      this.$router.push({
        path: '/showquestion',
        query: {
          eid: this.$route.query.eid,
          pid: this.$route.query.pid,
          total: this.$route.query.total,
          count: this.count - 1
        }
      })
      this.getQuestion()
      this.answer = ''
    },
    next () {
      this.updateAnswer()
      this.$router.push({
        path: '/showquestion',
        query: {
          eid: this.$route.query.eid,
          pid: this.$route.query.pid,
          total: this.$route.query.total,
          count: this.nextcount
        }
      })
      this.getQuestion()
      this.answer = ''
    },
    updateAnswer () {
      this.axios.post('/exam/updateanswer', {
        eid: this.$route.query.eid,
        qid: this.qid,
        answer: this.answer,
        answerList: this.answerList,
        username: this.username
      })
        .then(response => {
          console.log(response.data.msg)
        })
    },
    gotoPage (count) {
      this.count = count
      this.updateAnswer()
      this.$router.push({
        path: '/showquestion',
        query: {
          eid: this.$route.query.eid,
          pid: this.$route.query.pid,
          total: this.$route.query.total,
          count: count
        }
      })
      this.getQuestion()
      this.answer = ''
    },
    subPaper () {
      this.updateAnswer()
      this.axios.post('/exam/checkanswer', {
        username: this.username,
        eid: this.$route.query.eid
      }).then(response => {
        alert('提交成功')
        console.log(response.data.score)
        this.$router.push('/selectExam')
      })
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.total = this.$route.query.total
    this.count = this.$route.query.count
    this.eid = this.$route.query.eid
    this.getQuestion()
  }
}
</script>

<style scoped>

</style>
