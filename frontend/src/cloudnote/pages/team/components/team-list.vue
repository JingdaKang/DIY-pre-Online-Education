<template>
    <div >
        <el-row  v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"

        style="padding-left: 1%">

    <!--            display-->
    <team-note ref = "TeamNote"  v-show = "noteDisplay"></team-note>
    <team-notebook ref = "TeamNotebook" @accessFolder = "accessFolder" v-show = "notebookDisplay"></team-notebook>
    <team-table  ref = "TeamTable" @getdetail = "getDetail" v-show = "teamDisplay"></team-table>

    <center v-if="(FolderList.length==0) && (ArticleList.length==0)" >
        <i class="el-icon-edit" style="margin-top: 10%;font-size: 50px;"></i>
        <span style="font-family: 楷体;font-size: 30px"> 空空如也</span>
    </center>


</el-row>
</div>
</template>

<script>
import TeamTable from "./TeamTable";
import TeamNote from "./TeamNote";
import TeamNotebook from "./TeamNotebook";
import request from "@/network/request";

export default {
    name: "team-list",
    data: function () {
        return {
            loading:false,
            FolderList: [],
            ArticleList: [],
            Nav:["首页"],
            currentPage:1,
            Total:1,
            currentTitle:"首页",
            noteDisplay:false,
            teamDisplay:true,
            notebookDisplay:false

        }
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
            if(this.Total%13===0){  //如果不足一页 则退到上一页
                this.$parent.$refs.FileList.handleCurrentChange(Math.floor(this.$parent.$refs.FileList.Total/13))
            }

        },

        DeleteArticle(id){
            for(var i=0;i<this.ArticleList.length;i++){
                if(this.ArticleList[i].id==id){
                    this.ArticleList.splice(i,1)
                }
            }

            this.Total--;
            if(this.Total%13===0){
                this.$parent.$refs.FileList.handleCurrentChange(Math.floor(this.$parent.$refs.FileList.Total/13))
            }

        },

        accessFolder(index,row){
            this.loading = true;
            this.noteDisplay = true;
            this.teamDisplay = false;
            this.notebookDisplay = false;
            this.$parent.$refs.Navigate.is_notebook = false;
            this.$parent.$refs.Navigate.is_note = true;
            this.$parent.$refs.Navigate.currentNotebookIndex = index;
            //加载对应团队笔记本的团队笔记
            request({
                url:"/note/listByNotebook/",
                params:{notebook_id:row.tNotebookId}
            }).then(resp=>{
                var tNotes=resp.data.results;

                for(let index in tNotes){
                  var temp = {}
                  temp.tNoteId = tNotes[index].id;
                  temp.tNoteName = tNotes[index].note_title;
                  temp.createTime = tNotes[index].note_create;
                  temp.modifyTime = tNotes[index].note_modify;
                  temp.creator = tNotes[index].writer_id;
                  temp.modifier = tNotes[index].modifier_id;
                  this.$refs.TeamNote.tableData.push(temp);
              }
              this.$parent.$refs.Navigate.currentNotebook = row.tNotebookId;
              this.$refs.TeamNote.currentNotebook = row.tNotebookId;
              this.$refs.TeamNote.Total = Number(resp.data.count);
              this.loading = false;

          }).catch(err=>{console.log(err)});


        },

        getDetail(index,row){
            let team = row;
            this.loading = true;
            this.notebookDisplay = true;
            this.teamDisplay = false;
            this.noteDisplay = false;
            console.log(this.$parent.$refs.Navigate);
            this.$parent.$refs.Navigate.is_notebook = true;
            this.$parent.$refs.Navigate.is_note = false;
            this.$parent.$refs.Navigate.detail = true;
            this.$parent.$refs.Navigate.currentDisplay = row;
            this.$parent.$refs.Navigate.currentIndex = index;            
            //加载对应团队的团队笔记本
            request({
                url:"/notebook/listTeamNotebook/",
                params:{
                    team_id:row.teamId
                }
            }).then(resp=>{
                var tNotebooks=resp.data.results;

                for(let index in tNotebooks){
                  var temp = {}
                  temp.tNotebookId = tNotebooks[index].id;
                  temp.tNotebookName = tNotebooks[index].notebook_name;
                  temp.tNoteNum = tNotebooks[index].notebook_note.length;
                  temp.createTime = tNotebooks[index].notebook_create;
                  temp.modifyTime = tNotebooks[index].notebook_modify;
                  temp.creator = tNotebooks[index].creator_id;
                  temp.modifier = tNotebooks[index].modifier_id;
                  this.$refs.TeamNotebook.tableData.push(temp);
              }
                this.$refs.TeamNotebook.currentTeam = team;
              this.$refs.TeamNotebook.Total = Number(resp.data.count);

              this.loading = false;

          }).catch(err=>{console.log(err)});
        },
    },
    computed:{
    },
    components: {
        TeamTable,
        TeamNotebook,
        TeamNote
    },
}
</script>

<style scoped>

</style>