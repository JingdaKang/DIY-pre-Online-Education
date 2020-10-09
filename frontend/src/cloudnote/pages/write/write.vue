<template>
    <div style="padding-left: 1%;"
    v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
    >


    <!--编辑器-->
    <el-col :span="21" style="padding-right: 1%;" >
        <el-row>

            <div style="text-align: center;margin-bottom: 1%;margin-top: 1%;font-size: 30px">
                <el-input v-model="article.title" placeholder="标题"></el-input>
            </div>

        </el-row>
        <el-row>
            <mavon-editor style="height:700px;" v-model="article.mkValue"
            :ishljs="true"
            ref="md"
            @imgAdd="ImgAdd"
            @imgDel="ImgDel"
            @save="Save" />
        </el-row>
        <el-row style="text-align: center">
            <el-link type="success">感谢使用</el-link>
        </el-row>
    </el-col>


    <!--        编辑器侧边信息-->
    <el-col  :span="3" style="padding-top: 2%">

        <!--            日期-->
        <div style="text-align: center">
            创建日期: <i class="el-icon-date" style="color: deepskyblue">{{create_time}}</i><br>
            最近更新: <i class="el-icon-date" style="color: deepskyblue">{{update_time}}</i>
        </div>
        <el-divider></el-divider>

        <!--          笔记本目录-->
        <div >
            笔记本:
            <el-cascader
            :props="props"
            v-model="article.current"
            :options="options"
            @change="handleChange"
            ></el-cascader>


        </div>
        <el-divider></el-divider>
        <!--      标签-->
        <el-row type = "flex" justify = "center" style="padding: 10px;">
          <div>
              <el-tag
              :key="tag"
              v-for="tag in this.article.tags"
              closable
              :disable-transitions="false"
              @close="handleClose(tag)" >
              {{tag}}
          </el-tag>
          <el-input
          class="input-new-tag"
          v-if="inputVisible"
          v-model="inputValue"
          ref="saveTagInput"

          @keyup.enter.native="handleInputConfirm"
          @blur="handleInputConfirm"
          >
      </el-input>
      <el-button v-else class="button-new-tag"  @click="showInput">+ 添加标签</el-button>
  </div>
</el-row>
<el-row type = "flex" justify = "center" style="padding: 10px;">
    <el-button type="primary" icon="el-icon-check" @click="FinishSave" size = "medium">保存笔记</el-button>
</el-row>
<el-row type = "flex" justify = "center" style="padding: 10px;">
    <el-button type="primary" icon="el-icon-delete" @click="DeleteCache" size = "medium">清空内容</el-button>

</el-row>

</el-col>

</div>
</template>


<style>
.el-tag {
  margin-left: 25px;
  margin-bottom: 2px;
  margin-top: 2px;
}
.button-new-tag {
  margin-left: 10px;
  margin-top: 4px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>


<script>


import request from "@/network/request";
import axios from 'axios';
//import Tag from "@/components/Tag";
//import { post } from '@/network/http';
//import urls from '@/network/urls';

export default {
    name: "write",

    mounted(){
        //加载正在编辑的文章
        if(this.$route.params.article) {
            var tempdata = this.$route.params.article;
            this.article.title = tempdata.note_title;
            this.article.created_at = tempdata.note_create;
            this.article.updated_at = tempdata.note_modify;
            this.article.id = tempdata.id;
            this.article.mkValue = tempdata.note_text;
            this.article.folder_id = tempdata.notebook_id;
            this.article.current[0] = this.article.folder_id;
            this.article.tags = tempdata.tags;
            this.article.team_id = tempdata.team_id;
        }
        //加载笔记本选择器信息
        var notebook_url,notebook_params
        if(this.article.team_id!=null){
            notebook_url = "/notebook/listTeamNotebookName/";
            notebook_params = {
                type:"base",
                team_id:this.article.team_id,
            };
            request({
                url:notebook_url,
                params:notebook_params
            }).then(resp=>{
                var results = resp.data;
                var data = JSON.stringify(results,['id','notebook_name']);
                data = JSON.parse(data);
                this.options = data;
            });
        }else{
            notebook_url = "/notebook/listNotebookName/";
            notebook_params = {
                type:"base",
            };
            request({
                url:notebook_url,
                params:notebook_params
            }).then(resp=>{
                var results = resp.data;
                var data = JSON.stringify(results,['id','notebook_name']);
                data = JSON.parse(data);
                this.options = data;
            });
        }



    },

    beforeDestroy(){
      request({
        url:"/note/cancelLock/",
        method:'post',
        data:{
          note_id:this.article.id
      }
  }).then(resp=>{
    if(resp.data.code=="yes"){
        this.$message({
            type:"success",
            message:"退出编辑"
        });
    }
})
},
data:function () {
    return{
        loading:false,
        options:[],
        props: {
            value:"id",
            label:"notebook_name"

        },
        inputVisible: false,
        inputValue: '',

        article:{
            id:null,
            created_at:null,
            updated_at:null,
            deleted_at:null,
            title:"",
            current:[1],
            tags:[],
            mkValue: "",
            folder_id:0,
            folder_title:"",
            team_id:null
        },
    }

},
computed:{
    create_time(){
        if(this.article.id === null){
            return this.getNowFormatDate();
        }else{
            return this.article.created_at;
        }
    },
    update_time(){
        if(this.article.id === null){
            return this.getNowFormatDate();
        }else{
            return this.article.updated_at;
        }
    }
},
methods:{
    //获取当前格式化日期
    getNowFormatDate() {
        var date = new Date();
        var fullYear = date.getFullYear();
        var month = date.getMonth() + 1;
        var ms = month < 10 ? "-" + "0" + month : "-" + month;
        var day = date.getDate();
        var ds = day < 10 ? "-" + "0" + day : "-" + day;
        var rs = fullYear + ms + ds;
        var time = date.getHours();
        if (time < 10) {
            rs += " 0" + time;
        } else {
            rs += " " + time;
        }
        var minutes = date.getMinutes();
        var min = minutes < 10 ? ":0" + minutes : ":" + minutes;
        var seconds = date.getSeconds();
        var sed = seconds < 10 ? ":0" + seconds : ":" + seconds;
        rs += min + sed;
        return rs;
    },


            //点击保存事件
            FinishSave(){
                //this.loading=true;
                this.article.mkValue=this.$refs.md.$data.d_value;
                if(this.article.mkValue===""||this.article.title===""){
                    this.$message({
                        type:"error",
                        message:"请输入笔记标题或内容！"
                    });
                    return;
                }
                this.article.folder_id = this.article.current[0];
                if(this.article.id==0 || this.article.id==null){
                    console.log("new");
                    //新建笔记
                    request({
                        method:'post',
                        url:'/note/',
                        data:{
                            title:this.article.title,
                            mkValue:this.article.mkValue,
                            folder_id:this.article.folder_id,
                            tags:JSON.stringify(this.article.tags),
                            team_id:this.article.team_id,
                        }
                    }).then(resp=>{
                        this.article.created_at = resp.data.note_create;
                        this.article.updated_at = resp.data.note_modify;
                        this.article.id = resp.data.id;
                        this.addTag(resp.data.id);
                        this.loading=false;
                    }).catch(err=>{console.log(err)})
                }else{
                    //修改笔记
                    console.log("update");
                    request({
                        url:"/note/"+this.article.id+"/",
                        method:"put",
                        data:{
                            title:this.article.title,
                            mkValue:this.article.mkValue,
                            folder_id:this.article.folder_id,
                            tags:JSON.stringify(this.article.tags),
                            team_id:this.article.team_id,
                        }
                    }).then(resp=>{
                        this.article.created_at = resp.data.note_create;
                        this.article.updated_at = resp.data.note_modify;
                        this.addTag(this.article.id);
                        this.loading=false;
                    }).catch(err=>{console.log(err)})

                }


            },
            //给笔记添加标签
            addTag(id){
                let that = this;
                console.log("addToNote");
                request({
                    url:'/tag/addToNote/',
                    method:'post',
                    data:{
                        tags:JSON.stringify(this.article.tags),
                        note_id:id
                    }
                }).then(resp=>{
                    console.log(this.$parent.$parent);
                    that.$parent.$parent.$parent.ListTag();
                    console.log(resp.data.msg);
                    this.$message({
                        type:"success",
                        message:"保存成功！"
                    });

                })

            },
            //编辑器
            //保存 Ctrl+S回调
            Save(mkValue){
               //this.loading=true;
                this.article.mkValue=this.$refs.md.$data.d_value;
                if(this.article.mkValue===""||this.article.title===""){
                    this.$message({
                        type:"error",
                        message:"请输入笔记标题或内容！"
                    });
                    return;
                }
                this.article.folder_id = this.article.current[0];
                if(this.article.id==0 || this.article.id==null){
                    console.log("new");
                    //新建笔记
                    request({
                        method:'post',
                        url:'/note/',
                        data:{
                            title:this.article.title,
                            mkValue:this.article.mkValue,
                            folder_id:this.article.folder_id,
                            tags:JSON.stringify(this.article.tags),
                            team_id:this.article.team_id,
                        }
                    }).then(resp=>{
                        this.article.created_at = resp.data.note_create;
                        this.article.updated_at = resp.data.note_modify;
                        this.article.id = resp.data.id;
                        this.addTag(resp.data.id);
                        this.loading=false;
                    }).catch(err=>{console.log(err)})
                }else{
                    //修改笔记
                    console.log("update");
                    request({
                        url:"/note/"+this.article.id+"/",
                        method:"put",
                        data:{
                            title:this.article.title,
                            mkValue:this.article.mkValue,
                            folder_id:this.article.folder_id,
                            tags:JSON.stringify(this.article.tags),
                            team_id:this.article.team_id,
                        }
                    }).then(resp=>{
                        this.article.created_at = resp.data.note_create;
                        this.article.updated_at = resp.data.note_modify;
                        this.addTag(this.article.id);
                        this.loading=false;
                    }).catch(err=>{console.log(err)})

                }
                /*this.article.mkValue=mkValue;
                this.loading=true;

                request({
                    url:"/note/update/",
                    method:"post",
                    data:this.article
                }).then(resp=>{
                    this.$message({
                        type:"success",
                        message:resp.data.msg
                    });
                    this.article = resp.data.data;
                    this.loading=false
                }).catch(err=>{console.log(err)})*/
            },

            //图片上传
            ImgAdd(pos,imgfile){
                console.log(imgfile); //防止报错
                var data = new FormData();
                data.append('img', imgfile);
                this.loading=true;
                axios({
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    method: 'post',
                    url:"http://127.0.0.1:8888/api/img_upload/",
                    data:data
                }).then(resp=>{
                    this.$message({
                        type:"success",
                        message:"图片上传成功"
                    });
                    var temp = resp.data;
                    console.log(temp);
                    this.$refs.md.$img2Url(pos,resp.data.img);
                    this.loading=false

                }).catch(err=>{
                    this.$message({
                        type:"error",
                        message:err
                    })
                })
            },

            //图片从七牛云删除
            ImgDel(file){
                this.loading=true
                request({
                    url:"/qiniu/img_delete",
                    params:{
                        img_name:file[1].name
                    }
                }).then(resp=>{
                    if(resp.data.code==500){
                        this.$message({
                            type:"error",
                            message:resp.data.msg
                        })
                    }else{
                        this.$message({
                            type:"success",
                            message:resp.data.msg
                        })
                    }

                    this.loading=false
                })
            },


            //标签回调函数
            // tag是tags内容 也就是名字
            handleClose(tag) {
                this.article.tags.splice(this.article.tags.indexOf(tag), 1);
            },
            showInput() {
                this.inputVisible = true;
                this.$nextTick(() => {
                    this.$refs.saveTagInput.$refs.input.focus();
                });
            },
            handleInputConfirm() {
                let inputValue = this.inputValue;
                let is_repeated = this.article.tags.indexOf(inputValue);
                if (inputValue && is_repeated <0) {
                    if(this.article.tags==null){
                        this.article.tags = []
                    }
                    this.article.tags.push(inputValue)
                }
                this.inputVisible = false;
                this.inputValue = '';
            },

            //目录
            // 改变回调函数
            handleChange(val)
            {
                // eslint-disable-next-line no-console
                this.article.current = val;
                console.log(val);
            },

//清空redis缓存
DeleteCache(){
    /*request({
        url:'/article/temp_delete',
    }).then(resp=>{
        this.$message({
            type:"success",
            message:resp.data.msg
        });
        this.article={
            id:null,
            created_at:null,
            updated_at:null,
            deleted_at:null,
            title:"无标题",
            dir_path:[],
            tags:[],
            mkValue: "",
            folder_id:0,
            folder_title:""
        }

    })*/
    this.$message({
        type:"success",
        message:"清除成功！"
    });
    this.article={
        id:null,
        created_at:null,
        updated_at:null,
        deleted_at:null,
        title:"",
        current:[1],
        tags:[],
        mkValue: "",
        folder_id:0,
        folder_title:"",
        team_id:null
    }

}


}
}
</script>
