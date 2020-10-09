<template>
    <div  style="padding-top: 1%;"
    v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"

    >
    <el-row v-if = "detail">
        <el-col :span="18">
            <span style="font-weight: bold;font-size:20px">{{currentDisplay.teamName}}</span>
            <span style="margin-left:20px"><el-popover
                placement="right"
                width="100"
                trigger="hover">
                <el-table :data="gridData">
                    <el-table-column width="100" property="name" label="成员"></el-table-column>
                </el-table>
                <el-button slot="reference" type = "text" style = "color:#333;
                padding: 12px 5px;">    <i class="el-icon-user-solid"></i>
                <span style="margin-left: 10px">{{currentDisplay.memberNum}}个成员</span></el-button>
            </el-popover>
            <el-button round type = "text"  icon = "el-icon-plus" @click = "invite">邀请</el-button>
        </span>
    </el-col>

    <el-col :span="6">
        <el-button style = "margin-left:37%" type="text"  round size="mini" @click="back"><i class="el-icon-back" ></i>返回</el-button>
        <el-button class = "button-style" type="primary"  round size="mini" @click="open('笔记本名称')" v-if='is_notebook'><i class="el-icon-folder-add" ></i>新建笔记本</el-button>
        <el-button class = "button-style" type="success" round size="mini" @click="open('笔记名称')" v-if='is_note'><i class="el-icon-document-add" ></i>新建笔记</el-button>

    </el-col>
</el-row>

<el-row v-if = "!detail">
    <el-col :span="20">
        <span style="font-weight: bold;font-size:20px">团队笔记</span>



    </el-col>

    <el-col :span="4">
        <el-button class = "button-style" type="primary"  round size="mini" @click="open('团队名称')"><i class="el-icon-folder-add" ></i>新建团队</el-button>

    </el-col>
</el-row>
</div>
</template>

<script>

import request from "@/network/request";
export default {
    name: "navigate",
    data:function(){
      return{
          Nav:['首页',],
          loading:false,
          detail:false,
          is_note:false,
          is_notebook:false,
          currentDisplay:null,
          currentIndex:null,
          currentNotebookIndex:null,
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
            team_id:null,
            folder_title:""
        },
        currentNotebook:null,
    }
},
computed:{
    gridData:function () {
        var data = [];
        var members = this.currentDisplay.members;
        for(let index in members){
            data.push({"name":members[index]});
        }
        return data;
    },

},
methods:{
    invite(){        
        this.$prompt("请输入邀请成员昵称", '邀请', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
        }).then(({ value }) => {
            console.log(value);
            request({
                url:"/team/invite/",
                method:'post',
                data:{
                    member_name:value,
                    team_id:this.currentDisplay.teamId
                }
            }).then(resp=>{
                this.$message({
                    type: 'success',
                    message:"邀请成功！"
                });
                console.log(resp.data);
                //this.currentDisplay.members.push(resp.data.member);
                //this.currentDisplay.memberNum++;
            });
        });
    },
    open(title){
        this.$prompt(title, '创建', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
        }).then(({ value }) => {
            console.log(this.currentDisplay);
            this.loading = true;
            if(title=="团队名称"){
              request({
                url:"/team/",
                method:'post',
                data:{
                    team_name:value,
                }
            }).then(resp=>{
                this.$message({
                    type: 'success',
                    message:'创建成功！'
                });
                var temp = {}
                temp.teamName = resp.data.team_name;
                temp.notebookNum = resp.data.notebooks.length;
                temp.noteNum = resp.data.notes.length;
                temp.createTime = resp.data.team_create;
                temp.modifyTime = resp.data.team_modify;
                temp.creator = resp.data.leader_id;
                temp.modifier = resp.data.modifier_id;
                temp.memberNum = resp.data.members.length;
                temp.members = resp.data.members;
                temp.teamId = resp.data.id;
                let teamTable = this.$parent.$refs.TeamList.$refs.TeamTable
                teamTable.Total++;
            if(teamTable.currentPage<(Math.ceil(teamTable.Total/6))){
                teamTable.handleCurrentChange(Math.ceil(teamTable.Total/6))
            }else{
                teamTable.tableData.push(temp);
            }

                this.loading = false;
            }).catch(err=>{
                this.$message({
                    type: 'error',
                    message:err
                });
            })

        }else if(title=="笔记本名称"){
           request({
            url:"/notebook/createTeamNotebook/",
            method:'post',
            data:{
                team_notebook_name:value,
                team_id:this.currentDisplay.teamId
            }
        }).then(resp=>{
            this.$message({
                type: 'success',
                message:'创建成功！'
            });
            var temp = {}
            temp.tNotebookId = resp.data.id;
            temp.tNotebookName = resp.data.notebook_name;
            temp.tNoteNum = resp.data.notebook_note.length;
            temp.createTime = resp.data.notebook_create;
            temp.modifyTime = resp.data.notebook_modify;
            temp.creator = resp.data.creator_id;
            temp.modifier = resp.data.modifier_id;
            let teamNotebook = this.$parent.$refs.TeamList.$refs.TeamNotebook;
            teamNotebook.Total++;
            if(teamNotebook.currentPage<(Math.ceil(teamNotebook.Total/6))){
                teamNotebook.handleCurrentChange(Math.ceil(teamNotebook.Total/6))
            }else{
                teamNotebook.tableData.push(temp);
            }
            this.$parent.$refs.TeamList.$refs.TeamTable.tableData[this.currentIndex].notebookNum++;
            this.$parent.$refs.TeamList.$refs.TeamTable.tableData[this.currentIndex].modifyTime = temp.modifyTime;
            this.$parent.$refs.TeamList.$refs.TeamTable.tableData[this.currentIndex].modifier = temp.modifier;
            this.loading = false;
        }).catch(err=>{
            this.$message({
                type: 'error',
                message:err
            });
        });

    }else if(title=="笔记名称"){
        this.articleView.note_title = value;
        this.articleView.notebook_id = this.currentNotebook;
        this.articleView.team_id = this.currentDisplay.teamId;
        console.log("当前笔记本"+this.currentNotebook);
        console.log(this.articleView);
        this.$router.push({
            name:"write",
            params:{
                article:this.articleView
            }
        });
        this.loading = false;
    }




    this.$parent.$refs.FileList.Total++
    if(this.$parent.$refs.FileList.currentPage<(Math.ceil(this.$parent.$refs.FileList.Total/13))){
        this.$parent.$refs.FileList.handleCurrentChange(Math.ceil(this.$parent.$refs.FileList.Total/13))
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
                this.$parent.$refs.FileList.AccessFolder(resp.data.results,[],["首页",],Number(resp.data.count))
            }).catch(err=>{console.log(err)});
        }
        this.loading=false
        console.log(title);

    },
    back(){
        this.loading = true;
        if(this.$parent.$refs.TeamList.notebookDisplay==true){
            this.detail = false;
            this.currentDisplay = null;
            this.is_notebook=false;
            this.is_note = false;
            this.$parent.$refs.TeamList.notebookDisplay = false;
            this.$parent.$refs.TeamList.teamDisplay = true;
            this.$parent.$refs.TeamList.noteDisplay = false;
            this.$parent.$refs.TeamList.$refs.TeamNotebook.tableData = [];
        }else if(this.$parent.$refs.TeamList.noteDisplay==true){
            this.is_notebook=true;
            this.is_note=false;
            this.$parent.$refs.TeamList.notebookDisplay = true;
            this.$parent.$refs.TeamList.teamDisplay = false;
            this.$parent.$refs.TeamList.noteDisplay = false;
            this.$parent.$refs.TeamList.$refs.TeamNote.tableData = [];
        }


        this.loading = false;
    }
}
}
</script>

<style scoped>
.button-style{
    float:right;
}
</style>