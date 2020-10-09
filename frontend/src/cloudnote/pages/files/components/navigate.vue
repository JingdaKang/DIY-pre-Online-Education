<template>
    <div  style="padding-top: 1%;"
    v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"

    >
    <el-row>
        <el-col :span="19">

            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item v-for="(n) in Nav" :key="n"> <el-button :class="{ 'el-icon-house':n=='首页'  }" size="mini" round  style="font-weight: bolder" @click="ChangeNav(n)">{{n}}</el-button></el-breadcrumb-item>
            </el-breadcrumb>



        </el-col>

        <el-col :span="5">
            <el-button class = "button-style" type="primary"  round size="mini" @click="open('笔记本名称')" v-if = "!is_note"><i class="el-icon-folder-add" style="margin-right: 4px" ></i>新建笔记本</el-button>
            <el-button  class = "button-style" type="primary" round size="mini" @click="open('笔记名称')" v-if = "is_note"><i class="el-icon-document-add" style="margin-right: 4px" ></i>新建笔记</el-button>

        </el-col>
    </el-row>
</div>
</template>

<script>

import request from "@/network/request";
export default {
    name: "navigate",
    props:["display"],
    data:function(){
      return{
          Nav:['首页',],
          is_note:false,
          loading:false,
          articleView:{
            id:null,
            note_create:null,
            note_modify:null,
            deleted_at:null,
            note_title:"",
            current:[1],
            tags:[],
            note_text: "",
            notebook_id:1,
            folder_title:""
        },
    }
},
methods:{
    open(title){


        this.$prompt(title, '创建', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
        }).then(({ value }) => {
            this.loading=true;
            if (title==="笔记本名称"){

                request({
                    url:"/notebook/",
                    method:'post',
                    data:{
                        notebook_name:value,
                        creator_id:Number(sessionStorage.getItem('user_id'))
                    }
                }).then(resp=>{
                    this.$message({
                        type: 'success',
                        message:'创建成功！'
                    });
                    this.loading=false;
                    let fileList = this.$parent.$refs.FileList;
                    fileList.Total++;
                    if(fileList.currentPage<(Math.ceil(fileList.Total/8))){
                        fileList.handleCurrentChange(Math.ceil(fileList.Total/8));
                    }else{
                        fileList.FolderList.push(resp.data)

                    }
                    

                }).catch(err=>{
                    this.$message({
                        type: 'error',
                        message:err
                    });
                })


            }
            else if (title==="笔记名称"){
                this.articleView.note_title = value;
                this.articleView.notebook_id = this.$parent.$refs.FileList.currentNotebook;
                console.log("当前笔记本"+this.$parent.$refs.FileList.currentNotebook);
                this.$router.push({
                    name:"write",
                    params:{
                        article:this.articleView
                    }
                });
                this.loading = false;
            }

            this.$parent.$refs.FileList.Total++;
            if(this.$parent.$refs.FileList.currentPage<(Math.ceil(this.$parent.$refs.FileList.Total/8))){
                this.$parent.$refs.FileList.handleCurrentChange(Math.ceil(this.$parent.$refs.FileList.Total/8))
            }

        });



    },
    ChangeNav(title){
        this.loading=true;
        if(title==="首页"){
            request({
                url:"/notebook/",
                params:{
                    type:"base"
                }
            }).then(resp=>{
                this.$parent.$refs.FileList.AccessFolder(resp.data.results,[],["首页",],Number(resp.data.count),-1)
            }).catch(err=>{console.log(err)});
        }
        this.loading=false
        console.log(title);

    }
}
}
</script>

<style scoped>
.button-style{
    float:right;
}
</style>