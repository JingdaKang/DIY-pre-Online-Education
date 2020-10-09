<template>
    <div >
        <el-row  v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"

        style="padding-left: 1%">


        <el-row >
            <el-pagination style="float: right;"

            :hide-on-single-page="false"
            layout="prev, pager, next"
            :total="Total"
            :page-size="8"
            :current-page="currentPage"
            @current-change="handleCurrentChange"
            >
        </el-pagination>


    </el-row>
    <!--            目录-->
    <folder  @AccessFolder="AccessFolder" @DeleteFolder="DeleteFolder" v-for="j in FolderList" :key="j.id" :folder-info="j"></folder>
    <!--            文件-->
    <my-article v-for="(i,k) in ArticleList" :key="k"  @DeleteArticle="DeleteArticle" :article-info="i"></my-article>

    <center v-if="(FolderList.length==0) && (ArticleList.length==0)" >
        <i class="el-icon-edit" style="margin-top: 10%;font-size: 50px;"></i>
        <span style="font-family: 楷体;font-size: 30px"> 空空如也</span>
    </center>


</el-row>
</div>
</template>

<script>
import Folder from "@/cloudnote/Folder";
import MyArticle from "@/cloudnote/MyArticle";
import request from "@/network/request";
import bus from './eventBus.js';

export default {
    name: "file-list",
    data: function () {
        return {
            loading:false,
            FolderList: [],
            ArticleList: [],
            Nav:["首页"],
            currentPage:1,
            Total:1,
            currentTitle:"首页",
            currentNotebook:-1,

        }
    },
    watch:{
        FolderList(val,oldVal){
            console.log(oldVal.length);
            if(val.length==0){
                this.$emit('ChangeDisplay',true);
            }else if(val.length!=0){
                this.$emit('ChangeDisplay',false);
            }
        }
    },
    created(){
        bus.$on('filterNote',(keyword)=>{
            request({
                url:'/note/listByKeyword/',
                params:{
                    keyword:keyword,
                    notebook_id:this.currentNotebook,
                }
            }).then(resp=>{
                this.ArticleList = resp.data.results;
                this.Total = resp.data.count;
                this.currentPage = 1;
            })

        });
        bus.$on('clearSearch',()=>{
            request({
                url:'/note/listByNotebook/',
                params:{
                    notebook_id:this.currentNotebook
                }
            }).then(resp=>{
                this.ArticleList = resp.data.results;
                this.Total = resp.data.count;
                this.currentPage = 1;
            })

        });
        bus.$on('ascOrder',()=>{
            this.ArticleList.sort(function (a, b) {
                return a.note_modify>b.note_modify?1:-1;
            });

        });
        bus.$on('descOrder',()=>{
            this.ArticleList.sort(function (a, b) {
                return a.note_modify<b.note_modify?1:-1;
            });

        });
    },
    mounted() {
        this.loading=true;
        request({
            url:"/notebook/",
            params:{
                type:"base"
            }
        }).then(resp=>{
            this.FolderList=resp.data.results;
            // this.ArticleList=resp.data.Articles;
            if(this.FolderList==null){this.FolderList=[]}
                this.loading=false;    
            this.Total = Number(resp.data.count)

            this.$parent.$refs.navigate.$data.Nav=this.Nav.reverse()

            this.loading=false


        }).catch(err=>{console.log(err)});





    },
    methods:{
        DeleteFolder(id) {
            for(var i=0;i<this.FolderList.length;i++){
                if(this.FolderList[i].id==id){
                    this.FolderList.splice(i,1)
                }
            }


            this.Total--;
                if(this.Total%8===0){  //如果不足一页 则退到上一页
                    this.$parent.$refs.FileList.handleCurrentChange(this.$parent.$refs.FileList.currentPage-1)
                }else{
                    this.$parent.$refs.FileList.handleCurrentChange(this.$parent.$refs.FileList.currentPage)
                }

            },

            DeleteArticle(id){
                for(var i=0;i<this.ArticleList.length;i++){
                    if(this.ArticleList[i].id==id){
                        this.ArticleList.splice(i,1)
                    }
                }

                this.Total--;
                if(this.Total%8===0){  //如果不足一页 则退到上一页
                    this.$parent.$refs.FileList.handleCurrentChange(this.$parent.$refs.FileList.currentPage-1)
                }else{
                    this.$parent.$refs.FileList.handleCurrentChange(this.$parent.$refs.FileList.currentPage)
                }
            },

            AccessFolder(FolderList,ArticleList,nav,total,notebook_id){
                this.FolderList=FolderList;
                this.ArticleList=ArticleList;
                this.Nav=nav;
                this.$parent.$refs.navigate.Nav = this.Nav;
                this.$parent.$refs.navigate.is_note = true;
                this.Total = Number(total);
                this.currentPage = 1;
                this.currentNotebook = notebook_id; 
                console.log("访问笔记本"+this.currentNotebook);
                if(nav.length==1){
                    this.$parent.$refs.navigate.is_note = false;
                    console.log("访问首页"+this.currentNotebook);
                }
               


            },
            handleCurrentChange(val){
                this.currentPage = val;
                this.loading = true;
                if(this.currentNotebook==-1){
                    request({
                        url:"/notebook/",
                        params:{
                            type:"base",
                            page:val
                        }
                    }).then(resp=>{
                        this.FolderList=resp.data.results;

                        if(this.FolderList==null){this.FolderList=[]}
                            this.loading=false;    
                        this.Total = Number(resp.data.count)

                        this.$parent.$refs.navigate.$data.Nav=this.Nav.reverse()

                        this.loading=false


                    }).catch(err=>{console.log(err)});                    
                }else if(this.currentNotebook>0){
                    request({
                        url:"/note/listByNotebook/",
                        params:{
                            notebook_id:this.currentNotebook,
                            page:val}
                        }).then(resp=>{
                            this.ArticleList=resp.data.results;
                            this.Total = Number(resp.data.count);
                            this.loading=false;
                        })                  
                    }


                }
            },
            computed:{
            },
            components: {
                Folder,
                MyArticle
            },
        }
        </script>

        <style scoped>

        </style>
