<template>
  <div id="question" v-loading="loading">
    <el-card class="box-card"
             style="width:80%;margin-top:50px;margin-left:8%;min-height:600px;padding-top:10px;text-align: center">
      <el-row>
        <el-avatar :size="40" :src="avatar"
                   style="float:left;margin-left:20px"></el-avatar>
        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
          {{question.username}}</p>
        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">{{dateFormat(question.stime)}} 至
          {{dateFormat(question.etime)}}</p>
        <button v-if="question.status==1" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--success is-circle"><i
          class="el-icon-check"></i>
        </button>
        <button v-if="question.status==2" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--primary is-circle"><i
          class="el-icon-edit"></i>
        </button>
        <button v-if="question.status==3" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--warning is-circle">
          <i class="el-icon-star-off"></i>
        </button>
        <button v-if="question.status==0" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--info is-circle"><i
          class="el-icon-close"></i>
        </button>
        <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">{{question.score}}分
        </el-tag>
        <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{question.subject}}</el-tag>
      </el-row>
      <el-divider></el-divider>
      <el-row>
        <p>{{question.context}}</p>
      </el-row>
      <el-row style="margin-top: 10px">
        <el-button v-if="question.status<=1&&question.number>5&&question.username===username" type="primary"
                   @click="end_question(question.question_id)"
                   style="float:right;margin-right:3%">
          提交审核
        </el-button>
        <el-button type="success" @click="gotoForum(question.topic_id)"
                   style="float:right;margin-right:3%">
          前往论坛
        </el-button>
      </el-row>
      <el-collapse v-model="activeIndex" style="margin-top: 20px">
        <el-collapse-item v-if="question.status<2&&question.username==username" title="设置截止时间" name="1">
          <el-form :rules="rule" label-width="80px">
            <el-form-item label="截止时间" prop="deadline1" style="margin-left: 80px">
              <el-col :span="10">
                <el-date-picker
                  v-model="deadline"
                  type="datetime"
                  placeholder="选择截止时间"
                  :picker-options="pickerOptions">
                </el-date-picker>
              </el-col>
              <el-col :span="5">
                <el-button type="success" @click="activate_question(question.question_id)"
                           style="margin-left: 35%">提交
                </el-button>
              </el-col>
            </el-form-item>
          </el-form>
        </el-collapse-item>
        <el-collapse-item v-if="question.username!=username&&question.status<3&&question.status>0" title="回答问题"
                          name="1">
          <el-form :rules="rule">
            <el-form-item prop="answer_context">
              <el-input
                type="textarea"
                autosize
                placeholder="请输入内容"
                v-model="answer_context"
              >
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="submit_answer(question.question_id)"
                         style="margin-left: 35%">提交
              </el-button>
              <el-button type="info" @click="cancel_answer()">取消</el-button>
            </el-form-item>
          </el-form>
        </el-collapse-item>
        <el-collapse-item title="展开回答" name="2">
          <div v-if="question.answers.length==0" style="width:100%;height:200px">
            <h1 style="margin-top: 50px">这里什么都没有哦</h1>
          </div>
          <div class="infinite-list-wrapper"
               style="overflow-y:scroll;margin-top:20px;height: auto;width:100%">
            <ul
              class="list"
              style="list-style: none">

              <li v-for="answer in question.answers" :key="answer.answer_id" class="list-item">
                <el-card class="box-card"
                         style="width:90%;margin-left:5%;text-align: center;margin-top: 20px">
                  <el-row>
                    <el-avatar :size="40" :src="get_avatar(answer.avatar)"
                               style="float:left;margin-left:20px"></el-avatar>
                    <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                      {{answer.username}}</p>
                    <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                      {{dateFormat(answer.time)}}</p>
                    <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                      {{answer.score}}分
                    </el-tag>
                    <button v-if="answer.status==1" style="float:right;margin-right:10px" type="button"
                            class="el-button el-button--mini el-button--warning is-circle">
                      <i class="el-icon-star-off"></i>
                    </button>
                    <el-tag effect="dark" type="success" v-if="answer.from_forum==true"
                            style="float:right;margin-right:10px">
                      论坛信息
                    </el-tag>
                  </el-row>
                  <el-divider></el-divider>
                  <el-row>
                    <p v-for="item in formatText(answer.context)"
                       style="float:left;margin-left:20px;margin-right:20px;text-align: left;margin-top: 0;line-height: 20px">
                      {{item}}</p>
                  </el-row>
                  <el-form v-if="answer.score==0&&question.username==username" :rules="rule" label-width="80px"
                           style="text-align:center;margin-top:20px;margin-left:15px;padding-top: 10px;padding-bottom: 10px">
                    <el-form-item label="评分" prop="answer_score">
                      <el-col :span="12">
                        <el-input-number v-model="answer_score" @change="handleChange" :min="1"
                                         :max="question.score"></el-input-number>
                      </el-col>
                      <el-col :span="8">
                        <el-button type="success" @click="rate_answer(answer.answer_id)"
                                   style="margin-left: 35%">提交
                        </el-button>
                      </el-col>
                    </el-form-item>
                  </el-form>
                </el-card>
              </li>
            </ul>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

  </div>
</template>

<script>
  export default {
    name: "Question",
    data() {
      return {
        loading: true,
        activeIndex: '2',
        question: [],
        username: '',
        deadline: '',
        avatar: '',
        answer_score: '',
        answer_context: '',
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
        rule: {
          answer_context: [
            {
              require: true, message: '请输入内容', trigger: 'blur'
            }
          ]
        }
      }
    },
    mounted() {
      this.get_question(this.$route.params.question_id)
    },
    methods: {
      handleChange(value) {
      },
      load() {
        this.loading = true
        setTimeout(() => {
          this.count += 2
          this.loading = false
        }, 2000)
      },
      dateConversion(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes() + ":" + t.getSeconds();
        return time;
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      formatText(value) {
        return value.toString().split('\n')
      },
      get_avatar(value) {
        return "data:image/jpeg;base64," + value
      },
      get_question(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('question_id', value)
        that.axios({
          method: 'post',
          url: '/iasystem/get_question/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.question = res.data.question
              that.avatar = that.get_avatar(that.question.avatar)
              that.username = that.$cookies.get('username')
              that.loading = false
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询失败')
            }

          })
      },
      submit_answer(value) {
        if (this.$cookies.get('user_id')) {
          let that = this
          that.loading = true
          let param = new URLSearchParams()
          param.append('user_id', that.$cookies.get('user_id'))
          param.append('question_id', value)
          param.append('answer', that.answer_context)
          that.axios({
            method: 'post',
            url: '/iasystem/submit_answer/',
            data: param
          })
            .then(function (res) {
              if (res.data.code === 1) {
                that.$message({
                  message: "提交成功",
                  type: 'success'
                })
                that.loading = false
                setTimeout(function () {
                  that.$router.go(0)
                }.bind(that), 1000)
              } else if (res.data.code === 0) {
                that.loading = false
                that.$message.error('提交失败')
              }
            })
        } else {
          this.$router.push('/Login')
        }
      },
      cancel_answer() {
        this.answer_context = ''
        this.activeIndex = ''
      },
      activate_question(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('question_id', value)
        param.append('time', that.dateConversion(that.deadline))
        that.axios({
          method: 'post',
          url: '/iasystem/activate_question/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: '修改成功',
                type: 'success'
              })
              setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.$message.error('操作失败')
            }
          })
      },
      rate_answer(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('answer_id', value)
        param.append('score', that.answer_score)
        that.axios({
          method: 'post',
          url: '/iasystem/rate_answer/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: '评分成功',
                type: 'success'
              })
              setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.$message.error('评分失败')
            }
          })
      },
      end_question(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('question_id', value)
        that.axios({
          method: 'post',
          url: '/iasystem/end_question/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: '提交成功',
                type: 'success'
              })
              setTimeout(function () {
                that.$router.go(0)
              }.bind(that), 1000)
            } else if (res.data.code === 0) {
              that.$message.error('提交失败')
            }
          })
      },
      gotoForum(value) {
        this.$router.push({
          path: `/forum/topic/${value}`
        })
        //window.location.href = "http://127.0.0.1:8888/forum/topic/" + value
      }
    }
  }
</script>

<style scoped>

</style>
