/* eslint-disable */
<template>
  <div>
    <el-container
      style=" position:absolute; left:0; top:0; width:100%; height:100%; bottom: 0; border: 1px solid #eee">
      <el-aside width="250px" >
        <div style="text-align: center">
          <el-image src="/static/logo.png"
               style="width: 150px; height: 100px"/>
        </div>
        <el-menu
          :default-openeds="['2']"
          :default-active="$route.path"
          background-color="#fafafa"
          active-text-color="white"
          router>
          <el-menu-item index="/Teacher/Course_Work">
            <template slot="title"><i class="el-icon-reading"></i>课程-作业管理</template>
          </el-menu-item>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-document"></i>共享区管理</template>
            <el-menu-item-group>
              <el-menu-item
                index="/Teacher/TMaterial">共享资料</el-menu-item>
              <el-menu-item
                index="/Teacher/TGoodWork">优秀作业</el-menu-item>
            </el-menu-item-group>
          </el-submenu>


        </el-menu>
      </el-aside>
      <el-container>
        <el-header height="64px">
          <el-row>
            <el-col :span="12" style="text-align: left">
              <div class="grid-content bg-purple-dark">
                <span class="login-title1">在线教育平台作业系统</span>
                <span class="login-title">教师端</span>
              </div></el-col>

            <el-col :span="12" style="text-align: right;">
              <span>{{greet}}</span>
              <el-dropdown trigger="click" >
                <span class="el-dropdown-link">
                  {{user}}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item
                    icon="el-icon-setting"
                    @click.native="Setting()">更换头像</el-dropdown-item>
                  <el-dropdown-item
                    icon="el-icon-unlock"
                    @click.native="dialogVisible=true">修改密码</el-dropdown-item>
                  <el-dropdown-item
                    icon="el-icon-switch-button"
                    @click.native="goBack()">退出系统</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
              <span class="bt-registered" @click="goBack()" >退出</span>
            </el-col>
          </el-row>
        </el-header>
        <router-view/>
      </el-container>
    </el-container>

    <!-- 修改密码弹窗-->
    <el-dialog
      title="修改密码"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form
        :rules="changeDialogRules"
        ref="changeDialog"
        :model="changeDialog"
        label-position="right"
        show-message>
        <el-form-item label="旧密码：" prop="oldPsd">
          <el-col :span="20">
            <el-input
              prefix-icon="el-icon-lock"
              type="password"
              v-model="changeDialog.oldPsd"
              show-password></el-input>
          </el-col>
        </el-form-item>

        <el-form-item label="新密码：" prop="newPsd">
          <el-col :span="20">
            <el-input
              prefix-icon="el-icon-lock"
              type="password"
              v-model="changeDialog.newPsd"
              show-password></el-input>
          </el-col>
        </el-form-item>

        <el-form-item label="确认新密码：" prop="dnewPsd">
          <el-col :span="20">
            <el-input
              prefix-icon="el-icon-lock"
              type="password"
              v-model="changeDialog.dnewPsd"
              show-password></el-input>
          </el-col>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="ChangePsd('changeDialog')">确 定</el-button>
            </span>
    </el-dialog>

  </div>
</template>

<script>
    export default {
      data() {
        return {
          greet:'',
          user: '',
          dialogVisible: false,
          changeDialog: {
            oldPsd: '',
            newPsd: '',
            dnewPsd: '',
          },
          changeDialogRules: {
            oldPsd: [
              {required: true, message: '旧密码不可为空！', trigger: 'blur'}
            ],
            newPsd: [
              {required: true, message: '新密码不可为空！', trigger: 'blur'}
            ],
            dnewPsd: [
              {required: true, message: '新密码不可为空！', trigger: 'blur'}
            ]
          },

          workData: [],
        }
      },
      methods:{
        handleClose(done) {
          this.$confirm('确认关闭？')
            .then(_ => {
              done();
            })
            .catch(_ => {});
        },
        goBack(){
          this.$confirm('是否返回登录界面?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            console.log('go back');
            //this.$router.push({path:'/'})
            window.location.href="http://127.0.0.1:8888/#/Home"
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '取消'
            });
          });
        },
      },

      mounted() {
        this.user=this.$cookies.get('username');
        let myDate = new Date();
        let h=myDate.getHours();
        if(h>=3&&h<8)
          this.greet = '早上好，';
        else if(h>=8&&h<11)
          this.greet = '上午好，';
        else if(h>=11&&h<13)
          this.greet = '中午好，';
        else if(h>=13&&h<17)
          this.greet = '下午好，';
        else if(h>=17&&h<19)
          this.greet = '傍晚好，';
        else if(h>=19&&h<23)
          this.greet = '晚上好，';
        else if(h>=23||(h>=0&&h<3))
          this.greet = '夜深了，';
      },

    }
</script>
<style>
  .el-aside {
    border-top: 3px solid #ff0000;
    color: #333;
    background-color: #fafafa;
    position: relative;
  }
  .el-header {
    border-top: 3px solid #ff0000;
    box-shadow: 0px 2px 10px 0px rgba(0,0,0,0.1), 0 1px rgba(0,0,0,0.1);
    background-color: #fafafa;
    color: #333;
    line-height: 64px;
  }
  .el-menu-item.is-active{
    background-color: #409EFF !important;
    font-weight: bold;
  }
  .bt-registered{
    margin-left: 10px;
    background: red;
    color: white;
    transition: all .2s linear;
    display: inline-block;
    padding: 0 12px;
    cursor: pointer;
    height: 34px;
    line-height: 34px;
    font-weight: 500;
    border-radius: 5px;
  }
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .login-title1 {
    text-align: left;
    margin: 0 auto 40px auto;
    color: #212121;
    font-size: 24px;
  }
  .login-title {
    text-align: left;
    margin: 0 auto 40px auto;
    color: #ff0000;
    font-size: 24px;
  }

</style>
