<template>
  <div id="Search" style="margin-top: 0" v-loading="loading">
    <div class="Head_Container">
      <el-container>
        <el-main>
          <el-carousel :interval="4000" type="card" height="250px">
            <el-carousel-item v-for="item in imgUrls" :key="item">
              <img :src="item.src">
            </el-carousel-item>
          </el-carousel>
          <el-card class="box-card" style="height:auto;min-height:350px;width:98%;text-align: center;">
            <el-form label-width="80px" ref="search" :model="search" :rules="rules"
                     style="margin-top:20px;padding-top: 10px;padding-bottom: 10px">
              <el-row>
                <el-col :span="8">
                  <el-form-item label="专业" prop="major">
                    <el-select style="float: left" v-model="search.major" placeholder=""
                               filterable
                               @blur="selectBlur"
                               @change="getSubject">
                      <el-option label="不限" value="0"></el-option>
                      <el-option v-for="(item,index) in majorList" :key="index" :label="item.major_name"
                                 :value="item.major_id"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="科目" prop="type">
                    <el-select style="float: left" v-model="search.type" placeholder=""
                               filterable
                               @blur="selectBlur">
                      <el-option label="不限" value="0"></el-option>
                      <el-option v-for="(item,index) in subjectList" :key="index" :label="item.subject_name"
                                 :value="item.subject_id"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-divider></el-divider>
              <el-row>
                <el-col :span="14">
                  <el-form-item prop="keyword">
                    <el-input v-model="search.keyword" @keyup.enter.native="Search"
                              style="float:left;width:90%;margin-left:10px"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-form-item>
                    <el-button type="primary" icon="el-icon-search" style="float:left"
                               v-on:click="Search()">搜索
                    </el-button>
                  </el-form-item>
                </el-col>
                <el-col :span="4">
                  <el-form-item>
                    <el-button type="primary" style="float:left"
                               v-on:click="gotoForum()">前往论坛
                    </el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
            <el-tabs style="margin-top: 20px" v-model="activeName" type="border-card" @tab-click="handleClick">
              <el-tab-pane label="基本问题" name="first">
                <div v-if="base_questions.length==0" style="width:100%;height:200px">
                  <h1 style="margin-top: 50px">这里什么都没有哦</h1>
                </div>
                <div style="margin-top:20px;height: auto;width:100%;">
                  <el-card v-for="question in page_base_questions" class="box-card"
                           style="min-height:350px;width:90%;margin-left:5%;text-align: center;margin-top: 20px">
                    <el-row>
                      <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">
                        {{question.subject}}
                      </el-tag>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row>
                      <h4 style="float:left;margin-left:20px;width:80%">{{question.description}}</h4>
                    </el-row>
                    <el-row>
                      <p v-for="item in formatText(question.answer)"
                         style="float:left;margin-left:20px;margin-right:20px;text-align: left;width:auto;margin-top: 0;line-height: 20px">
                        {{item}}</p>
                    </el-row>
                  </el-card>
                  <el-row style="margin-top:20px" v-if="page_base_questions.length!=0">
                    <el-pagination
                      @size-change="handleSizeChange1"
                      @current-change="handleCurrentChange1"
                      :current-page="currentPage1"
                      :page-sizes="[2,3,4]"
                      :page-size="2"
                      layout="total, sizes, prev, pager, next, jumper"
                      :total="totalCount1">
                    </el-pagination>
                  </el-row>
                </div>
              </el-tab-pane>
              <el-tab-pane label="活跃问题" name="second">
                <div v-if="active_questions.length==0" style="width:100%;height:200px">
                  <h1 style="margin-top: 50px">这里什么都没有哦</h1>
                </div>
                <div style="margin-top:20px;height: auto;width:100%">
                  <el-card v-for="question in page_active_questions" :key="question.question_id" class="box-card"
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
                      <button v-if="question.status==0" style="float:right;margin-right:10px" type="button"
                              class="el-button el-button--mini el-button--info is-circle"><i
                        class="el-icon-close"></i>
                      </button>
                      <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                        {{question.score}}分
                      </el-tag>
                      <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">
                        {{question.subject}}
                      </el-tag>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row>
                      <p>{{question.context}}</p>
                    </el-row>
                    <el-row style="margin-top: 10px">
                      <el-button type="success" @click="question_Detail(question.question_id)"
                                 style="float:right;margin-right:3%">
                        更多回答
                      </el-button>
                    </el-row>
                    <el-divider></el-divider>
                    <div v-if="question.answer.score==null">
                      <p>暂无回答</p>
                    </div>
                    <div v-model="question.answer" v-if="question.answer.score!=null"
                         style="text-align: center;width: 100%">
                      <el-row>
                        <el-avatar :size="40" :src="get_avatar(question.answer.avatar)"
                                   style="float:left;margin-left:20px"></el-avatar>
                        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                          {{question.answer.username}}</p>
                        <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                          {{question.answer.score}}分
                        </el-tag>
                        <button v-if="question.answer.status==2" style="float:right;margin-right:10px" type="button"
                                class="el-button el-button--mini el-button--warning is-circle">
                          <i class="el-icon-star-off"></i>
                        </button>
                        <el-tag effect="dark" type="success" v-if="question.answer.from_forum==true"
                                style="float:right;margin-right:10px">
                          论坛信息
                        </el-tag>
                      </el-row>
                      <el-row style="margin-top: 20px">
                        <p v-for="item in formatText(question.answer.context)"
                           style="float:left;margin-left:20px;margin-right:20px;text-align: left;width:auto;margin-top: 0;line-height: 20px">
                          {{item}}</p>
                      </el-row>
                    </div>
                  </el-card>
                  <el-row style="margin-top:20px" v-if="page_active_questions.length!=0">
                    <el-pagination
                      @size-change="handleSizeChange2"
                      @current-change="handleCurrentChange2"
                      :current-page="currentPage2"
                      :page-sizes="[2,3,4]"
                      :page-size="2"
                      layout="total, sizes, prev, pager, next, jumper"
                      :total="totalCount2">
                    </el-pagination>
                  </el-row>
                </div>
              </el-tab-pane>
              <el-tab-pane label="相关资源" name="third">
                <div v-if="requests.length==0" style="width:100%;height:200px">
                  <h1 style="margin-top: 50px">这里什么都没有哦</h1>
                </div>
                <div style="margin-top:20px;height:auto;width:100%">
                  <el-card v-for="(sub_request,index) in page_requests" :key="index" class="box-card"
                           style="width:80%;margin-top:20px;margin-left:8%;padding-top:10px;padding-bottom:20px;text-align: center">
                    <el-row>
                      <el-avatar :size="40" :src="get_avatar(sub_request.avatar)"
                                 style="float:left;margin-left:20px"></el-avatar>
                      <p style="float:left;margin-left:20px;margin-top: 10px;line-height: 22px">
                        {{sub_request.username}}</p>
                      <p style="float:left;margin-left:20px;margin-top: 10px;line-height: 22px">
                        {{dateFormat(sub_request.stime)}} 至
                        {{dateFormat(sub_request.etime)}}</p>
                      <button v-if="sub_request.status==1" style="float:right;margin-right:10px" type="button"
                              class="el-button el-button--mini el-button--success is-circle"><i
                        class="el-icon-check"></i>
                      </button>
                      <button v-if="sub_request.status==0" style="float:right;margin-right:10px" type="button"
                              class="el-button el-button--mini el-button--info is-circle"><i
                        class="el-icon-close"></i>
                      </button>
                      <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                        {{sub_request.score}}分
                      </el-tag>
                      <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">
                        {{sub_request.subject}}
                      </el-tag>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row>
                      <p>{{sub_request.context}}</p>
                    </el-row>
                    <el-row style="margin-top: 10px">
                      <el-button type="success" @click="request_Detail(sub_request.request_id)"
                                 style="float:right;margin-right:3%">
                        更多资源
                      </el-button>
                    </el-row>
                    <el-divider></el-divider>
                    <div v-if="sub_request.resource.score==null">
                      <p>暂无回答</p>
                    </div>
                    <div v-model="sub_request.resource" v-if="sub_request.resource.score!=null"
                         style="text-align: center;width: 100%">
                      <el-row>
                        <el-avatar :size="40" :src="get_avatar(sub_request.resource.avatar)"
                                   style="float:left;margin-left:20px"></el-avatar>
                        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                          {{sub_request.resource.username}}</p>
                        <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                          {{sub_request.resource.score}}分
                        </el-tag>
                        <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">
                          {{sub_request.resource.number}}次
                        </el-tag>
                      </el-row>
                      <el-row style="text-align:center;margin-top: 15px">
                        <el-col :span="18">
                          <label style="font-size:18px">{{getfileName(sub_request.resource.location)}}</label>
                        </el-col>
                        <el-col :span="6">
                          <a class="download"
                             :href="download(sub_request.resource.resource_id,getfileName(sub_request.resource.location))">下载</a>
                        </el-col>
                      </el-row>
                    </div>
                  </el-card>
                  <el-row style="margin-top:20px" v-if="page_requests.length!=0">
                    <el-pagination
                      @size-change="handleSizeChange3"
                      @current-change="handleCurrentChange3"
                      :current-page="currentPage3"
                      :page-sizes="[2,3,4]"
                      :page-size="2"
                      layout="total, sizes, prev, pager, next, jumper"
                      :total="totalCount3">
                    </el-pagination>
                  </el-row>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
  export default {
    name: " Search",
    data() {
      return {
        search: {
          major: '0',
          type: '0',
          keyword: '',
        },
        username: '',
        currentPage1: 1,
        pageSize1: 2,
        totalCount1: '',
        currentPage2: 1,
        pageSize2: 2,
        totalCount2: '',
        currentPage3: 1,
        pageSize3: 2,
        totalCount3: '',
        loading: false,
        activeName: 'first',
        base_questions: [],
        active_questions: [],
        requests: [],
        page_base_questions: [],
        page_active_questions: [],
        page_requests: [],
        majorList: [],
        subjectList: [],
        multipleSelection: [],
        imgUrls: [
          {
            src: require("../assets/IAsystem/1.jpg"),
          },
          {
            src: require("../assets/IAsystem/2.jpg"),
          },
          {
            src: require("../assets/IAsystem/3.jpg"),
          },
          {
            src: require("../assets/IAsystem/4.jpg"),
          },
          {
            src: require("../assets/IAsystem/5.jpg"),
          },
          {
            src: require("../assets/IAsystem/6.jpg"),
          },
        ],
        rules: {
          major: [
            {
              required: true,
              message: '请选择所属专业',
              trigger: 'change'
            }
          ],
          type: [
            {
              required: true,
              message: '请选择所属科目',
              trigger: 'change'
            }
          ],
          keyword: [
            {
              required: true,
              message: '请输入搜索内容',
              trigger: 'change'
            },
            {
              min: 3, max: 20, message: '长度在 3 到 20 个字符'
            }
          ]
        }
      }
    },
    mounted() {
      this.getMajor()
    },
    methods: {
      handleClick(tab, event) {
      },
      Search() {
        let that = this
        let param = new URLSearchParams()
        param.append('keyword', that.search.keyword)
        param.append('type', that.search.type)
        that.loading = true
        that.axios.post('/iasystem/search/', param)
          .then(function (res) {
            if (res.data.code === 1) {
              that.base_questions = res.data.base_questions
              that.active_questions = res.data.active_questions
              that.requests = res.data.requests
              that.totalCount1 = res.data.base_questions.length
              that.totalCount2 = res.data.active_questions.length
              that.totalCount3 = res.data.requests.length
              that.get_page_base_question()
              that.get_page_active_question()
              that.get_page_request()
              that.loading = false
              if (that.base_questions.length == 0 && that.active_questions.length == 0 && that.requests.length == 0) {
                that.$message({
                  message: "没有符合条件的结果",
                  type: "info"
                });
              } else {
                that.$message({
                  message: "查询成功",
                  type: "success"
                });
              }
            } else {
              that.loading = false
              that.$message.error('查询失败')
            }
          })
      },
      handleSizeChange1(val) {
        this.pageSize1 = val;
        this.get_page_base_question()
      },
      handleCurrentChange1(val) {
        this.currentPage1 = val;
        this.get_page_base_question()
      },
      handleSizeChange2(val) {
        this.pageSize2 = val;
        this.get_page_active_question()
      },
      handleCurrentChange2(val) {
        this.currentPage2 = val;
        this.get_page_active_question()
      },
      handleSizeChange3(val) {
        this.pageSize3 = val;
        this.get_page_request()
      },
      handleCurrentChange3(val) {
        this.currentPage3 = val;
        this.get_page_request()
      },
      getMajor() {
        let that = this
        that.$http.get('/iasystem/majors/')
          .then(function (res) {
            if (res.data.code === 1) {
              that.majorList = res.data.majors
              that.username = that.$cookies.get('username')
            } else if (res.data.code === 0) {
              that.$message.error('查询专业失败')
            }
          })
      },
      get_page_base_question() {
        this.page_base_questions = [];
        for (let i = (this.currentPage1 - 1) * this.pageSize1; i < this.totalCount1; i++) {
          this.page_base_questions.push(this.base_questions[i])
          if (this.page_base_questions.length == this.pageSize1) break;
        }
      },
      get_page_active_question() {
        this.page_active_questions = [];
        for (let i = (this.currentPage2 - 1) * this.pageSize2; i < this.totalCount2; i++) {
          this.page_active_questions.push(this.active_questions[i])
          if (this.page_active_questions.length == this.pageSize2) break;
        }
      },
      get_page_request() {
        this.page_requests = [];
        for (let i = (this.currentPage3 - 1) * this.pageSize3; i < this.totalCount3; i++) {
          this.page_requests.push(this.requests[i])
          if (this.page_requests.length == this.pageSize3) break;
        }
      },
      getSubject(value) {
        let that = this
        if (that.search.major === '0') {
          that.$http.get('/iasystem/subjects/')
            .then(function (res) {
              if (res.data.code === 1) {
                that.subjectList = res.data.subjects
              } else if (res.data.code === 0) {
                that.$message.error('查询课程失败')
              }
            })
        } else {
          that.subjectList = that.majorList[value - 1].subjectList
        }
      },
      formatText(value) {
        return String(value).split('\n')
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      get_avatar(value) {
        return "data:image/jpeg;base64," + value
      },
      download(value1, value2) {
        return "/iasystem/download/" + value1 + "/" + value2
      },
      getfileName(value) {
        let length1 = value.toString().length
        let temp = value.toString().substring(value.toString().lastIndexOf('/') + 1, length1)
        let length2 = temp.length
        let index = temp.indexOf('.')
        return temp.substring(0, index - 32) + temp.substring(index, length2)
      },
      selectBlur(e) {
        this.type = e.target.value
      },
      gotoForum() {
        window.location.href = "http://127.0.0.1:8888/forum"
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
    }
  }
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }

  .Head_Container {
    overflow-x: hidden;
  }

  .download {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #409EFF;
    background-color: #ECF5FF;
    border-color: #B3D8FF;
    font-size: 12px;
  }

  .download:hover {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #FFFFFF;
    background-color: #409EFF;
    border-color: #409EFF;
    font-size: 12px;
  }
</style>
