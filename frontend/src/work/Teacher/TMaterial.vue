<template>
  <div>
    <el-main
      v-loading="loading"
      element-loading-text="加载中">
      <!-- 共享资料界面 -->
      <el-col
        :offset="0"
        :span="24">
        <el-input
          style="width:160px;"
          prefix-icon="el-icon-search"
          class="search"
          v-model="search3"
          placeholder="输入关键字搜索"/>
        <el-button
          type="primary"
          @click="uploadmaterial()">上传资料</el-button>
        <el-table
          ref="materialTable"
          stripe
          :data="materialData1"
          empty-text="暂无数据">
          <el-table-column
            prop="materialnumber"
            label="资料编号"
            width="80">
          </el-table-column>
          <el-table-column
            prop="courseid"
            label="所属课程编号"
            width="120">
          </el-table-column>
          <el-table-column
            prop="belonged"
            label="所属课程"
            width="200">
          </el-table-column>
          <el-table-column
            prop="materialname"
            label="资料名"
            width="250">
          </el-table-column>
          <el-table-column
            prop="uploaduser"
            label="上传者"
            width="100">
          </el-table-column>
          <el-table-column
            prop="uploaddata"
            label="上传日期"
            sortable
            width="160">
          </el-table-column>
          <el-table-column
            prop="teacher"
            label="课程教师"
            width="100">
          </el-table-column>
          <el-table-column
            label="操作"
            width="200">
            <template slot-scope="scope">
              <el-button @click="downloadmaterial(scope.row.materialnumber)" type="text">下载资料
                <i class="el-icon-download"></i></el-button>
              <el-button @click="deletematerial(scope.row.materialnumber)" type="text">删除资料
                <i class="el-icon-delete"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
    <!-- 上传资料弹窗-->
    <el-dialog
      title="上传资料"
      :visible.sync="uploadialog"
      width="20%">
      <template>
        <el-select
          @change="coursechange()"
          v-model="course"
          placeholder="请选择课程">
          <el-option
            v-for="item in courses"
            :key="item.cid"
            :label="item.course"
            :value="item.cid">
            <span style="float: left">{{ item.course }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.cid }}</span>
          </el-option>
        </el-select>
      </template>
      <br><br>
      <el-upload
        class="upload-demo"
        action="https://jsonplaceholder.typicode.com/posts/"
        list-type="text"
        accept=".xls,.xlsx,.doc,.docx,.pdf,.txt,.rar,.zip,.jpg,.jpeg,.png"
        :show-file-list="true"
        :file-list="fileList"
        :on-success="uploadSuccess"
        :before-upload="beforeUpload">
        <el-button size="small" type="primary" :disabled="banup">点击上传</el-button>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "TMaterial",
      data() {
        return {
          user: '',
          loading: false,
          search3: '',
          courses:[],
          course:'',
          banup: false,
          fileUrl: '',
          filename:'',
          fileList: [],
          materialData: [],
          uploadialog: false,
        }
      },
      methods: {
        getMaterial(){
          this.materialData = [];
          this.loading = true;
          setTimeout(() => {
            this.$axios.post('/api/GetMaterial?T=1',{
              username:this.user
            }).then((res)=>{
              let tt = unescape(res.data.result).split(',');
              for(let i=0; i<tt.length/7; i++){
                let t = i*7;
                let ttt={
                  materialnumber:tt[t],
                  materialname:tt[t+5],
                  uploaduser:tt[t+4],
                  uploaddata:tt[t+6].substring(0,10)+" "+tt[t+6].substring(11,19),
                  belonged:tt[t+2],
                  courseid:tt[t+1],
                  teacher:tt[t+3]
                };
                this.materialData.push(ttt);
              }
            });
            this.loading = false;
          }, 1000);
        },
        downloadmaterial(fid){
          this.$axios.post('/api/GetMaterial?down=1',{
            fid:fid
          }).then((res)=>{
            window.location=res.data.file;
          });
        },
        deletematerial(fid){
          this.$confirm('此操作将删除该资料, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$axios.post('/api/GetMaterial?delete=1',{
              fid:fid
            }).then((res)=>{
              this.getMaterial();
              this.$message.success('删除成功!');
            });
          }).catch(() => {
            this.$message.info('已取消删除');
          });
        },

        uploadmaterial(){
          this.course='';
          this.courses=[];
          this.banup=true;
          this.$axios.post('/api/GetMaterial?teachercourse=1',{
            username:this.user
          }).then((res)=>{
            var tt = unescape(res.data.course).split(',');
            for(var i=0; i<tt.length/2; i++){
              var t = i*2;
              var ttt={
                cid:tt[t],
                course:tt[t+1]
              };
              this.courses.push(ttt);
            }
          });
          this.uploadialog = true;
        },
        coursechange(){
          this.cid = this.course;
          this.$axios.post('/api/GetMaterial?insert=1',{
            cid:this.course
          }).then((res)=>{
            if(res.data.msg===0){
              this.banup = true;
              this.$confirm('该课程暂未创建共享区，是否创建?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                this.$axios.post('/api/ShareArea?create=1',{
                  cid:this.cid,
                }).then((res)=>{
                  this.banup = false;
                  this.$message.success('创建成功!');
                });
              }).catch(() => {
                this.$message.info('取消创建');
              });
            }
            else
              this.banup = false;
          });
        },
        beforeUpload(file){
          let fd = new FormData();
          fd.append('file',file);//传文件
          this.$axios.post('/api/UploadMaterial?File=1',fd)
            .then((res) =>{
              this.fileUrl = unescape(res.data.url);
              this.filename = unescape(res.data.file);
            });
        },
        uploadSuccess() {
          let myDate = new Date();
          this.$axios.post('/api/UploadMaterial?up=1', {
            username: this.user,
            cid: this.cid,
            file: this.fileUrl,
            filename: this.filename,
            time: myDate
          }).then((res) => {
            this.$message.success('上传成功！');
            this.fileList = [];
          });
        },
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.getMaterial();
      },
      computed: {
        materialData1:function () {
          let search=this.search3;
          if(search){
            return  this.materialData.filter(function(dataNews){
              return Object.keys(dataNews).some(function(key){
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          return this.materialData
        },
      },
    }
</script>

<style scoped>

</style>
