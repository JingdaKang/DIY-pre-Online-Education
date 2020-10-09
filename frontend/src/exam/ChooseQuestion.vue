<template>
  <div>
    <el-table
      :data="tableData"
      border="true"
      @selection-change="select"
      style="width: 100%">
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column prop="id" label="编号" width="180">
      </el-table-column>
      <el-table-column prop="type" label="类型" width="180"
                       :filters="[{text: '单项选择题', value: '单项选择题'}, {text: '多项选择题', value: '多项选择题'}, {text: '填空题', value: '填空题'},
                                  {text: '判断题', value: '判断题'}, {text: '主观题', value: '主观题'}]"
                       :filter-method="filterType">
      </el-table-column>
      <el-table-column prop="count" label="难度系数" width="180"
                       :filters="[{text: '1', value: 1},{text: '2', value: 2},{text: '3', value: 3},{text: '4', value: 4},{text: '5', value: 5},
                                  {text: '6', value: 6},{text: '7', value: 7},{text: '8', value: 8},{text: '9', value: 9},{text: '10', value: 10}]"
                       :filter-method="filterCount">
      </el-table-column>
      <el-table-column prop="content" label="题干">
      </el-table-column>
    </el-table>
    <div>
      试卷名称：
      <el-input type="text" v-model="papername" placeholder="请输入试卷名称"></el-input>
    </div>
    <el-button type="primary" v-on:click.native="addPaper">提交试卷</el-button>
  </div>
</template>

<script>
export default {
  name: 'ChooseQuestion',
  data () {
    return {
      tableData: {
        id: '',
        type: '',
        count: '',
        content: ''
      },
      scount: 0,
      mcount: 0,
      bcount: 0,
      jcount: 0,
      sbcount: 0,
      sscore: '',
      mscore: '',
      bscore: '',
      jscore: '',
      sbscore: '',
      questionList: [],
      idList: [],
      papername: ''
    }
  },
  methods: {
    filterType (value, row) {
      return row.type === value
    },
    filterCount (value, row) {
      return row.count === value
    },
    selectQuestion () {
      this.axios.get('/exam/choosequestion', {
        params: {course: this.$route.query.course}
      })
        .then(response => {
          this.tableData = response.data
          this.tableData.id = response.data.id
          this.tableData.type = response.data.type
          this.tableData.count = response.data.count
          this.tableData.content = response.data.content
        })
    },
    select (val) {
      this.questionList = ''
      console.log(this.questionList)
      this.questionList = val
      console.log(this.questionList)
    },
    addPaper () {
      this.checkCount()
      let questionData = this.questionList
      this.idList = []
      for (let i = 0; i < questionData.length; i++) {
        this.idList.push(questionData[i].id)
      }
      let data = new FormData()
      data.append('idList', this.idList)
      data.append('username', this.username)
      data.append('papername', this.papername)
      data.append('course', this.$route.query.course)
      data.append('sscore', this.sscore)
      data.append('scount', this.scount)
      data.append('mscore', this.mscore)
      data.append('mcount', this.mcount)
      data.append('bscore', this.bscore)
      data.append('bcount', this.bcount)
      data.append('jscore', this.jscore)
      data.append('jcount', this.jcount)
      data.append('sbscore', this.sbscore)
      data.append('sbcount', this.sbcount)
      this.axios.post('/exam/addPaper', data)
        .then(response => {
          alert(response.data.msg)
        })
    },
    checkCount () {
      let questionData = this.questionList
      this.scount = 0
      this.mcount = 0
      this.bcount = 0
      this.jcount = 0
      this.sbcount = 0
      for (let i = 0; i < questionData.length; i++) {
        if (questionData[i].type === '单项选择题') {
          this.scount += 1
        } else if (questionData[i].type === '多项选择题') {
          this.mcount += 1
        } else if (questionData[i].type === '填空题') {
          this.bcount += 1
        } else if (questionData[i].type === '判断题') {
          this.jcount += 1
        } else if (questionData[i].type === '主观题') {
          this.sbcount += 1
        }
      }
      if (this.$route.query.simplecount !== '' && this.scount !== this.$route.query.simplecount) {
        console.log(this.scount)
        alert('单项选择题数量错误')
        this.reload()
      } else if (this.$route.query.multiplecount !== '' && this.mcount !== this.$route.query.multiplecount) {
        console.log(this.mcount)
        alert('多项选择题数量错误')
        this.reload()
      } else if (this.$route.query.blankcount !== '' && this.bcount !== this.$route.query.blankcount) {
        alert('填空题数量错误')
        this.reload()
      } else if (this.$route.query.judgecount !== '' && this.jcount !== this.$route.query.judgecount) {
        alert('判断题数量错误')
        this.reload()
      } else if (this.$route.query.subjectivecount !== '' && this.sbcount !== this.$route.query.subjectivecount) {
        alert('主观题数量错误')
        this.reload()
      }
    }
  },
  mounted () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.sscore = this.$route.query.simplescore
    this.mscore = this.$route.query.multiplescore
    this.bscore = this.$route.query.blankscore
    this.jscore = this.$route.query.judgescore
    this.sbscore = this.$route.query.subjectivescore
    this.selectQuestion()
  }
}
</script>

<style scoped>

</style>
