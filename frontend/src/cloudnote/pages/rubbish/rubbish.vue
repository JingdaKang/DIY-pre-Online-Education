<template>
    <div style="padding-left: 2%;padding-right: 2%"
    >

    <top-bar @ForeverDelete="ForeverDelete"></top-bar>

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

    <el-row style="padding-left: 1%"
    v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    >
    <!--            文件-->
    <rubbish-file  @Recover="Recover" @DeleteForever = "DeleteForever" v-for="f in ArticleList" :key="f.id" :file-info="f"></rubbish-file>


    <center v-if="ArticleList.length==0" >
        <i class="el-icon-edit" style="margin-top: 10%;font-size: 50px;"></i>
        <span style="font-family: 楷体;font-size: 30px"> 空空如也</span>
    </center>


</el-row>

</div>
</template>

<script>
import RubbishFile from "@/cloudnote/pages/rubbish/components/RubbishFile";
import TopBar from "@/cloudnote/pages/rubbish/components/TopBar";
import request from "@/network/request";
export default {
    name: "rubbish",
    components: {TopBar, RubbishFile},
    //测试代码
    /*mounted(){
        this.loading=true;
        this.ArticleList=this.testdata.items;
        this.Count = this.testdata.total;
        this.loading=false;
    },*/

    mounted(){
        this.loading=true;
        request({
            url:"/note/getRubbish/",
        }).then(resp=>{
            this.ArticleList=resp.data.results;
            if(this.ArticleList==null){this.ArticleList=[]}
                this.Count = resp.data.count;
            this.loading=false
        })


    },


    data:function () {
        return{
            loading:false,
            keywords:"",
            ArticleList:[],
            Count:0,
            currentPage:1,
            Total:1,
            recoverOK:{
                "code": 200,
                "msg": "恢复成功！",
                "data": null
            },
        }
    },
    methods:{
        Recover(id) {
            this.loading=true
                /*this.$message({
                    type:"success",
                    message:this.recoverOK.msg
                });

                for(var i=0;i<this.ArticleList.length;i++){
                    if(this.ArticleList[i].id==id){
                        this.ArticleList.splice(i,1)
                    }
                }*/
                request({
                    url:"/note/recover/",
                    params:{
                        id:id
                    }
                }).then(resp=>{

                    if (resp.data.code==500){
                        this.$message({
                            type:"warning",
                            message:resp.data.msg
                        })

                    } else{
                        this.$message({
                            type:"success",
                            message:this.recoverOK.msg
                        });

                        for(var i=0;i<this.ArticleList.length;i++){
                            if(this.ArticleList[i].id==id){
                                this.ArticleList.splice(i,1)
                            }
                        }

                    }

                    this.loading=false



                })
            },
            DeleteForever(id){
                this.loading=true
                request({
                    url:'/note/'+id+'/',
                    method:'delete',
                }).then(resp=>{
                    console.log(resp.code)
                    this.$message({
                        type:"success",
                        message:"永久清除成功"
                    });
                    for(var i=0;i<this.ArticleList.length;i++){
                        if(this.ArticleList[i].id==id){
                            this.ArticleList.splice(i,1)
                        }
                    }
                    this.loading=false
                })

            },

            ForeverDelete() {
                this.loading=true;
                request({
                    url:"/article/delete/forever"
                }).then(resp=>{
                    this.$message({
                        type:"success",
                        message:resp.data.msg
                    })

                    this.ArticleList=[]
                    this.loading=false
                })
            }

        }
    }
    </script>

    <style scoped>

    </style>
