<template>
    <div style="padding-left: 2%" >
    <div  style="padding-top: 1%;">

        <el-row>
                <span style="font-weight: bold;font-size:20px">用户中心</span>


        </el-row>
    </div>
    <div>
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>个人信息</span>
            <el-button v-if= "!isEdit" style="float: right; padding: 3px 0" type="text" @click="edit">修改</el-button>
            <el-button v-if= "isEdit" style="float: right; padding: 3px 0" type="text" @click="save">保存</el-button>
        </div>
        <div class = "info-body">
            <div>
                <div class="left"><span >用户名：</span></div>
                <div class="right">
                    <span v-if = "!isEdit">{{dataForm.username}}</span>
                    <el-input v-if="isEdit" auto-complete="off" v-model="dataForm.username" size = "small"></el-input>
                </div>
            </div>
            <div>
                <div class="left"><span>性别：</span></div>
                <div class="right">
                    <span v-if = "!isEdit">{{dataForm.gender}}</span>
                    <el-radio v-model="dataForm.gender" label="男" v-show = "isEdit">男</el-radio>
                    <el-radio v-model="dataForm.gender" label="女" v-show = "isEdit">女</el-radio>
                </div>
            </div>
            <div>
                <div class="left"><span>邮箱：</span></div>
                <div class="right"><span v-if = "!isEdit">{{dataForm.email}}</span>
                    <el-input v-if="isEdit" auto-complete="off" v-model="dataForm.email" size = "small"></el-input></div>
                </div>
                <div>
                    <div class="left"><span>电话号码：</span></div>
                    <div class="right"><span v-if = "!isEdit">{{dataForm.tel}}</span>
                        <el-input v-if="isEdit" auto-complete="off" v-model="dataForm.tel" size = "small"></el-input></div>
                    </div>
                    <div>
                        <div class="left"><span>身份：</span></div>
                        <div class="right"><span v-if = "!isEdit">{{dataForm.type}}</span><el-input v-if="isEdit" :disabled="true" v-model="dataForm.type" size = "small"></el-input></div>
                    </div>
                    <div>
                        <div class="left"><span>出生年月：</span></div>
                        <div class="right"><span v-if = "!isEdit">{{dataForm.bir}}</span>
                            <el-date-picker v-if = "isEdit" size = "small"
                            v-model="dataForm.bir"
                            type="date"
                            placeholder="选择日期"
                            value-format="yyyy-MM-dd">
                        </el-date-picker></div>
                    </div>
                </div>
            </el-card>
        </div>
    </div>
</template>
<style>

.text {
    font-size: 14px;
}
.box-card{
    margin: 3% auto;
}
.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}
.clearfix:after {
    clear: both
}

.box-card {
    width: 480px;
}
.info-body{
    line-height: 3;
}
.left{
    width: 20%;
    display: inline;
}
.right{
    width: 80%;
    float: right;
}
</style>

<script>
import request from "@/network/request";
export default {
    name: "manage",
    methods:{
        edit(){
            this.isEdit = true
        },
        save(){
            var genderDic = {'男':'M','女':'F'};
            request({
                url:"/user/"+sessionStorage.getItem('user_id')+"/",
                method:"put",
                data:{
                    username:this.dataForm.username,
                    user_gender:genderDic[this.dataForm.gender],
                    email:this.dataForm.email,
                    user_tel:this.dataForm.tel,
                    user_bir:this.dataForm.bir,
                    is_active:true,
                }
            }).then(resp=>{
                console.log(resp);
            }).catch(err=>{console.log(err)});
            this.isEdit = false;
        }
    },
    data: function () {
        return {
            isEdit:false,
            dataForm: {
                username:null,
                gender:null,
                email:null,
                tel:null,
                type:null,
                bir:null,
            },
        }
    },
    created(){
        request({
            url:"/user/"+sessionStorage.getItem('user_id')+"/",
        }).then(resp=>{
            var result = resp.data;
            console.log(result);
            var genderDic = {'M':"男",'F':"女",'D':"未设定"};
            var typeDic ={'S':'学生','T':'教师','M':'管理员'};
            this.dataForm.username = result.username;
            this.dataForm.gender = genderDic[result.user_gender];
            this.dataForm.email = result.email==""?"未设定":result.email;
            this.dataForm.tel = result.user_tel==null?"未设定":result.user_tel;
            this.dataForm.type = typeDic[result.type];
            this.dataForm.bir = result.user_bir==null?"未设定":result.user_bir;               
        })
    }
}
</script>

<style scoped>

</style>