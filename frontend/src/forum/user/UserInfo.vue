<template>
     <div class="info">


       <div class="userInfo">
         <h2>个人信息</h2>

         <el-form ref="userinfo" :model="userinfo" label-width="90px">
           <el-form-item readonly="true" label="用户名">
             <span>{{userinfo.username}}</span>
           </el-form-item>
           <el-form-item readonly="true" label="我的贡献度">
             <span>{{userinfo.user_credit}}</span>
           </el-form-item>
           <el-form-item label="教育背景">
             <el-input v-model="userinfo.user_edu">{{userinfo.user_edu}}</el-input>
           </el-form-item>
           <el-form-item label="地址">
             <el-input v-model="userinfo.user_addr">{{userinfo.user_addr}}</el-input>
           </el-form-item>
           <el-form-item label="手机号">
             <el-input v-model="userinfo.user_tel">{{userinfo.user_tel}}</el-input>
           </el-form-item>
           <el-form-item>
             <el-button type="primary" @click="updateInfo()">更新</el-button>
           </el-form-item>
         </el-form>
       </div>

       <div class="avatar">
         <h2>我的头像</h2>
         <img :src="'http://127.0.0.1:8888/media/' + userinfo.avatar_url" width="120" height="120"/>
         <br>
         <input type="file" id="uploadImage" accept="image/jpeg,image/jpg,image/png"/>
         <br><br>
         <el-button type="primary" size="mini" @click="onSubmitImg()">上传</el-button>
       </div>

    </div>




</template>

<script>
    export default {
      name: "UserInfo",
      data() {
        return {
          user: window.localStorage.getItem('username'),
          userinfo:{},
          fileList: [],

        }
      },
      created(){
        this.getUserInfo();
      },
      methods: {
        getUserInfo() {
          console.log('name', this.user)
          this.axios.get('/forum/userinfo',{
            params: {
              user: this.user,
            }
          })
            .then((response) => {
              if (response.data.status === 0) {
                console.log('userinfo', response)
                this.userinfo = response.data.data
              }

            })
            .catch((error) => {
              console.error('获取用户信息异常', error)
            })
        },
        updateInfo(){
          const data = this.userinfo
          this.axios.post('/forum/updateUserInfo',{
            user_edu: data.user_edu,
            user_addr: data.user_addr,
            user_tel: data.user_tel
          }) .then(response => {
            if (response.data.status === 0) {
              this.getUserInfo();
              this.$message({
                showClose: true,
                message: response.data.message,
                type: response.success === 0 ? 'success' : 'error',
                duration: 2000
              })
            } else {
              this.$message({
                showClose: true,
                message: response.data.message,
                type: response.success === 0 ? 'success' : 'error',
                duration: 2000
              })
            }
          })

        },
        onSubmitImg() {
          var data = new FormData();
          var img = document.getElementById('uploadImage').files[0];
          data.append('file',img,img.name);
          let headers = {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
          this.axios.post("/forum/updateUserAvatar", data, headers)
            .then(response => {
              if (response.data.status === 0) {
                this.getUserInfo();
                this.$message({
                  showClose: true,
                  message: response.data.message,
                  type: response.success === 0 ? 'success' : 'error',
                  duration: 2000
                })
              } else {
                this.$message({
                  showClose: true,
                  message: response.data.message,
                  type: response.success === 0 ? 'success' : 'error',
                  duration: 2000
                })
              }
            })
        },
      }
    }

</script>

<style scoped lang="scss">
  .info{
    display: flex;
    .userInfo{
      width: 50%;
    }
    .avatar{
      margin-left: 10%;
      width: 50%;

    }

  }
</style>
