<template>
    <div  v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    style="padding-left: 1%;"
    >



    <el-row>


        <el-col :span="16" >
            <el-tooltip  effect="light"  placement="right">
                <div slot="content">


                    <el-link icon="el-icon-edit" @click="dialogVisible=true"></el-link>
                    <el-divider direction="vertical"></el-divider>
                    <el-link class="el-icon-info"> </el-link>
                    <el-divider direction="vertical"></el-divider>
                    <el-link class="el-icon-delete" @click="Delete"></el-link>


                </div>




                <el-link style="font-size: 17px"  @click="AccessFolder"  >
                    <i class="el-icon-folder" style="margin-right: 1px"></i>
                {{FolderInfo.notebook_name}}</el-link>
            </el-tooltip>
        </el-col>

        <!--            编辑框-->
        <el-dialog
        title="修改"
        :visible.sync="dialogVisible"
        width="30%"
        >
        <el-input v-model="current_title"></el-input>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="Update">确 定</el-button>
        </span>
    </el-dialog>
    <!--                    日期-->
    <el-col  :span="4" style="float: right;margin-right: 5%">

        <i class="el-icon-date" style="color: #409EFF">{{FolderInfo.notebook_modify}}</i>


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
    name: "Folder",
    props:["FolderInfo"],
    data:function () {
        return{
            loading:false,
            dialogVisible:false,
            current_title:this.FolderInfo.notebook_name
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
                        message:'已将笔记本内所有笔记放入回收站！'
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