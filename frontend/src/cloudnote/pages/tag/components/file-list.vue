<template>
    <div >
        <el-row  v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"

        style="padding-left: 1%;">


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
import MyArticle from "@/cloudnote/MyArticle";
import request from "@/network/request";

export default {
    name: "file-list",
    data: function () {
        return {
            loading:false,
            FolderList: [],
            ArticleList: [],
            Nav:["标签"],
            currentPage:1,
            Total:1,
            currentTitle:"首页",
            tag_id:null

        }
    },
    watch: {
        '$route':'load'
    },
    created() {
        this.load();

    },

    activated() {
        this.load();


    },
    methods:{
        load(){
            this.loading=true;
            if(this.$route.query.tag_id){
                this.tag_id = this.$route.query.tag_id;
            }
            request({
                url:"/tag/listNoteByTag/",
                params:{
                    tag_id:this.tag_id,
                    user_id:sessionStorage.getItem('user_id'),
                }
            }).then(resp=>{
                this.ArticleList=resp.data.results;
                this.Nav=["标签",resp.data.tag_name];
                this.$parent.$refs.navigate.Nav = this.Nav;
                this.Total = Number(resp.data.count);
                this.loading=false


            }).catch(err=>{console.log(err)});
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

        handleCurrentChange(val){
            this.currentPage = val;
            this.loading = true;
            request({
                url:"/tag/listNoteByTag/",
                params:{
                    tag_id:this.tag_id,
                    user_id:sessionStorage.getItem('user_id'),
                    page:val,
                }
            }).then(resp=>{
                this.ArticleList=resp.data.results;
                this.Nav=["标签",resp.data.tag_name];
                this.$parent.$refs.navigate.Nav = this.Nav;
                this.Total = Number(resp.data.count);
                this.loading=false


            }).catch(err=>{console.log(err)});
            this.currentPage = val;

        }
    },
    computed:{
    },
    components: {
        MyArticle
    },
}
</script>

<style scoped>

</style>
