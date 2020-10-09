<template>
  <div id="request" v-loading="loading">
    <el-card class="box-card"
             style="width:80%;margin-top:50px;margin-left:8%;min-height:600px;padding-top:10px;text-align: center">
      <el-row>
        <el-avatar :size="40" :src="avatar"
                   style="float:left;margin-left:20px"></el-avatar>
        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
          {{sub_request.username}}</p>
        <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">{{dateFormat(sub_request.stime)}} 至
          {{dateFormat(sub_request.etime)}}</p>
        <button v-if="sub_request.status==1" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--success is-circle"><i
          class="el-icon-check"></i>
        </button>
        <button v-if="sub_request.status==0" style="float:right;margin-right:10px" type="button"
                class="el-button el-button--mini el-button--info is-circle"><i
          class="el-icon-close"></i>
        </button>
        <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">{{sub_request.score}}分
        </el-tag>
        <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">{{sub_request.subject}}</el-tag>
      </el-row>
      <el-divider></el-divider>
      <el-row>
        <p>{{sub_request.context}}</p>
      </el-row>
      <el-collapse v-model="activeIndex" style="margin-top: 20px">
        <el-collapse-item v-if="sub_request.username!=username&&sub_request.status>0" title="提供资源" name="1">
          <el-upload
            style="margin-top:20px;"
            class="upload-demo"
            ref="upload"
            :data="info"
            action="iasystem/uploadFiles/"
            :on-change="handleChange"
            :before-upload="beforeFileUpload"
            :auto-upload="false"
            :file-list="fileList"
            :on-success="uploadSuccess"
            multiple
            :limit="5">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传文件</el-button>
          </el-upload>
        </el-collapse-item>
        <el-collapse-item title="展开回答" name="2">
          <div v-if="sub_request.resources.length==0" style="width:100%;height:200px">
            <h1 style="margin-top: 50px">这里什么都没有哦</h1>
          </div>
          <div class="infinite-list-wrapper"
               style="overflow-y:scroll;margin-top:20px;height: auto;width:100%">
            <ul
              class="list"
              style="list-style: none">
              <li v-for="resource in sub_request.resources" :key="resource.resource_id" class="list-item">
                <el-card class="box-card"
                         style="width:90%;margin-left:5%;text-align: center;margin-top: 20px">
                  <el-row>
                    <el-avatar :size="40" :src="get_avatar(resource.avatar)"
                               style="float:left;margin-left:20px"></el-avatar>
                    <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                      {{resource.username}}</p>
                    <p style="float:left;margin-left:20px;margin-top: 10px;line-height:22px">
                      {{dateFormat(resource.time)}}</p>
                    <el-tag effect="dark" type="primary" style="float: right;margin-right: 10px">
                      {{resource.score}}分
                    </el-tag>
                    <el-tag effect="dark" type="success" style="float: right;margin-right: 10px">
                      下载{{resource.number}}次
                    </el-tag>
                  </el-row>
                  <el-divider></el-divider>
                  <el-row style="text-align:center;">
                    <el-col :span="18">
                      <label style="font-size:18px">{{getfileName(resource.location)}}</label>
                    </el-col>
                    <el-col :span="6">
                      <a :href="download(resource.resource_id,getfileName(resource.location))">下载</a>
                    </el-col>
                  </el-row>
                  <el-form v-if="resource.score==0&&sub_request.username==username" :rules="rule" label-width="80px"
                           style="text-align:center;margin-top:20px;margin-left:15px;padding-top: 10px;padding-bottom: 10px">
                    <el-form-item label="评分" prop="resource_score">
                      <el-col :span="12">
                        <el-input-number v-model="resource_score" @change="handleChange1" :min="1"
                                         :max="sub_request.score"></el-input-number>
                      </el-col>
                      <el-col :span="8">
                        <el-button type="success" @click="rate_resource(resource.resource_id)"
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
    name: "Request",
    data() {
      return {
        loading: true,
        activeIndex: '2',
        resource_score: '',
        deadline: '',
        avatar: '',
        sub_request: [],
        username: '',
        fileList: [],
        info: {
          request_id: '',
        },
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          }
        },
      }
    },
    mounted() {
      this.get_request(this.$route.params.request_id)
    },
    methods: {
       handleChange1(value) {
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
      rate_resource(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('resource_id', value)
        param.append('score', that.resource_score)
        that.axios({
          method: 'post',
          url: '/iasystem/rate_resource/',
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
      get_avatar(value) {
        return "data:image/jpeg;base64," + value
      },
      get_request(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('request_id', value)
        that.axios({
          method: 'post',
          url: '/iasystem/get_request/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.sub_request = res.data.sub_request
              that.avatar = that.get_avatar(that.sub_request.avatar)
              that.username = that.$cookies.get('username')
              that.loading = false
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询失败')
            }
          })
      },
      beforeFileUpload(file, fileList) {
        if (this.$cookies.get('user_id')) {
          const that = this
          that.info.request_id = that.sub_request.request_id
        } else {
          this.$router.push('/Login')
        }
      },
      handleChange(file, fileList) {
        this.fileList = fileList
      },
      uploadSuccess(response, file, fileList) {
        if (response.code == 1) {
          this.$message({message: '上传成功!', type: 'success'});
          setTimeout(function () {
            this.$router.go(0)
          }.bind(this), 1000)
        }
      },
      submitUpload() {
        this.$refs.upload.submit();
      },
      download(value1, value2) {
        return "/iasystem/download/" + value1 + "/" + value2
      },
      getfileName(value) {
        let length1 = value.toLocaleString().length
        let temp = value.toLocaleString().substring(value.toLocaleString().lastIndexOf('/') + 1, length1)
        let length2 = temp.length
        let index = temp.indexOf('.')
        return temp.substring(0, index - 32) + temp.substring(index, length2)
      },
      activate_request(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('request_id', value)
        param.append('time', that.dateConversion(that.deadline))
        that.axios({
          method: 'post',
          url: '/iasystem/activate_request/',
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
    }
  }
</script>

<style scoped>
  a {
    margin-left: 15px;
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

  a:hover {
    margin-left: 15px;
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
