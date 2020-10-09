<template>
  <el-main class="app-body"  style="margin-top:20px">
    <template>
      <div class="choose">
        <div style="text-align: right">
          <el-link type="success" v-on:click="showUpload">使用docx文件上传题目</el-link>
          <el-link type="primary" v-on:click="showExplain">点此查看上传说明</el-link>
        </div>
        <el-form label-position="right" label-width="100px">
          <el-form-item label="题目类型： ">
            <el-select @visible-change="$forceUpdate()" v-model="value" placeholder="请选择题目类型" @change="chooseType">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="课程： ">
            <el-select v-model="course" placeholder="请选择课程" @change="chooseCourse">
              <el-option
                v-for="item in courseoption"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="章节： ">
            <el-select @visible-change="$forceUpdate()" v-model="chapter" placeholder="请选择章" @change="chooseChapter">
              <el-option
                v-for="item in chapteroption"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-select @visible-change="$forceUpdate()" v-model="section" placeholder="请选择节">
              <el-option
                v-for="item in sectionoption"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <!--            单选内容-->
      <div id="simple" v-show="simpleShow">
        <el-form :model="Simple" ref="Simple" :rules="srules" label-position="right" label-width="100px">
          <el-form-item label="题干" prop="content" style="text-align: center">
            <el-col :span="12">
              <el-input type="textarea" v-model="Simple.content" placeholder="请输入题干"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="选项A" prop="choice1">
            <el-col :span="12">
              <el-input type="text" v-model="Simple.choice1" placeholder="请输入选项A"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="选项B" prop="choice2">
            <el-col :span="12">
              <el-input type="text" v-model="Simple.choice2" placeholder="请输入选项B"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="选项C" prop="choice3">
            <el-col :span="12">
              <el-input type="text" v-model="Simple.choice3" placeholder="请输入选项C"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="选项D" prop="choice4">
            <el-col :span="12">
              <el-input type="text" v-model="Simple.choice4" placeholder="请输入选项D"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-radio-group v-model="Simple.answer">
              <el-radio label="1">选项A</el-radio>
              <el-radio label="2">选项B</el-radio>
              <el-radio label="3">选项C</el-radio>
              <el-radio label="4">选项D</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="图片" prop="picture" id="picture">
            <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :auto-upload="false"
              on-success="handleSuccess"
              accept=".jpg, .png"
              ref="picture"
              :file-list="fileList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
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
        <el-form :model="Multiple" ref="Multiple" :rules="mrules" label-position="right" label-width="100px">
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
          <el-form-item label="图片" prop="picture">
            <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :auto-upload="false"
              on-success="handleSuccess"
              accept=".jpg, .png"
              ref="picture"
              :file-list="fileList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
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
        <el-form :model="Blank" ref="Blank" :rules="brules" label-position="right" label-width="100px">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Blank.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-input type="text" v-model="Blank.answer" placeholder="请输入答案"></el-input>
          </el-form-item>
          <el-form-item label="图片" prop="picture">
            <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :auto-upload="false"
              on-success="handleSuccess"
              accept=".jpg, .png"
              ref="picture"
              :file-list="fileList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
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
         <el-form :model="Judge" ref="Judge" :rules="jrules" label-position="right" label-width="100px">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Judge.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-radio-group v-model="Judge.answer">
              <el-radio label="1">正确</el-radio>
              <el-radio label="0">错误</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="图片" prop="picture">
            <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :auto-upload="false"
              on-success="handleSuccess"
              accept=".jpg, .png"
              ref="picture"
              :file-list="fileList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
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
        <el-form :model="Subjective" ref="Subjective" :rules="sbrules" label-position="right" label-width="100px">
          <el-form-item label="题干" prop="content">
            <el-input type="textarea" v-model="Subjective.content" placeholder="请输入题干"></el-input>
          </el-form-item>
          <el-form-item label="参考答案" prop="answer">
            <el-input type="textarea" v-model="Subjective.answer" placeholder="请输入参考答案"></el-input>
          </el-form-item>
          <el-form-item label="图片" prop="picture">
            <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :auto-upload="false"
              on-success="handleSuccess"
              accept=".jpg, .png"
              ref="picture"
              :file-list="fileList"
              list-type="picture">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
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
      <!--      docx文件上传及相关说明-->
      <div>
        <el-dialog title="docx文件上传" center="true" :visible.sync="docxShow">
          <el-upload
            :limit="1"
            style="text-align: center"
            :file-list="docxList"
            accept=".docx"
            ref="docx"
            :auto-upload="false"
            action=""
            :on-change="handleChange"
            :on-preview="handlePreview"
            :on-remove="handleRemove">
            <el-button slot="trigger" size="small" type="primary">选择文件</el-button>
            <el-button size="small" type="success" @click="uploadDocx">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">请先阅读上传说明，只能上传docx文件，且不超过500kb</div>
          </el-upload>
        </el-dialog>
      </div>
      <div>
        <el-dialog title="docx文件排版说明" center="true" :visible.sync="explainShow" width="950px">
          <img src="@/assets/explain1.png" width="900px" height="320px">
          <img src="@/assets/explain2.png" width="900px" height="740px">
        </el-dialog>
      </div>
    </template>
  </el-main>
</template>

<script>
export default {
  name: 'AddQuestion',
  data () {
    return {
      simpleShow: false,
      multipleShow: false,
      blankShow: false,
      judgeShow: false,
      subjectiveShow: false,
      docxShow: false,
      explainShow: false,
      username: '',
      isCollapse: false,
      type: '',
      options: [{
        value: 1,
        label: '单项选择题'
      }, {
        value: 2,
        label: '多项选择题'
      }, {
        value: 3,
        label: '填空题'
      }, {
        value: 4,
        label: '判断题'
      }, {
        value: 5,
        label: '主观题'
      }],
      course: '',
      chapter: '',
      section: '',
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
      },
      fileList: [],
      docxList: [],
      courseoption: [],
      chapteroption: [],
      sectionoption: [],
      srules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}],
        chapter: [{required: true, message: '请选择章数', trigger: 'blur'}],
        section: [{required: true, message: '请选择节数', trigger: 'blur'}],
        content: [{required: true, message: '请输入题干', trigger: 'blur'}],
        choice1: [{required: true, message: '请输入选项A', trigger: 'blur'}],
        choice2: [{required: true, message: '请输入选项B', trigger: 'blur'}],
        choice3: [{required: true, message: '请输入选项C', trigger: 'blur'}],
        choice4: [{required: true, message: '请输入选项D', trigger: 'blur'}],
        answer: [{required: true, message: '请选择参考答案', trigger: 'blur'}],
        count: [{required: true, message: '请选择难度系数', trigger: 'blur'}]
      },
      mrules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}],
        chapter: [{required: true, message: '请选择章数', trigger: 'blur'}],
        section: [{required: true, message: '请选择节数', trigger: 'blur'}],
        content: [{required: true, message: '请输入题干', trigger: 'blur'}],
        choice1: [{required: true, message: '请输入选项A', trigger: 'blur'}],
        choice2: [{required: true, message: '请输入选项B', trigger: 'blur'}],
        choice3: [{required: true, message: '请输入选项C', trigger: 'blur'}],
        choice4: [{required: true, message: '请输入选项D', trigger: 'blur'}],
        answerList: [{required: true, message: '请选择参考答案', trigger: 'blur'}],
        count: [{required: true, message: '请选择难度系数', trigger: 'blur'}]
      },
      brules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}],
        chapter: [{required: true, message: '请选择章数', trigger: 'blur'}],
        section: [{required: true, message: '请选择节数', trigger: 'blur'}],
        content: [{required: true, message: '请输入题干', trigger: 'blur'}],
        answer: [{required: true, message: '请输入参考答案', trigger: 'blur'}],
        count: [{required: true, message: '请选择难度系数', trigger: 'blur'}]
      },
      jrules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}],
        chapter: [{required: true, message: '请选择章数', trigger: 'blur'}],
        section: [{required: true, message: '请选择节数', trigger: 'blur'}],
        content: [{required: true, message: '请输入题干', trigger: 'blur'}],
        answer: [{required: true, message: '请输入参考答案', trigger: 'blur'}],
        count: [{required: true, message: '请选择难度系数', trigger: 'blur'}]
      },
      sbrules: {
        course: [{required: true, message: '请选择课程', trigger: 'blur'}],
        chapter: [{required: true, message: '请选择章数', trigger: 'blur'}],
        section: [{required: true, message: '请选择节数', trigger: 'blur'}],
        content: [{required: true, message: '请输入题干', trigger: 'blur'}],
        answer: [{required: true, message: '请输入参考答案', trigger: 'blur'}],
        count: [{required: true, message: '请选择难度系数', trigger: 'blur'}]
      }
    }
  },
  methods: {
    chooseType: function (value) {
      if (value === 1) {
        this.simpleShow = true
        this.multipleShow = false
        this.blankShow = false
        this.judgeShow = false
        this.subjectiveShow = false
        this.type = 1
      } else if (value === 2) {
        this.simpleShow = false
        this.multipleShow = true
        this.blankShow = false
        this.judgeShow = false
        this.subjectiveShow = false
        this.type = 2
      } else if (value === 3) {
        this.simpleShow = false
        this.multipleShow = false
        this.blankShow = true
        this.judgeShow = false
        this.subjectiveShow = false
        this.type = 3
      } else if (value === 4) {
        this.simpleShow = false
        this.multipleShow = false
        this.blankShow = false
        this.judgeShow = true
        this.subjectiveShow = false
        this.type = 4
      } else if (value === 5) {
        this.simpleShow = false
        this.multipleShow = false
        this.blankShow = false
        this.judgeShow = false
        this.subjectiveShow = true
        this.type = 5
      }
    },
    chooseCourse () {
      this.findChapter()
    },
    chooseChapter () {
      this.findSection()
    },
    submited: function (formdata) {
      this.$refs[formdata].validate((valid) => {
        if (valid) {
          let data = new FormData()
          if (this.type === 1) {
            data.append('username', this.username)
            data.append('type', this.type)
            data.append('content', this.Simple.content)
            data.append('choice1', this.Simple.choice1)
            data.append('choice2', this.Simple.choice2)
            data.append('choice3', this.Simple.choice3)
            data.append('choice4', this.Simple.choice4)
            data.append('answer', this.Simple.answer)
            if (this.$refs['picture'].fileList[0] != null) {
              data.append('picture', this.$refs['picture'].fileList[0].raw)
            } else {
              data.append('picture', '')
            }
            data.append('score', this.Simple.score)
            data.append('course', this.course)
            data.append('chapter', this.chapter)
            data.append('section', this.section)
            data.append('count', this.Simple.count)
          } else if (this.type === 2) {
            data.append('username', this.username)
            data.append('type', this.type)
            data.append('content', this.Multiple.content)
            data.append('choice1', this.Multiple.choice1)
            data.append('choice2', this.Multiple.choice2)
            data.append('choice3', this.Multiple.choice3)
            data.append('choice4', this.Multiple.choice4)
            data.append('answerList', this.Multiple.answerList)
            if (this.$refs['picture'].fileList[0] != null) {
              data.append('picture', this.$refs['picture'].fileList[0].raw)
            } else {
              data.append('picture', '')
            }
            data.append('score', this.Multiple.score)
            data.append('course', this.course)
            data.append('chapter', this.chapter)
            data.append('section', this.section)
            data.append('count', this.Multiple.count)
          } else if (this.type === 3) {
            data.append('username', this.username)
            data.append('type', this.type)
            data.append('content', this.Blank.content)
            data.append('answer', this.Blank.answer)
            if (this.$refs['picture'].fileList[0] != null) {
              data.append('picture', this.$refs['picture'].fileList[0].raw)
            } else {
              data.append('picture', '')
            }
            data.append('score', this.Blank.score)
            data.append('course', this.course)
            data.append('chapter', this.chapter)
            data.append('section', this.section)
            data.append('count', this.Blank.count)
          } else if (this.type === 4) {
            data.append('username', this.username)
            data.append('type', this.type)
            data.append('content', this.Judge.content)
            data.append('answer', this.Judge.answer)
            if (this.$refs['picture'].fileList[0] != null) {
              data.append('picture', this.$refs['picture'].fileList[0].raw)
            } else {
              data.append('picture', '')
            }
            data.append('score', this.Judge.score)
            data.append('course', this.course)
            data.append('chapter', this.chapter)
            data.append('section', this.section)
            data.append('count', this.Judge.count)
          } else if (this.type === 5) {
            data.append('username', this.username)
            data.append('type', this.type)
            data.append('content', this.Subjective.content)
            data.append('answer', this.Subjective.answer)
            if (this.$refs['picture'].fileList[0] != null) {
              data.append('picture', this.$refs['picture'].fileList[0].raw)
            } else {
              data.append('picture', '')
            }
            data.append('score', this.Subjective.score)
            data.append('course', this.course)
            data.append('chapter', this.chapter)
            data.append('section', this.section)
            data.append('count', this.Subjective.count)
          }
          let config = {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
          this.axios.post('/exam/addquestion', data, config).then(response => {
            alert(response.data.msg)
          })
        } else {
          return false
        }
      })
    },
    findCourse () {
      this.axios.post('/exam/findcourse', {username: this.username})
        .then(response => {
          this.courseoption = response.data.nameList
        })
    },
    findChapter () {
      this.axios.post('/exam/findchapter', {
        username: this.username,
        course: this.course
      }).then(response => {
        console.log(response.data)
        this.chapteroption = response.data.chapteroption
      })
    },
    findSection () {
      this.axios.post('/exam/findsection', {
        username: this.username,
        course: this.course,
        chapter: this.chapter
      }).then(response => {
        console.log(response.data)
        this.sectionoption = response.data.sectionoption
        console.log(this.sectionoption)
      })
    },
    toggleSideBar () {
      this.isCollapse = !this.isCollapse
    },
    handleSuccess (response, file) {
      this.$message.success(response.msg)
    },
    handleChange (file, fileList) {
      this.fileList = fileList.slice(-3)
    },
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove (file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    showUpload () {
      this.docxShow = true
    },
    uploadDocx () {
      let formData = new FormData()
      formData.append('username', this.username)
      formData.append('docx', this.$refs.docx.$refs['upload-inner'].fileList[0].raw)
      this.axios.post('/exam/uploaddocx', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(response => {
          alert(response.data.msg)
        })
    },
    showExplain () {
      this.explainShow = true
    }
  },
  mounted: function () {
    let user = sessionStorage.getItem('username')
    if (user) {
      this.username = user
    }
    this.findCourse()
  }
}
</script>

<style scoped>

</style>
