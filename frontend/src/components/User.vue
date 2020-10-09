<template>
  <div id="user" class="demo-block demo-zh-CN demo-form" style="width:70%;margin-top: 15px;margin-left: 15%;padding-bottom: 15px"
       v-loading="loading">
    <el-card class="box-card" style="width:100%;text-align: center">
      <p style="font-size:20px;font-weight:bold">
        个人中心
      </p>
      <div class="avatar_border">
        <div class="avatar_left">
          <img src="api/avatar/" class="avatar" id="user_avatar">
        </div>
        <div class="avatar_right">
          <el-upload
            style="margin-top:55px"
            class="upload-demo"
            ref="upload"
            action="api/avatarUpload/"
            accept="image/jpeg,image/png,image/jpg"
            :before-upload="beforeAvatarUpload"
            :auto-upload="false"
            :file-list="fileList"
            :on-success="uploadSuccess"
            list-type="picture"
            :limit="1">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传头像</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过2M</div>
          </el-upload>
        </div>
      </div>
      <el-form ref="user" :model="user" :rules="rule" label-width="80px" style="margin-left:10%;margin-top:40px;width:80%">
        <el-form-item label="用户名" prop="username" style="margin-top: 20px">
          <el-input v-model="user.username"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="性别" prop="user_gender">
              <el-select style="float: left" v-model="user.user_gender">
                <el-option label="女" value="F"></el-option>
                <el-option label="男" value="M"></el-option>
                <el-option label="保密" value="D"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生日" prop="user_bir">
              <el-date-picker v-model="user.user_bir" value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="学历" prop="user_edu">
          <el-input v-model="user.user_edu"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="user_addr">
          <el-input v-model="user.user_addr"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="user.email"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="user_tel">
          <el-input v-model="user.user_tel"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="身份">
              <el-label style="float:left;margin-left:25px" v-if="user.type==='T'">老师</el-label>
              <el-label style="float:left;margin-left:25px" v-if="user.type==='S'">学生</el-label>
              <el-label style="float:left;margin-left:25px" v-if="user.type==='A'">管理员</el-label>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户状态">
              <button style="float:left;margin-left:25px" v-if="user.is_active===true" type="button"
                      class="el-button el-button--small el-button--success is-circle"><i class="el-icon-check"></i>
              </button>
              <button style="float:left;margin-left:25px" v-if="user.is_active===false" type="button"
                      class="el-button el-button--small el-button--danger is-circle"><i class="el-icon-close"></i>
              </button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row style="margin-top:20px;text-align: center;margin-bottom: 20px">
          <el-button type="primary" round @click="ChangePassword()">修改密码</el-button>
          <el-button type="success" round @click="onSubmit('user')">修改信息</el-button>
          <el-button type="danger" round @click="home()">返回主页</el-button>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "User",
    data() {
      const checkPhone = (rule, value, callback) => {
        const phoneReg = /^1[3|4|5|7|8][0-9]{9}$/
        setTimeout(() => {
          if (!Number.isInteger(+value)) {
            callback(new Error('请输入数字值'))
          } else {
            if (phoneReg.test(value)) {
              callback()
            } else if (!value) {
              callback()
            } else {
              callback(new Error('电话号码格式不正确'))
            }
          }
        }, 100)
      }
      const checkEmail = (rule, value, callback) => {
        const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
        if (!value) {
          return callback(new Error('邮箱不能为空'))
        }
        setTimeout(() => {
          if (mailReg.test(value)) {
            callback()
          } else {
            callback(new Error('请输入正确的邮箱格式'))
          }
        }, 100)
      }
      return {
        loading: true,
        new_imgUrl: '',
        imgUrl: '',
        gender: '',
        user: [],
        fileList: [],
        rule: {
          username: [
            {
              required: true,
              message: '请输入用户名',
              trigger: 'change'
            }
          ],
          user_gender: [
            {
              required: true,
              trigger: 'change'
            }
          ],
          user_bir: [
            {
              trigger: 'change'
            }
          ],
          user_edu: [
            {
              trigger: 'change'
            }
          ],
          user_addr: [
            {
              trigger: 'change'
            }
          ],
          email: [
            {
              required: true,
              validator: checkEmail,
              trigger: 'change'
            }
          ],
          user_tel: [
            {
              validator: checkPhone,
              trigger: 'blur'
            }
          ],

        },
      }
    },
    mounted: function () {
      if (this.$cookies.get('user_id')) {
        this.getUser()
      } else {
       this.$router.push('/Login')
      }
    },
    methods: {
      getUser() {
        let that = this
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        that.axios({
          method: 'post',
          url: '/api/user/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.user = res.data.user[0]
              console.log(that.user)
              that.loading = false
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
              console.log(res.data.msg)
            }
          })
      },
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.updateInfo()
          } else {
            that.$message('请注意输入格式')
            return false;
          }
        });
      },
      updateInfo() {
        let that = this
        let param = new URLSearchParams()
        let user_id = that.$cookies.get('user_id')
        param.append('user_id', user_id)
        param.append('new_username', that.user.username)
        param.append('new_gender', that.user.user_gender)
        param.append('new_birthday', that.user.user_bir)
        param.append('new_education', that.user.user_edu)
        param.append('new_address', that.user.user_addr)
        param.append('new_email', that.user.email)
        param.append('new_telephone', that.user.user_tel)
        that.axios({
          method: 'post',
          url: '/api/update_info/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message({
                message: res.data.msg,
                type: 'success'
              })
              that.getUser()
            } else if (res.data.code === 0) {
              that.$message.error('修改失败')
            }
          })
      },
      home() {
        this.$router.push('/Home')
      },
      ChangePassword() {
        this.$router.push('/Password')
      },
      //上传时，判断文件的类型及大小是否符合规则
      beforeAvatarUpload(file) {
        const isJPG = file.type == 'image/jpeg' || file.type == 'image/png'
        const isLt2M = file.size / 1024 / 1024 < 2
        if (!isJPG) {
          this.$message.warning('上传头像图片只能是 JPG/PNG 格式!')
          return isJPG
        }
        if (!isLt2M) {
          this.$message.warning('上传头像图片大小不能超过 2MB!')
          return isLt2M
        }
        return isJPG && isLt2M
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

    }
  }
</script>

<style scoped>
  .avatar {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    display: block;
  }

  .avatar_border {
    margin-top: 25px;
    margin-left: 10%;
    width: 80%;
    height: 180px;
  }

  .avatar_left {
    height: 100%;
    margin-left: 45px;
    float: left;
    display: block;
  }

  .avatar_right {
    width: 360px;
    float: left;
    margin-left: 30px;
    display: block;
  }
</style>
