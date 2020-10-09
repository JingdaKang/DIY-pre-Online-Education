<template>
  <div id="myResource" class="demo-block demo-zh-CN demo-form" v-loading="loading">
    <el-card class="box-card" style="width:100%;text-align: center;height:auto;min-height:700px">
      <p style="font-size:20px;font-weight:bold">
        我的资源
      </p>
      <el-divider></el-divider>
      <el-row>
        <el-form label-width="80px">
          <el-col :span="7">
            <el-form-item prop="keyword" label="文件名">
              <el-input v-model="keyword" style="float:left;width:90%;margin-left:10px"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item prop="type" label="文件类型">
              <el-select v-model="type" style="float: left;margin-left: 25px">
                <el-option label="不限" value=""></el-option>
                <el-option label="txt" value="txt"></el-option>
                <el-option label="pdf" value="pdf"></el-option>
                <el-option label="doc" value="doc"></el-option>
                <el-option label="docx" value="docx"></el-option>
                <el-option label="xlsx" value="xlsx"></el-option>
                <el-option label="zip" value="zip"></el-option>
                <el-option label="pptx" value="pptx"></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="4">
            <el-form-item>
              <el-button type="primary" icon="el-icon-search" style="float:left;margin-left: 0px"
                         v-on:click="search_by_condition">搜索
              </el-button>
            </el-form-item>
          </el-col>
        </el-form>
        <el-button size="medium" type="primary" plain style="float:right;margin-right:75px"
                   @click="batch_download()">批量下载
        </el-button>
      </el-row>
      <div v-if="page_resources.length==0" style="width:100%;height:200px">
        <h1 style="margin-top: 50px">这里什么都没有哦</h1>
      </div>
      <el-table :data="page_resources" v-if="page_resources.length!=0" ref="resource"
                @selection-change="handleSelectionChange"
                style="width: 100%;margin-top:20px" border>
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column prop="resource_name" label="资源名称" min-width="100" align="center">
          <template slot-scope="scope">
            {{getfileName(scope.row.location)}}
          </template>
        </el-table-column>
        <el-table-column prop="time" label="上传时间" min-width="100" align="center">
          <template slot-scope="scope">
            {{dateFormat(scope.row.time)}}
          </template>
        </el-table-column>
        <el-table-column prop="request" label="所属需求" min-width="100" align="center">
          <template slot-scope="scope">
            <a class="redirect" @click="gotoRequest(scope.row.request_id)">{{scope.row.context}}</a>
          </template>
        </el-table-column>
        <el-table-column prop="download" label="下载" min-width="100" align="center">
          <template slot-scope="scope">
            <el-row style="text-align:center">
              <a class="download" :href="download(scope.row.resource_id,getfileName(scope.row.location))">下载</a>
            </el-row>
          </template>
        </el-table-column>
      </el-table>
      <el-row style="margin-top:20px" v-if="page_resources.length!=0">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 50, 100, 200]"
          :page-size="10"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalCount">
        </el-pagination>
      </el-row>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    data() {
      return {
        loading: false,
        type: '',
        keyword: '',
        activeIndex: 1,
        currentPage: 1,
        pageSize: 10,
        totalCount: '',
        resourceList: [],
        page_resources: [],
        multipleSelection: []
      }
    },
    mounted() {
      let user_id = this.$cookies.get('user_id')
      if (user_id) {
        this.getResources()
      }  else {
       this,$router.push('/Home')
      }
    },
    methods: {
      getResources() {
        let that = this
        let param = new URLSearchParams()
        param.append('user_id', that.$cookies.get('user_id'))
        that.loading = true
        that.axios({
          method: 'post',
          url: '/iasystem/resources/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.resourceList = res.data.resources
              that.totalCount = res.data.resources.length
              that.get_page_resource()
              that.loading = false
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询类别失败')
            }
          })
      },
      get_page_resource() {
        this.page_resources = [];
        for (let i = (this.currentPage - 1) * this.pageSize; i < this.totalCount; i++) {
          this.page_resources.push(this.resourceList[i])
          if (this.page_resources.length == this.pageSize) break;
        }
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.get_page_resource()
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.get_page_resource()
      },
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.resource.toggleRowSelection(row);
          });
        } else {
          this.$refs.resource.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      download(value1, value2) {
        return "/iasystem/download/" + value1 + "/" + value2
      },
      getfileName(value) {
        let length1 = value.toLocaleString().length
        let temp = value.toLocaleString().substring(value.toLocaleString().lastIndexOf('/') + 1, length1)
        let length2 = temp.length
        let index = temp.indexOf('.')
        return temp.substring(0, index - 32) + temp.substring(index, length2)
      },
      gotoRequest(value) {
        this.$router.push({
          path: `/Request/${value}`,
        })
      },
      dateFormat(value) {
        const t = new Date(value);
        const time = t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() + " " + t.getHours() + ":" + t.getMinutes();
        return time;
      },
      search_by_condition() {
        let that = this
        let param = new URLSearchParams()
        let type = this.type
        let keyword = this.keyword
        param.append('user_id', that.$cookies.get('user_id'))
        if (type.length > 0) {
          param.append('type', type)
        } else {
          param.append('type', 0)
        }
        if (keyword.length > 0) {
          param.append('keyword', keyword)
        } else {
          param.append('keyword', 0)
        }
        that.loading = true
        that.axios({
          method: 'post',
          url: '/iasystem/search_by_condition/',
          data: param,
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.resourceList = res.data.resources
              that.totalCount = res.data.resources.length
              that.loading = false
              that.get_page_resource()
            } else if (res.data.code === 0) {
              that.loading = false
              that.$message.error('查询失败')
            }
          })
      },
      batch_download() {
        let that = this
        let param = new URLSearchParams()
        let i = 0
        let list = []
        let length = that.$refs.resource.selection.length
        for (i = 0; i < length; i++) {
          list.push(that.$refs.resource.selection[i].resource_id)
        }
        param.append('resources', list)
        that.axios({
          method: 'post',
          url: '/iasystem/batch_download/',
          data: param,
        })
          .then(function (res) {
            if (res.data.code === 1) {
              window.location.href = '/iasystem/download_zip/'
            }
          })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  .download {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #409EFF;
    background-color: #ECF5FF;
    border-color: #B3D8FF;
    font-size: 12px;
  }

  .download:hover {
    margin-left: 35%;
    display: block;
    border-radius: 5%;
    padding-top: 5px;
    padding-bottom: 5px;
    width: 60px;
    height: 20px;
    text-decoration: none;
    color: #FFFFFF;
    background-color: #409EFF;
    border-color: #409EFF;
    font-size: 12px;
  }

  .redirect {
    text-decoration: none;
    color: #000b16;
  }

  .redirect:hover {
    text-decoration: none;
    color: #409EFF;
  }
</style>
