<template>
  <div id="ReleaseHall" v-loading="loading">
    <p style="font-size:20px;font-weight:bold;margin-top:25px">
      热门发布
    </p>
    <el-divider></el-divider>
    <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick" style="min-height: 500px">
      <el-tab-pane label="问题" name="first">
        <div style="margin-top:20px;height: auto;min-height:500px;width:100%">
          <el-card v-for="question in page_questions" :key="question.question_id" class="box-card"
                   style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;text-align: center">
            <el-row>
              <el-avatar :size="40" :src="get_avatar(question.avatar)"
                         style="float:left;margin-left:20px"></el-avatar>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{question.username}}</p>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{dateFormat(question.stime)}} 至
                {{dateFormat(question.etime)}}</p>
              <button v-if="question.status==1" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--success is-circle"><i
                class="el-icon-check"></i>
              </button>
              <button v-if="question.status==2" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--primary is-circle"><i
                class="el-icon-edit"></i>
              </button>
              <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">{{question.score}}分
              </el-tag>
              <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{question.subject}}
              </el-tag>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <p>{{question.context}}</p>
            </el-row>
            <el-row>
              <el-button type="primary" @click="question_Detail(question.question_id)"
                         style="float: right;margin-right: 60px">查看详情
              </el-button>
            </el-row>
          </el-card>
          <el-row style="margin-top:20px" v-if="page_questions.length!=0">
            <el-pagination
              @size-change="handleSizeChange1"
              @current-change="handleCurrentChange1"
              :current-page="currentPage1"
              :page-sizes="[3,4,5]"
              :page-size="3"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalCount1">
            </el-pagination>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="需求" name="second">
        <div style="margin-top:20px;height: auto;min-height:500px;width:100%">
          <el-card v-for="sub_request in page_requests" :key="sub_request.request_id" class="box-card"
                   style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;text-align: center">
            <el-row>
              <el-avatar :size="40" :src="get_avatar(sub_request.avatar)"
                         style="float:left;margin-left:20px"></el-avatar>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{sub_request.username}}</p>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{dateFormat(sub_request.stime)}} 至
                {{dateFormat(sub_request.etime)}}</p>
              <button style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--success is-circle"><i class="el-icon-check"></i>
              </button>
              <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">{{sub_request.score}}分
              </el-tag>
              <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{sub_request.subject}}
              </el-tag>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <p>{{sub_request.context}}</p>
            </el-row>
            <el-row>
              <el-button type="primary" @click="request_Detail(sub_request.request_id)"
                         style="float: right;margin-right: 60px">
                查看详情
              </el-button>
            </el-row>
          </el-card>
          <el-row style="margin-top:20px" v-if="page_requests.length!=0">
            <el-pagination
              @size-change="handleSizeChange2"
              @current-change="handleCurrentChange2"
              :current-page="currentPage2"
              :page-sizes="[3,4,5]"
              :page-size="3"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalCount2">
            </el-pagination>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="问题填充" name="third" v-if="this.$cookies.get('type')==='T'">
        <div v-if="store_questions.length==0" style="width:100%;height:200px">
          <h1 style="margin-top: 50px">这里什么都没有哦</h1>
        </div>
        <div style="margin-top:20px;height: auto;width:100%">
          <el-card v-for="question in ps_questions" class="box-card"
                   style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;text-align: center">
            <el-row>
              <el-avatar :size="40" src="iasystem/avatar/" style="float:left;margin-left:20px"></el-avatar>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">{{username}}</p>
              <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                {{dateFormat(question.stime)}} 至
                {{dateFormat(question.etime)}}</p>
              <button v-if="question.status==1" style="float:right;margin-right:10px" type="button"
                      class="el-button el-button--mini el-button--success is-circle"><i
                class="el-icon-check"></i>
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
              <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{question.subject}}
              </el-tag>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <p>{{question.context}}</p>
            </el-row>
            <el-collapse @change="handleChange" style="margin-top: 20px">
              <el-collapse-item title="自主回答" name="1">
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
                    <el-button type="success" @click="submit_base(question.question_id)"
                               style="margin-left: 35%">提交
                    </el-button>
                    <el-button type="info" @click="cancel_answer()">取消</el-button>
                  </el-form-item>
                </el-form>
              </el-collapse-item>
              <el-collapse-item title="展开回答" name="2">
                <div class="infinite-list-wrapper"
                     style="overflow-y:scroll;margin-top:20px;height: auto;width:100%">
                  <ul
                    class="list"
                    style="list-style: none">
                    <li v-for="answer in question.answers" class="list-item">
                      <el-card class="box-card"
                               style="width:90%;margin-left:5%;text-align: center;margin-top: 20px">
                        <el-row>
                          <el-avatar :size="40" :src="get_avatar(answer.avatar)"
                                     style="float:left;margin-left:20px"></el-avatar>
                          <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                            {{answer.username}}</p>
                          <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                            {{dateFormat(answer.time)}}</p>
                          <el-tag effect="light" type="primary" style="float: right;margin-right: 10px">
                            {{answer.score}}分
                          </el-tag>
                          <el-tag effect="dark" type="success" v-if="answer.status==1"
                                  style="float:right;margin-right:10px">
                            论坛信息
                          </el-tag>
                        </el-row>
                        <el-divider></el-divider>
                        <el-row>
                          <p style="float:left;margin-left:20px;text-align: left">
                            {{answer.context}}</p>
                        </el-row>
                        <el-row>
                          <el-button type="success" @click="accept_answer(question.question_id,answer.answer_id)"
                                     style="float:right;margin-right: 30px">推荐
                          </el-button>
                        </el-row>
                      </el-card>
                    </li>
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-card>
           <el-row style="margin-top:20px" v-if="ps_questions.length!=0">
                    <el-pagination
                      @size-change="handleSizeChange3"
                      @current-change="handleCurrentChange3"
                      :current-page="currentPage3"
                      :page-sizes="[3,4,5]"
                      :page-size="3"
                      layout="total, sizes, prev, pager, next, jumper"
                      :total="totalCount3">
                    </el-pagination>
                  </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  export default {
    name: "ReleaseHall",
    data() {
      return {
        loading: true,
        username: '',
        activeName: 'first',
        activeIndex: '2',
        currentPage1: 1,
        pageSize1: 3,
        totalCount1: '',
        currentPage2: 1,
        pageSize2: 3,
        totalCount2: '',
        currentPage3: 1,
        pageSize3: 3,
        totalCount3: '',
        answer_context: '',
        requests: [],
        page_requests: [],
        questions: [],
        page_questions: [],
        store_questions: [],
        ps_questions: [],
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
      this.get_hot_requests()
      this.get_store_questions()
    },
    methods: {
      handleChange(value) {
      },
      handleClick(tab, event) {
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      get_avatar(value) {
        return "data:image/jpeg;base64," + value
      },
      handleSizeChange1(val) {
        this.pageSize1 = val;
        this.get_page_question()
      },
      handleCurrentChange1(val) {
        this.currentPage1 = val;
        this.get_page_question()
      },
      handleSizeChange2(val) {
        this.pageSize2 = val;
        this.get_page_request()
      },
      handleCurrentChange2(val) {
        this.currentPage2 = val;
        this.get_page_request()
      },
      handleSizeChange3(val) {
        this.pageSize3 = val;
        this.get_page_store_question()
      },
      handleCurrentChange3(val) {
        this.currentPage3 = val;
        this.get_page_store_question()
      },
      get_hot_requests() {
        let that = this
        that.axios({
          method: 'post',
          url: '/iasystem/get_hot_requests/'
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.requests = res.data.requests
              that.questions = res.data.questions
              that.totalCount1 = res.data.questions.length
              that.totalCount2 = res.data.requests.length
              that.get_page_question()
              that.get_page_request()
              that.username = that.$cookies.get('username')
              that.loading = false
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询失败')

            }
          })
      },
      get_store_questions() {
        let that = this
        that.axios({
          method: 'post',
          url: '/iasystem/get_store_questions/'
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.store_questions = res.data.store_questions
              that.totalCount3 = res.data.store_questions.length
              that.get_page_store_question()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_page_question() {
        this.page_questions = [];
        for (let i = (this.currentPage1 - 1) * this.pageSize1; i < this.totalCount1; i++) {
          this.page_questions.push(this.questions[i])
          if (this.page_questions.length == this.pageSize1) break;
        }
      },
      get_page_request() {
        this.page_requests = [];
        for (let i = (this.currentPage2 - 1) * this.pageSize2; i < this.totalCount2; i++) {
          this.page_requests.push(this.requests[i])
          if (this.page_requests.length == this.pageSize2) break;
        }
      },
      get_page_store_question() {
        this.ps_questions = [];
        for (let i = (this.currentPage3 - 1) * this.pageSize3; i < this.totalCount3; i++) {
          this.ps_questions.push(this.store_questions[i])
          if (this.ps_questions.length == this.pageSize3) break;
        }
      },
      question_Detail(value) {
        this.$router.push({
          path: `/Question/${value}`,
        })
      },
      request_Detail(value) {
        this.$router.push({
          path: `/Request/${value}`,
        })
      },
      accept_answer(value1, value2) {
        let that = this
        let param = new URLSearchParams()
        param.append('question_id', value1)
        param.append('answer_id', value2)
        that.axios({
          method: 'post',
          url: '/iasystem/accept_answer/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: "上传成功",
                type: "success"
              })
            } else if (res.data.code === 0) {
              that.$message.error('上传失败')
            }
          })
      },
      submit_base(value) {
        let that = this
        that.loading = true
        let param = new URLSearchParams()
        param.append('question_id', value)
        param.append('answer', that.answer_context)
        that.axios({
          method: 'post',
          url: '/iasystem/submit_base/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: "上传成功",
                type: "success"
              })
            } else if (res.data.code === 0) {
              that.$message.error('上传失败')
            }
            setTimeout(function () {
              that.$router.go(0)
              that.loading = false
            }.bind(that), 1000)
          })
      },
      cancel_answer() {
        this.answer_context = ''
        this.activeIndex = ''
      },
    }
  }
</script>

<style scoped>

</style>
