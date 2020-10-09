<template>
    <div  v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    >



    <el-row>


        <el-col :span="16" >
            <el-link style="font-size: 17px"  @click="dialogVisible=true"  >
                <i class="el-icon-message" style="margin-right: 1px"></i>
            {{NoticeInfo.notebook_name}}</el-link>
        </el-col>

        <!--            通知详情框-->
        <el-dialog
        title="通知"
        :visible.sync="dialogVisible"
        width="30%"
        >
        <span>。。邀请您加入。。。小组</span>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">拒绝邀请</el-button>
            <el-button type="primary" @click="Update">接受邀请</el-button>
        </span>
    </el-dialog>
    <!--                    日期-->
    <el-col  :span="4">

        <i class="el-icon-date" style="color: #409EFF">{{NoticeInfo.notebook_modify}}</i>


    </el-col>
</el-row>


<!--                横线-->
<el-row>
    <hr  >
</el-row>

</div>
</template>

<script>
import request from "@/network/request";

export default {
    name: "NoticeDetail",
    props:["NoticeInfo"],
    data:function () {
        return{
            loading:false,
            dialogVisible:false,
            //current_title:this.FolderInfo.notebook_name
        }
    },
    methods:{
        Delete(){
            if(this.FolderInfo.id==1){
                this.$message({
                    type: 'error',
                    message:'默认笔记本不可删除！'
                });
            }else{
                this.loading=true;
                request({
                    url:"/notebook/delete/",
                    params:{
                        id:this.FolderInfo.id
                    }
                }).then(resp=>{
                    this.$message({
                        type: 'success',
                        message:'已将笔记本内所有笔记放入废纸篓！'
                    });
                    console.log(resp);
                    this.$emit('DeleteFolder',this.FolderInfo.id);
                    this.loading=false;
                })
            }
        },
        Update(){
            this.loading=true;
            request({
                url:"/notebook/"+this.FolderInfo.id+"/",
                method:'put',
                data:{
                    notebook_name:this.current_title,
                    creator_id:sessionStorage.getItem('user_id')
                }
            }).then(resp=>{
                this.FolderInfo.notebook_name = resp.data.notebook_name;
                this.$message({
                    type:"success",
                    message:"修改成功: "+this.FolderInfo.notebook_name
                });

                this.current_title = this.FolderInfo.notebook_name;
                this.loading=false;
                this.dialogVisible=false
            })
        },
        AccessFolder(){
            this.loading=true;
            request({
                url:"/note/listByNotebook/",
                params:{notebook_id:this.FolderInfo.id}
            }).then(resp=>{
                this.$emit("AccessFolder",[],resp.data.results,["首页",this.FolderInfo.notebook_name],resp.data.count,this.FolderInfo.id)
                this.loading=false;
            })
            /**this.$emit("AccessFolder",[{
                    id:1,
                    created_at:"2020-03-08",
                    updated_at:"2020-03-08",
                    deleted_at:"0-0-0-0",
                    title:"test",
                    dir_path:[],
                    tags:[],
                    mkValue: "",
                    folder_id:1,
                    folder_title:"默认笔记本"
                },],['首页','默认笔记本',],1)**/
            }
        }


    }
    </script>

    <style scoped>

    </style>