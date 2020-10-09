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
          v-model="search5"
          placeholder="输入关键字搜索"/>
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
            prop="admin"
            label="管理员"
            width="100">
          </el-table-column>
          <el-table-column
            label="操作"
            width="134">
            <template slot-scope="scope">
              <el-button @click="downloadmaterial(scope.row.materialnumber)" type="text" >下载
                <i class="el-icon-download"></i></el-button>
              <el-button @click="deletematerial(scope.row.materialnumber)" type="text" v-if="user===scope.row.uploaduser||user===scope.row.admin">删除
                <i class="el-icon-delete"></i></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-main>
  </div>
</template>

<script>
    export default {
        name: "Material",
      data() {
        return {
          user: '',
          loading: false,
          search5: '',
          materialData: [],

        }
      },
      methods: {
        getMaterial(){
          this.materialData = [];
          this.loading = true;
          setTimeout(() => {
            this.$axios.post('/api/GetMaterial?S=1',{
              username:this.user
            }).then((res)=>{
              let tt = unescape(res.data.result).split(',');
              for(let i=0; i<tt.length/8; i++){
                let t = i*8;
                let ttt={
                  materialnumber:tt[t],
                  materialname:tt[t+5],
                  uploaduser:tt[t+4],
                  uploaddata:tt[t+6].substring(0,10)+" "+tt[t+6].substring(11,19),
                  belonged:tt[t+2],
                  courseid:tt[t+1],
                  teacher:tt[t+3],
                  admin:tt[t+7]
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
      },
      mounted() {
        this.user=this.$cookies.get('username');
        this.getMaterial();
      },
      computed: {
        materialData1:function () {
          let search=this.search5;
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
