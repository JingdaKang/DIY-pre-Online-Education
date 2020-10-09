<template>
  <div  style="margin-top:20px">
    <div style="text-align: center">
      <span style="font-size: x-large">试题列表</span>
    </div>
    <el-table
      :data="tableData"
      border="true"
      stripe
      :header-cell-style="headStyle"
      style="width: 100%">
      <el-table-column prop="id" label="编号" width="180" align="center">
      </el-table-column>
      <el-table-column prop="course" label="课程" width="180" align="center">
      </el-table-column>
      <el-table-column prop="type" label="类型" width="180" align="center"
                       :filters="[{text: '单项选择题', value: '单项选择题'}, {text: '多项选择题', value: '多项选择题'}, {text: '填空题', value: '填空题'},
                                  {text: '判断题', value: '判断题'}, {text: '主观题', value: '主观题'}]"
                       :filter-method="filterType">
      </el-table-column>
      <el-table-column prop="content" label="题干" align="center">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        align="center"
        width="100">
        <template slot-scope="scope">
          <el-button type="text" v-on:click="changeQuestion(scope.row)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-size="10"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
    <el-dialog title="试题信息修改" center="true" :visible.sync="dialogVisible">
      <!--            单选内容-->
      <div id="simple" v-show="simpleShow">
        <el-form :model="Simple" ref="Simple" :rules="srules">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Simple.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="选项A" prop="choice1">
            <el-input type="text" v-model="Simple.choice1" placeholder="请输入选项A"></el-input>
          </el-form-item>
          <el-form-item label="选项B" prop="choice2">
            <el-input type="text" v-model="Simple.choice2" placeholder="请输入选项B"></el-input>
          </el-form-item>
          <el-form-item label="选项C" prop="choice3">
            <el-input type="text" v-model="Simple.choice3" placeholder="请输入选项C"></el-input>
          </el-form-item>
          <el-form-item label="选项D" prop="choice4">
            <el-input type="text" v-model="Simple.choice4" placeholder="请输入选项D"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-radio-group v-model="Simple.answer">
              <el-radio label="1">选项A</el-radio>
              <el-radio label="2">选项B</el-radio>
              <el-radio label="3">选项C</el-radio>
              <el-radio label="4">选项D</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="难度系数" prop="count">
            <el-radio-group v-model="Simple.count">
              <el-radio-button label="1"></el-radio-button>
              <el-radio-button label="2"></el-radio-button>
              <el-radio-button label="3"></el-radio-button>
              <el-radio-button label="4"></el-radio-button>
              <el-radio-button label="5"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="submited('Simple')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!--            多选内容-->
      <div id="multiple" v-show="multipleShow">
        <el-form :model="Multiple" ref="Multiple" :rules="mrules">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Multiple.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="选项A" prop="choice1">
            <el-input type="text" v-model="Multiple.choice1" placeholder="请输入选项1"></el-input>
          </el-form-item>
          <el-form-item label="选项B" prop="choice2">
            <el-input type="text" v-model="Multiple.choice2" placeholder="请输入选项2"></el-input>
          </el-form-item>
          <el-form-item label="选项C" prop="choice3">
            <el-input type="text" v-model="Multiple.choice3" placeholder="请输入选项3"></el-input>
          </el-form-item>
          <el-form-item label="选项D" prop="choice4">
            <el-input type="text" v-model="Multiple.choice4" placeholder="请输入选项4"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-checkbox-group v-model="Multiple.answerList">
              <el-checkbox label="A"></el-checkbox>
              <el-checkbox label="B"></el-checkbox>
              <el-checkbox label="C"></el-checkbox>
              <el-checkbox label="D"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="难度系数" prop="count">
            <el-radio-group v-model="Multiple.count">
              <el-radio-button label="1"></el-radio-button>
              <el-radio-button label="2"></el-radio-button>
              <el-radio-button label="3"></el-radio-button>
              <el-radio-button label="4"></el-radio-button>
              <el-radio-button label="5"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="submited('Multiple')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!--            填空内容-->
      <div id="blank" v-show="blankShow">
        <el-form :model="Blank" ref="Blank" :rules="brules">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Blank.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-input type="text" v-model="Blank.answer" placeholder="请输入答案"></el-input>
          </el-form-item>
          <el-form-item label="难度系数" prop="count">
            <el-radio-group v-model="Blank.count">
              <el-radio-button label="1"></el-radio-button>
              <el-radio-button label="2"></el-radio-button>
              <el-radio-button label="3"></el-radio-button>
              <el-radio-button label="4"></el-radio-button>
              <el-radio-button label="5"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="submited('Blank')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!--            判断内容-->
      <div id="judge" v-show="judgeShow">
         <el-form :model="Judge" ref="Judge" :rules="jrules">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Judge.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-radio-group v-model="Judge.answer">
              <el-radio label="1">正确</el-radio>
              <el-radio label="0">错误</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="难度系数" prop="count">
            <el-radio-group v-model="Judge.count">
              <el-radio-button label="1"></el-radio-button>
              <el-radio-button label="2"></el-radio-button>
              <el-radio-button label="3"></el-radio-button>
              <el-radio-button label="4"></el-radio-button>
              <el-radio-button label="5"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="submited('Judge')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!--            主观内容-->
      <div id="subjective" v-show="subjectiveShow">
        <el-form :model="Subjective" ref="Subjective" :rules="sbrules">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Subjective.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-input type="text" v-model="Subjective.answer" placeholder="请输入参考答案"></el-input>
          </el-form-item>
          <el-form-item label="难度系数" prop="count">
            <el-radio-group v-model="Subjective.count">
              <el-radio-button label="1"></el-radio-button>
              <el-radio-button label="2"></el-radio-button>
              <el-radio-button label="3"></el-radio-button>
              <el-radio-button label="4"></el-radio-button>
              <el-radio-button label="5"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="submited('Subjective')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'SelectQuestion',
  data () {
    return {
      username: '',
      tableData: [{
        id: '',
        course: '',
        type: '',
        content: ''
      }],
      dialogVisible: false,
      type: '',
      qid: '',
      total: '',
      currentPage: '',
      simpleShow: false,
      multipleShow: false,
      blankShow: false,
      judgeShow: false,
      subjectiveShow: false,
      Simple: {
        content: '',
        choice1: '',
        choice2: '',
        choice3: '',
        choice4: '',
        answer: '',
        picture: '',
        count: ''
      },
      Multiple: {
        content: '',
        choice1: '',
        choice2: '',
        choice3: '',
        choice4: '',
        answerList: [],
        picture: '',
        count: ''
      },
      Blank: {
        content: '',
        answer: '',
        picture: '',
        count: ''
      },
      Judge: {
        content: '',
        answer: '',
        picture: '',
        count: ''
      },
      Subjective: {
        content: '',
        answer: '',
        picture: '',
        count: ''
      }
    }
  },
  methods: {
    filterType (value, row) {
      return row.type === value
    },
    selectQuestion () {
      this.axios.get('/exam/selectquestion', {
        params: {
          username: this.username,
          currentPage: this.currentPage
        }
      })
        .then(response => {
          this.total = response.data.total
          this.currentPage = response.data.currentPage
          console.log(response)
          console.log(this.total)
          console.log(this.currentPage)
          this.tableData = response.data.tableData
        })
    },
    changeQuestion (row) {
      this.qid = row.id
      this.axios.get('exam/findquestion', {
        params: {
          'qid': this.qid
        }
      }).then(response => {
        let data = response.data
        this.type = data.type
        let type = data.type
        if (type === '1') {
          this.simpleShow = true
          this.multipleShow = false
          this.blankShow = false
          this.judgeShow = false
          this.subjectiveShow = false
          this.Simple.content = data.content
          this.Simple.choice1 = data.choice1
          this.Simple.choice2 = data.choice2
          this.Simple.choice3 = data.choice3
          this.Simple.choice4 = data.choice4
          this.Simple.answer = data.answer
          this.Simple.count = data.count
        } else if (type === '2') {
          this.simpleShow = false
          this.multipleShow = true
          this.blankShow = false
          this.judgeShow = false
          this.subjectiveShow = false
          this.Multiple.content = data.content
          this.Multiple.choice1 = data.choice1
          this.Multiple.choice2 = data.choice2
          this.Multiple.choice3 = data.choice3
          this.Multiple.choice4 = data.choice4
          this.Multiple.answerList = data.answerList
          this.Multiple.count = data.count
        } else if (type === '3') {
          this.simpleShow = false
          this.multipleShow = false
          this.blankShow = true
          this.judgeShow = false
          this.subjectiveShow = false
          this.Blank.content = data.content
          this.Blank.answer = data.answer
          this.Blank.count = data.count
        } else if (type === '4') {
          this.simpleShow = false
          this.multipleShow = false
          this.blankShow = false
          this.judgeShow = true
          this.subjectiveShow = false
          this.Judge.content = data.content
          this.Judge.answer = data.answer
          this.Judge.count = data.count
        } else if (type === '5') {
          this.simpleShow = false
          this.multipleShow = false
          this.blankShow = false
          this.judgeShow = false
          this.subjectiveShow = true
          this.Subjective.content = data.content
          this.Subjective.answer = data.answer
          this.Subjective.count = data.count
        }
        this.dialogVisible = true
      })
    },
    submited (formdata) {
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          let data = new FormData()
          data.append('qid', this.qid)
          data.append('type', this.type)
          if (this.type === '1') {
            data.append('content', this.Simple.content)
            data.append('choice1', this.Simple.choice1)
            data.append('choice2', this.Simple.choice2)
            data.append('choice3', this.Simple.choice3)
            data.append('choice4', this.Simple.choice4)
            data.append('answer', this.Simple.answer)
            data.append('count', this.Simple.count)
          } else if (this.type === '2') {
            data.append('content', this.Multiple.content)
            data.append('choice1', this.Multiple.choice1)
            data.append('choice2', this.Multiple.choice2)
            data.append('choice3', this.Multiple.choice3)
            data.append('choice4', this.Multiple.choice4)
            data.append('answerList', this.Multiple.answerList)
            data.append('count', this.Multiple.count)
          } else if (this.type === '3') {
            data.append('content', this.Blank.content)
            data.append('answer', this.Blank.answer)
            data.append('count', this.Blank.count)
          } else if (this.type === '4') {
            data.append('content', this.Judge.content)
            data.append('answer', this.Judge.answer)
            data.append('count', this.Judge.count)
          } else if (this.type === '5') {
            data.append('content', this.Subjective.content)
            data.append('answer', this.Subjective.answer)
            data.append('count', this.Subjective.count)
          }
          this.axios.post('/exam/changequestion', data)
            .then(response => {
              alert(response.data.msg)
              this.dialogVisible = false
            })
        }
      })
    },
    headStyle () {
      return 'text-align: center;background:#eef1f6;'
    },
    handleCurrentChange (currentPage) {
      this.$router.push({
        path: '/selectQuestion',
        query: {
          'currentPage': currentPage
        }
      })
      this.selectQuestion()
    },
    before () {
      this.$router.push({
        path: '/selectQuestion',
        query: {
          'currentPage': this.currentPage - 1
        }
      })
      this.selectQuestion()
    },
    next () {
      this.$router.push({
        path: '/selectQuestion',
        query: {
          'currentPage': this.currentPage + 1
        }
      })
      this.selectQuestion()
    }
  },
  mounted: function () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    if (!this.$route.query.currentPage) {
      this.currentPage = 1
    } else {
      this.currentPage = this.$route.query.currentPage
    }
    this.selectQuestion()
  }
}
</script>

<style scoped>
.el-table{
  text-align: center;
}
</style>
