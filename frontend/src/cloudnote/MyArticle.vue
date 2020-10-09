<template>
    <div  v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    style="padding-left: 1%;"
    >

    <el-row>
        <el-col :span="16" >
            <el-tooltip  effect="light"  placement="right">

                <div slot="content">
                    <el-link icon="el-icon-edit" @click="Edit(ArticleInfo.id)"></el-link>
                    <el-divider direction="vertical"></el-divider>
                    <el-link class="el-icon-info"> </el-link>
                    <el-divider direction="vertical"></el-divider>
                    <el-link class="el-icon-delete" @click="DeleteArticle"></el-link>


                </div>
                <el-link style="font-weight: bolder;font-size: 15px" @click="GetArticleInfo(ArticleInfo.id)" target="_blank"  >
                    <i class="el-icon-document" style="margin-right: 1px"></i>
                {{ArticleInfo.note_title}}</el-link>
            </el-tooltip>

        </el-col>
        <!--                    日期-->
        <el-col  :span="4" style="float: right;margin-right: 5%">

            <i class="el-icon-date" style="color: #409EFF" >{{ArticleInfo.note_modify}}</i>


        </el-col>
    </el-row>
    <!--                横线-->
    <el-row>
        <hr >
    </el-row>



    <!--文章展示-->
    <el-drawer
    :title="articleDetail.title"
    :visible.sync="dialogVisible"
    size="auto"
    direction="ttb"
    style="overflow: auto;"
    >
    <div style="padding:0 2%">
        <makedown-show
        :mk-value="articleDetail.mkValue" ></makedown-show>
    </div>
</el-drawer>





</div>




</template>

<script>

import request from "@/network/request";
import MakedownShow from "@/cloudnote/makedownShow";

export default {
    name: "MyArticle",
    components: {MakedownShow},
    props:["ArticleInfo"],
    data:function(){
        return{
            articleDetail:{
              mkValue:'',
              title:'',
              id:0,
          },
          dialogVisible:false,
          articleView:null,
          loading:false,
      }
  },
  methods: {
    GetArticleInfo(id){
        //this.loading = true;

        request({
            url:'/note/'+id
        }).then(resp=>{
            var data = resp.data;
            this.articleDetail.mkValue  = data.note_text;
            this.articleDetail.title = data.note_title;
            this.articleDetail.id = data.id;
            this.loading = false;
            this.dialogVisible=true;
        })
    },
    DeleteArticle(){
        this.loading=true;
        request({
            method:'get',
            url:"/note/delete/",
            params:{
                id:this.ArticleInfo.id
            }

        }).then(resp=>{
            this.$message({
                type:'success',
                message:"成功将笔记放入回收站！"
            });

            this.$emit('DeleteArticle',resp.data.id);
            this.loading=false
        });
    },


    Edit(id){
        this.loading=true;
                //注意 axios是异步请求
                request({
                    url:'/note/'+id
                }).then(resp=>{
                    this.articleView= resp.data;
                    this.$router.push({
                        name:"write",
                        params:{
                            article:this.articleView
                        }
                    });
                    this.loading=false

                });


            }

        }

    }
    </script>

    <style scoped>
    /deep/ .el-drawer{
        background-color:rgb(209, 231, 254) !important;
        text-align:center;
        font-size:20px;
    }
    </style>
